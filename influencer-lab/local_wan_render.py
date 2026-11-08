#!/usr/bin/env python3
"""STRICT local ComfyUI Wan2.2 5B proof-of-concept runner (standard library only).

Defaults to OFFLINE DRY RUN. NEVER downloads a model, installs dependencies,
reads remote GitHub jobs, changes Windows settings, publishes, or spends money.

Input: locally exported ComfyUI workflow in API FORMAT (not UI-format JSON).
Only the exact built-in Wan 5B node family is allowed. Images are read ONLY
from the named project's input directory, and results written to its renders
directory. ComfyUI is contacted exclusively via loopback 127.0.0.1.

Only --execute sends a request to the user's already-running local ComfyUI.
This script intentionally is NOT an autonomous remotely-triggered bridge.
"""
from __future__ import annotations

import argparse
import copy
import json
import mimetypes
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

from prepare_video_jobs import NEGATIVE, PERSONAS

MODEL = "wan2.2_ti2v_5B_fp16.safetensors"
TEXT_ENCODER = "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
VAE = "wan2.2_vae.safetensors"
CLASSES = {
    "UNETLoader": 1, "CLIPLoader": 1, "VAELoader": 1,
    "CLIPTextEncode": 2, "Wan22ImageToVideoLatent": 1,
    "LoadImage": 1, "KSampler": 1, "ModelSamplingSD3": 1,
    "VAEDecode": 1, "CreateVideo": 1, "SaveVideo": 1,
}
PORTS = {8000, 8188, 8189, 8190}
IMAGE_NAMES = {name: name + ".png" for name in PERSONAS}
IMAGE_MAX_BYTES = 12 * 1024 * 1024
VIDEO_MAX_BYTES = 120 * 1024 * 1024
MAX_NODES = 24

def _single(workflow, class_type):
    values = [node for node in workflow.values() if node["class_type"] == class_type]
    if len(values) != 1:
        raise ValueError(f"Expected exactly one {class_type}")
    return values[0]

def validate_api_workflow(raw):
    """Deny unknown nodes, unknown models, and all non-standard workflow shapes."""
    if not isinstance(raw, dict) or not 10 <= len(raw) <= MAX_NODES:
        raise ValueError("Expected a small ComfyUI API-format node dictionary")
    counts = {}
    for key, node in raw.items():
        if not isinstance(key, str) or not re.fullmatch(r"[0-9]{1,5}", key):
            raise ValueError("Nonstandard ComfyUI API node id")
        if not isinstance(node, dict) or set(node) - {"class_type", "inputs", "_meta"}:
            raise ValueError("Unsupported or malformed ComfyUI node")
        kind, inputs = node.get("class_type"), node.get("inputs")
        if kind not in CLASSES or not isinstance(inputs, dict):
            raise ValueError("Unknown/forbidden node type: " + str(kind))
        counts[kind] = counts.get(kind, 0) + 1
        for item in inputs.values():
            if isinstance(item, list) and len(item) == 2 and isinstance(item[0], str):
                if item[0] not in raw:
                    raise ValueError("Graph link escapes allowed workflow")
            elif isinstance(item, (list,dict)):
                raise ValueError("Unrecognized input structure")
    if counts != CLASSES:
        raise ValueError("Workflow is not the exact expected native Wan 5B node set")
    for kind, field, expected in (
        ("UNETLoader", "unet_name", MODEL),
        ("CLIPLoader", "clip_name", TEXT_ENCODER),
        ("VAELoader", "vae_name", VAE),
    ):
        if _single(raw, kind)["inputs"].get(field) != expected:
            raise ValueError("Wrong model in " + kind)
    sampler = _single(raw, "KSampler")["inputs"]
    if "positive" not in sampler or "negative" not in sampler:
        raise ValueError("Missing positive/negative prompt connections")
    positive, negative = sampler["positive"], sampler["negative"]
    if not all(isinstance(x,list) and len(x)==2 for x in (positive,negative)):
        raise ValueError("Prompt connections must link to CLIP nodes")
    if positive[0] == negative[0]:
        raise ValueError("Positive and negative nodes must be separate")
    for link in (positive, negative):
        if raw.get(link[0], {}).get("class_type") != "CLIPTextEncode":
            raise ValueError("Prompt node is not CLIPTextEncode")
    latent = _single(raw, "Wan22ImageToVideoLatent")["inputs"]
    start = latent.get("start_image")
    if not isinstance(start,list) or len(start)!=2 or raw.get(start[0],{}).get("class_type")!="LoadImage":
        raise ValueError("Image-to-video connection must be enabled, not text-only")
    return copy.deepcopy(raw)

