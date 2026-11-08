#!/usr/bin/env python3
"""Prepare three separate image-to-video storyboard experiments safely offline.

Produces prompts/work-queue metadata for ComfyUI Wan2.2 TI2V 5B. Does NOT
download models, execute AI generation, create API charges or publish videos.
Requires visually consistent key art supplied and approved by the owner.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

BASE=Path(__file__).resolve().parent
PERSONAS={
 "vexa-volt":{
   "shot":"Vexa Volt in her futuristic studio near a skeptical evidence meter",
   "motion":"subtle natural blink and eyebrow raise, delicate head turn, antenna hairpin moving gently, holographic meter softly flickering",
   "camera":"slow cinematic dolly in, shallow depth of field",
   "constraints":"keep face, lavender asymmetrical hair, glasses, mustard jacket, logos and details consistent; NO morphing, no new text"
 },
 "pip-patch":{
   "shot":"Pip, cheerful orange-streaked creative tech host, with a small floating robot Patch",
   "motion":"Pip gives an expressive skeptical reaction; little robot tilts and bobs independently, soft glow pulses; no deformed hands",
   "camera":"subtle side-to-side camera slide; two distinct subjects in frame",
   "constraints":"robot must stay separate from Pip, same face and hair, no extra limbs; no nonsense subtitles, no shape or identity changes"
 },
 "blop":{
   "shot":"Blop the translucent mint-green alien in a crooked business suit examining a generic unbranded USB-C cable",
   "motion":"alien eye blink, slow elastic antenna sway, gentle hand holding a cable, amused head tilt, very subtle suit fabric movement",
   "camera":"slow macro push-in then settle",
   "constraints":"same translucent mint alien, two purple eyes and monocle, yellow tie; no brand marks; no extra limbs, face warping or captions"
 }
}

NEGATIVE=("melted hands, changing faces, inconsistent identities, extra fingers, distorted anatomy, "
          "random text, logo corruption, heavy camera shake, jerky motion, giant artificial subtitle banners, "
          "camera snap, flicker, deformed robots, duplicate characters")

def compile_jobs(images, seconds=3, width=480, height=832, fps=24):
    if seconds<2 or seconds>5 or fps!=24:
        raise ValueError("Start with short 2-5s 24fps clips on 8GB VRAM")
    if width%16 or height%16 or width>720 or height>1280 or width*height>480*832:
        raise ValueError("First 8GB evaluation must be <=480x832 and divisible by 16")
    frame_count=seconds*fps+1
    if (frame_count-1)%4:
        raise ValueError("Wan frames require 4n+1")
    jobs=[]
    for name,d in PERSONAS.items():
        img=images.get(name)
        if not isinstance(img,str) or not img.strip():
            raise ValueError("Owner-approved image required for "+name)
        # Do not assume the image file exists on GitHub Actions or on the local PC.
        path=Path(img).expanduser()
        if not path.is_file() or path.suffix.lower() not in {".png",".jpg",".jpeg",".webp"}:
            raise ValueError(name+": valid local character image not found")
        jobs.append({
           "persona":name,"mode":"image_to_video",
           "source_image":str(path.resolve()),
           "prompt":("A high-end stylized 3D character animation, faithful to the SOURCE IMAGE. "
                     +d["shot"]+". "+d["motion"]+". "+d["camera"]+". "
                     +"Stable character model and stable light; 9:16 cinematic composition. "
                     +d["constraints"]),
           "negative_prompt":NEGATIVE,
           "width":width,"height":height,"fps":fps,"frames":frame_count,
           "duration_seconds":seconds,
           "backend":"Wan2.2-TI2V-5B via local ComfyUI",
           "offload_model_to_cpu":True,
           "forbid_remote_api":True,"forbid_automatic_publication":True,
           "requires_visual_quality_review":True,
           "requires_ai_disclosure_before_post":True,
           "output_filename":"REVIEW-"+name+".mp4"
        })
    return jobs

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--vexa",required=True,type=Path)
    p.add_argument("--pip",required=True,type=Path)
    p.add_argument("--blop",required=True,type=Path)
    p.add_argument("--out",default="influencer-local-jobs.json",type=Path)
    a=p.parse_args()
    jobs=compile_jobs({"vexa-volt":str(a.vexa),"pip-patch":str(a.pip),"blop":str(a.blop)})
    output={"status":"PROMPTS_ONLY_NOT_GENERATED","model":"Wan2.2 TI2V 5B",
        "requires_local_comfyui_workflow":True,"paid_api_calls":0,
        "test_stages":["owner-approved original key art","three separate image-to-video clips",
                       "human visual and audio QA","free own FFmpeg assembly"],
        "jobs":jobs}
    a.out.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("Created local shot prompt manifest:",a.out)

if __name__=="__main__":main()
