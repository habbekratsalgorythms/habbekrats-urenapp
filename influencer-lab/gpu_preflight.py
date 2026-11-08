#!/usr/bin/env python3
"""Read-only GPU/host readiness report for local video-generation experiments.

No downloads, hardware settings, network calls, model inference or GPU allocation.
This helps decide if a Windows-host RTX 3070 can test Wan2.2-TI2V-5B using
ComfyUI native model offloading. Does NOT guarantee speed/quality.
"""
from __future__ import annotations
import argparse
import json
import os
import platform
import re
import shutil
import subprocess
from pathlib import Path

def _run(command):
    try:
        return subprocess.run(command,capture_output=True,text=True,timeout=8,check=True).stdout.strip()
    except (FileNotFoundError, OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None

def parse_smi(text):
    """Return GPU cards; recognize comma/space in GPU name."""
    cards=[]
    if not text: return cards
    for line in text.splitlines():
        # Format: name, memory.total MiB, driver_version
        m=re.match(r"^(.+?),\s*(\d+(?:\.\d+)?)\s*(?:MiB|MB)?\s*,\s*([\d.]+)\s*$",line.strip())
        if m:
            cards.append({"name":m.group(1).strip(),"vram_mib":int(float(m.group(2))),
                          "driver":m.group(3)})
    return cards

def probe(smi_output=None,disk_path=None):
    smi=smi_output if smi_output is not None else _run(["nvidia-smi",
        "--query-gpu=name,memory.total,driver_version","--format=csv,noheader"])
    cards=parse_smi(smi)
    disk=Path(disk_path or Path.home())
    try:
        free_gib=round(shutil.disk_usage(disk).free / (1024**3),1)
    except (OSError,ValueError):
        free_gib=None
    win=platform.system().lower()=="windows"
    names=" ".join(g["name"] for g in cards).lower()
    eligible=any(g["vram_mib"]>=7600 for g in cards)
    if cards and eligible:
        recommendation="TRY_WAN22_5B_COMFYUI_LOW_VRAM"
    elif cards:
        recommendation="GPU_FOUND_BUT_8GB_CLASS_NOT_CONFIRMED"
    else:
        recommendation="NEED_WINDOWS_NVIDIA_DRIVER_OR_WSL_GPU_VISIBILITY"
    return {
        "host_platform":platform.platform(),
        "cards":cards,
        "disk_free_gib":free_gib,
        "run_on":"Windows host with native NVIDIA GPU" if win else "GPU-enabled Linux or WSL2 (not unconfigured Hyper-V guest)",
        "recommended_first_experiment":recommendation,
        "suggested_video_model":"Wan2.2-TI2V-5B (ComfyUI, native offload; small image-to-video clips)",
        "model_quality_is_proven":False,
        "local_gpu_was_exercised":False,
        "estimated_hardware_note":"RTX 3070 usually has 8GB VRAM; test 480p/short clips first; high-end 14B/LTX Desktop local mode need more VRAM.",
        "allow_paid_fallback_without_approval":False,
        "suggested_storage_headroom_gib":30,
        "storage_readiness":"CHECK_SPACE" if free_gib is None else ("SUFFICIENT_FOR_STAGED_TEST" if free_gib>=30 else "INSUFFICIENT_FOR_STAGED_TEST"),
        "powershell_next":"nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader"
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--save",type=Path,help="optional local JSON output")
    a=p.parse_args()
    result=probe()
    content=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    print(content)
    if a.save:
        a.save.parent.mkdir(parents=True,exist_ok=True)
        a.save.write_text(content,encoding="utf-8")

if __name__=="__main__":main()