def build_workflow(exported, persona, uploaded_image_filename):
    """Rewrite every user-controlled generation field to hard-coded safe limits."""
    if persona not in PERSONAS:
        raise ValueError("Unknown persona")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,100}\.(png|jpg|jpeg|webp)", uploaded_image_filename, re.I):
        raise ValueError("Unsafe uploaded image filename")
    wf = validate_api_workflow(exported)
    details = PERSONAS[persona]
    pos = ("An exquisitely crafted cinematic original character animation, "
           "faithful to source art. " + details["shot"] + ". " + details["motion"]
           + ". " + details["camera"] + ". Stable colors and recognizable face. "
           + details["constraints"])
    sampler = _single(wf, "KSampler")["inputs"]
    wf[sampler["positive"][0]]["inputs"]["text"] = pos
    wf[sampler["negative"][0]]["inputs"]["text"] = NEGATIVE
    latent = _single(wf, "Wan22ImageToVideoLatent")["inputs"]
    latent.update({"width":480, "height":832, "length":73, "batch_size":1})
    _single(wf, "LoadImage")["inputs"]["image"] = uploaded_image_filename
    sampler.update({"seed":87123,"steps":20,"cfg":5.0,"sampler_name":"uni_pc",
                    "scheduler":"simple","denoise":1.0})
    _single(wf, "CreateVideo")["inputs"]["fps"] = 24
    # The only output is a review draft inside ComfyUI's standard output folder.
    _single(wf, "SaveVideo")["inputs"]["filename_prefix"] = "Klyptiq/REVIEW-" + persona
    return wf

def _read_image(images_dir: Path, persona: str):
    root = images_dir.resolve(strict=True)
    # Never allow symlinks to another directory, nor source images from Documents.
    image = root / IMAGE_NAMES[persona]
    if image.is_symlink() or not image.is_file() or image.resolve().parent != root:
        raise ValueError("Expected direct non-symlink image: " + IMAGE_NAMES[persona])
    if image.stat().st_size < 100 or image.stat().st_size > IMAGE_MAX_BYTES:
        raise ValueError("Image size out of approved range (100 bytes - 12 MiB)")
    data = image.read_bytes()
    if not (data.startswith(b"\x89PNG\r\n\x1a\n")):
        raise ValueError("Only real PNG signature images accepted")
    return data

def _url(port, endpoint):
    if port not in PORTS:
        raise ValueError("Only designated local ComfyUI ports are allowed")
    if not endpoint.startswith("/") or "//" in endpoint or "\\" in endpoint:
        raise ValueError("Invalid ComfyUI API path")
    return f"http://127.0.0.1:{port}{endpoint}"

def _send(port, endpoint, body=None, headers=None, timeout=12):
    req = urllib.request.Request(_url(port,endpoint), data=body, headers=headers or {})
    with urllib.request.urlopen(req,timeout=timeout) as res:
        data = res.read(15 * 1024 * 1024)
    return data

def _upload_png(port, image_bytes, persona):
    boundary = "comfy" + uuid.uuid4().hex
    fname = persona + "-" + uuid.uuid4().hex[:12] + ".png"
    b = boundary.encode("ascii")
    body = (
        b"--"+b+b"\r\n"
        +b'Content-Disposition: form-data; name="image"; filename="'+fname.encode()+b'"\r\n'
        +b"Content-Type: image/png\r\n\r\n"+image_bytes+b"\r\n"
        +b"--"+b+b"\r\n"
        +b'Content-Disposition: form-data; name="type"\r\n\r\ninput\r\n'
        +b"--"+b+b"--\r\n"
    )
    response = json.loads(_send(port,"/upload/image",body,
            {"Content-Type":"multipart/form-data; boundary="+boundary},timeout=40))
    result = response.get("name")
    if not isinstance(result,str) or result!=fname:
        raise ValueError("ComfyUI did not confirm the exact image upload")
    return result

def _queue(port, workflow):
    payload = json.dumps({"prompt":workflow,"client_id":"klyptiq-local-review"}).encode("utf-8")
    result = json.loads(_send(port,"/prompt",payload,
        {"Content-Type":"application/json"},timeout=20))
    ident=result.get("prompt_id")
    if not isinstance(ident,str):
        raise RuntimeError("ComfyUI refused prompt: "+str(result.get("error", "missing id")))
    return ident

