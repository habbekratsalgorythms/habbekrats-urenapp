# First original Wan 2.2 5B video — local GPU, no paid credits

## Actual status (2026-11-08)

local_wan_render.py is an offline-first Python 3 tool with no extra Python packages. It validates one LOCAL ComfyUI API-format workflow, restricts node types and model files to the native Wan 5B template, fixes dimensions to 480x832, 73 frames and 24fps, and can submit exactly one local image-to-video render to an existing ComfyUI instance. Default is dry-run with ZERO network calls; explicit --execute is required to render. Video stays unpublished and manual quality approval is required.

This is NOT a remote connection to the owner's computer. No Windows files have been read, and no Wan generation has run on the owner's RTX 3070 yet. A future outbound-only, least-privilege worker can be designed after proof of successful local rendering. A full-access GitHub self-hosted runner or remote SSH/RDP is specifically not part of the proposed access model.

## Hardware & storage

Windows host NVIDIA RTX 3070 8GB VRAM, 32GB RAM. Use official Wan2.2 TI2V 5B with native offload. Model loads and render time cannot yet be predicted. Keep the separate SpotlessPro VM OFF when first trying heavy video rendering.

The user is moving ComfyUI data from an ordinary USB stick to an external SSD. IMPORTANT: E: is an EXAMPLE BELOW; replace it with the real SSD letter. Never cut-and-paste the running Desktop executable/application directory. ComfyUI Desktop keeps application resources and *user data* separately; the selected user data base path is tracked under %APPDATA%\ComfyUI\config.json as basePath. Close Desktop and back up settings before any relocation. Reopen and verify models/inputs/outputs on SSD, do not delete the original until tested. Keep drive letter fixed.

## First setup (not performed yet on Windows)

1. Complete and launch ComfyUI Desktop; verify NVIDIA/CUDA and local API port. Do not switch on Comfy Cloud payments.
2. Set a ComfyUI user-data base folder on external SSD (for example E:\AI\ComfyData) via Desktop's supported installation/data setup. Allow at least 30 GB free for model downloads and video outputs.
3. In Workflow > Browse Templates > Video, choose official Wan2.2 5B video generation. Download the three official models via ComfyUI: diffusion model wan2.2_ti2v_5B_fp16.safetensors, text encoder umt5_xxl_fp8_e4m3fn_scaled.safetensors, VAE wan2.2_vae.safetensors. Do not download untrusted executables.
4. Enable image-to-video branch on official Wan template (Ctrl+B on bypassed LoadImage/latent branch). Save workflow in ComfyUI's API JSON format, NOT ordinary UI save, to for example E:\AI\Klyptiq\wan_5b.api.json.
5. Store one original, owner-approved PNG at E:\AI\Klyptiq\Input\vexa-volt.png; other options pip-patch.png and blop.png.
6. Copy local_wan_render.py AND prepare_video_jobs.py together from the reviewed repository to E:\AI\Klyptiq\Scripts. Python 3 required on the Windows host.

## Offline, no-risk dry run

PowerShell command — change E: to actual SSD letter:

    py E:\AI\Klyptiq\Scripts\local_wan_render.py --workflow E:\AI\Klyptiq\wan_5b.api.json --images E:\AI\Klyptiq\Input --renders E:\AI\Klyptiq\Renders --persona vexa-volt

Expected SAFE DRY-RUN. It checks node set, models and wiring without GPU work or network. If the native template's API export has changed, stop and update/test our validator; never bypass safety checks just to force a job.

## One local render, only after dry-run

    py E:\AI\Klyptiq\Scripts\local_wan_render.py --workflow E:\AI\Klyptiq\wan_5b.api.json --images E:\AI\Klyptiq\Input --renders E:\AI\Klyptiq\Renders --persona vexa-volt --port 8000 --execute

Port 8000 may differ; Desktop's real loopback port could be 8188, 8189 or 8190. Script allows only exact loopback 127.0.0.1 with four ports. No public firewall rules, SSH or remote desktop. It expects one video result and writes a separate REVIEW-vexa-volt.mp4/webm on the SSD; it does not overwrite existing reviews.

This does NOT generate voice or synced lips. Official Wan 5B template outputs a silent video. Later stages: original Kokoro narration, independently evaluated lipsync, final FFmpeg editing and owner visual/audio rights review.

## Official reference links

- https://docs.comfy.org/tutorials/video/wan/wan2_2
- https://comfy.org/hub/workflows/wan-2-2-5b-video-generation-f83ee3caa04e/
- https://github.com/comfyorg/comfyui/blob/master/script_examples/websockets_api_example.py
- https://github.com/Comfy-Org/desktop