def _wait_and_fetch(port, prompt_id, output_dir, persona, deadline_s=7200):
    deadline=time.monotonic()+deadline_s
    result=None
    while time.monotonic()<deadline:
        data=json.loads(_send(port,"/history/"+urllib.parse.quote(prompt_id,safe=""),timeout=15))
        if prompt_id in data:
            result=data[prompt_id]
            break
        time.sleep(6)
    if result is None:
        raise TimeoutError("Render did not complete in allotted local time")
    if result.get("status",{}).get("status_str")=="error":
        raise RuntimeError("ComfyUI reported execution error; inspect its local logs")
    files=[]
    for node in result.get("outputs",{}).values():
        for field in ("gifs","videos","video"):
            entries=node.get(field,[])
            if isinstance(entries,dict): entries=[entries]
            for entry in entries:
                if isinstance(entry,dict) and entry.get("type")=="output":
                    files.append(entry)
    if len(files)!=1:
        raise ValueError("Expected exactly one completed output video; inspect ComfyUI")
    entry=files[0]
    fname, sub = entry.get("filename"),entry.get("subfolder","")
    if not isinstance(fname,str) or not fname.lower().endswith((".mp4",".webm")):
        raise ValueError("Unsupported local video extension")
    if not re.fullmatch(r"[a-zA-Z0-9_.-]{1,170}",fname):
        raise ValueError("Unsafe output name")
    if not isinstance(sub,str) or (sub and not re.fullmatch(r"[A-Za-z0-9_-]{1,50}",sub)):
        raise ValueError("Unsafe output subfolder")
    params=urllib.parse.urlencode({"filename":fname,"subfolder":sub,"type":"output"})
    data=_send(port,"/view?"+params,timeout=120)
    if not 1000<len(data)<=VIDEO_MAX_BYTES:
        raise ValueError("Output video size out of range")
    dest=output_dir / ("REVIEW-"+persona+Path(fname).suffix.lower())
    if dest.exists():
        raise FileExistsError("Refusing to overwrite existing preview: "+str(dest))
    dest.write_bytes(data)
    return dest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--workflow",type=Path,required=True,
                   help="ComfyUI export: Save (API Format), not UI workflow")
    p.add_argument("--images",type=Path,required=True,
                   help="Dedicated local folder with approved named PNG assets")
    p.add_argument("--renders",type=Path,required=True,
                   help="Dedicated local folder for review output")
    p.add_argument("--persona",choices=list(PERSONAS),default="vexa-volt")
    p.add_argument("--port",type=int,choices=sorted(PORTS),default=8000)
    p.add_argument("--execute",action="store_true",
                   help="Only if explicitly chosen: submit ONE local render")
    args=p.parse_args()
    wf=json.loads(args.workflow.read_text(encoding="utf-8"))
    # Validate workflow BEFORE any local network calls or files created.
    build_workflow(wf,args.persona,IMAGE_NAMES[args.persona])
    if not args.execute:
        print("SAFE DRY-RUN: approved Wan node set, models and prompt wiring only.")
        print("No GPU use, no upload, no file changes. For real run use --execute.")
        print("Expected image: ",args.images / IMAGE_NAMES[args.persona])
        return 0
    image=_read_image(args.images,args.persona)
    args.renders.mkdir(parents=True,exist_ok=True)
    if args.renders.is_symlink():
        raise ValueError("Renders folder must not be a symlink")
    result_path=args.renders / ("REVIEW-"+args.persona+".mp4")
    if result_path.exists():
        raise FileExistsError("Review output exists: please move it first")
    uploaded=_upload_png(args.port,image,args.persona)
    job=build_workflow(wf,args.persona,uploaded)
    prompt_id=_queue(args.port,job)
    print("Render queued locally; prompt ID:",prompt_id,flush=True)
    out=_wait_and_fetch(args.port,prompt_id,args.renders,args.persona)
    print("Local render complete:",out)
    print("PUBLICATION BLOCKED; manual visual + voice + rights review still required.")
    return 0

if __name__=="__main__":
    try:
        sys.exit(main())
    except (ValueError,TimeoutError,FileNotFoundError,FileExistsError,urllib.error.URLError,RuntimeError) as exc:
        print("STOP (no silent fallback):",exc,file=sys.stderr)
        sys.exit(2)
