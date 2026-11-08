# Influencer Lab — high-quality video production: GPU-first, cloud only if necessary

**Owner go-ahead, 8 Nov 2026:** Keep Vexa, Pip & Patch and Blop in development. Prefer visually rich, consistent character motion, **not** the old moving-caption slideshow. Owner has an NVIDIA RTX 3070, likely 8 GB VRAM. Total trial budget remains **€20 for all three**, within €100 across five income projects. No third-party generation, software subscription or API request was authorized merely by asking for an evaluation.

## Proven so far (no misleading success claims)

- Existing static AI key art for three distinctive personas has visual appeal.
- A **12 s free motion-design MP4** was rendered in this conversation with the reference artwork, original simple synthesizer beat, motion-poster camera moves and graphics. It does **NOT** contain facial acting, generated mouth movement, synchronized dialogue or live animation of limbs. This is only a baseline to beat, NOT a successful final animated persona.
- The actual owner's Windows GPU has **NOT yet been remotely accessed**; no local Wan inference has been performed. The host's driver, GPU free RAM, system RAM, available disk and ComfyUI version are unknown.

## Hardware verdict

- **RTX 3070 (normally 8 GB)**: viable for an experimental local Wan2.2 TI2V 5B ComfyUI workflow with **native offloading**. ComfyUI's own Wan2.2 docs explicitly say the 5B model fits 8GB VRAM with native offloading, but quality and runtime are not guaranteed.
- Begin at **480×832, 73 frames (about 3 sec @24fps)** with image-to-video, then test 480×832 at 121 frames/5 sec if stable. These are conservative trial settings, not model output guarantees.
- Local image-to-video of a known character key frame is preferable to pure prompt-to-video, because visual identity matters. Pip & Patch (two subjects) should be separately controlled when practical.
- **LTX Desktop is NOT a free local-generation option on 8GB VRAM:** their published app minimum is 16GB and recommends 32GB; under 16GB the desktop app uses the paid API.
- Keep the generation workflow on the **Windows host**, where the graphics driver directly accesses RTX3070. GPU passthrough into a separate Hyper-V Ubuntu VM is not assumed. WSL2 with NVIDIA drivers may also work, but native Windows ComfyUI is simpler for first try. Do not change the SpotlessPro VM or experiment with GPU-P without a separate safe plan.

### Zero-change initial GPU check

On the Windows HOST, open PowerShell and run:

```powershell
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
```

Alternatively, when cloned locally with Python 3:

```powershell
py influencer-lab\gpu_preflight.py --save gpu-report.json
```

This checks availability without changing drivers, downloading models, running GPU inference, signing into any site or buying credits. **Do not paste passwords, cookies, API keys or private files** into chat.

### Free local inference pilot (only after GPU check)

1. Install the official **ComfyUI Desktop/Windows** version from <https://www.comfy.org/download> on the host; no browser-exposed 0.0.0.0 server and no remote access.
2. In ComfyUI -> Workflow -> Browse Templates -> Video, choose **Wan2.2 5B video generation**, the official native-offloading 5B workflow.
3. Download official model weights via ComfyUI's model manager or the sources linked in the official tutorial, leaving disk headroom (plan 30GB+ available for staged model files, caches and output). Do not download untrusted 'free optimized' executables.
4. From three individually approved original key-art images, build a prompt manifest:
```powershell
py influencer-lab\prepare_video_jobs.py --vexa C:\Art\vexa.png --pip C:\Art\pip-patch.png --blop C:\Art\blop.png --out C:\Art\wan-first-tests.json
```
5. Use the resulting prompts with the official TI2V I2V template, starting with each character's three-second camera/face performance. The script generates **prompts**, not a ComfyUI workflow or MP4. In the template select the corresponding local images and prompts; try one at a time.
6. Reject generations with identity drift, melting hands, blinking eyes in strange places, inconsistent hair, robot merging with Pip, inaccurate lips or noticeable flicker. Do not assume the first sample is good.
7. If this works, feed each approved local MP4 into a separate FFmpeg assembly with original caption animation, polished voice, original sound and clear 9:16 framing. No third-party protected footage, unauthorized voice impersonation or hidden brand sponsorship.

## Optional Grok fallback (NOT ENABLED)

xAI API price list verified Nov 8 2026; **USD, excluding taxes, input fees and unsuccessful attempts**. Prices can change; verify again before making requests.

| Model | 480p/sec | 720p/sec | 1080p/sec | Best use |
| --- | ---: | ---: | ---: | --- |
| grok-imagine-video-1.5-lite | $0.02 | $0.03 | $0.14 | Cheapest short motion test from character artwork |
| grok-imagine-video | $0.05 | $0.07 | not offered | Legacy edit/extend |
| grok-imagine-video-1.5 | $0.08 | $0.14 | $0.25 | Strong character references, natural face motion and native high res |

Example excluding input costs and retries: **one 5s 720p** Lite clip ~$0.15; main model ~$0.70; native 1080p main model ~$1.25. Total cost scales linearly with **all** generated attempts, not simply the clips you keep. Lite 1080p is upscaled from 720p. Full 1.5 image-to-video supports native 1080p; reference-to-video with multiple images currently supports up to 720p. Official xAI supports 15s clips max per request. See <https://docs.x.ai/developers/pricing> and <https://docs.x.ai/developers/model-capabilities/video/overview>.

**No API spending without explicit approval for an exact, fixed maximum.** For a first fallback trial propose a hard **$3 max** across ~10 short Lite 720p 5s attempts (includes room for image-input fees), *but approval has not been granted*. Disable auto top-up and use account-side budget limits if xAI supports them; otherwise do not automate paid generation.

## Creative quality gates and asset strategy

- Keep **one clearly documented key art + expression/turnaround references** per persona. Use consistent wardrobe, color, eye design and distinctive prop; export separate images for each persona instead of cropping a busy three-panel poster for final clips.
- Produce **true character motion** (head/eyes/body/robot) first. Add talking/phoneme lip-sync only after identity is stable, with voice pacing checked. A text-to-speech voice by itself does not animate a mouth.
- The trailer/promo style should have rapid meaningful visual beats, but not rely on camera zoom to pretend a stationary person is acting.
- Use only original characters and commercially acceptable model/tool/asset rights, and check platform AI labels before any release. No real people's faces or voices cloned.
- Score first 3s hook, character consistency, natural motion, voice/audio quality, edit rhythm, AI disclosure, claims, legal rights and per-episode cost separately. Technical MP4 validity is a necessary condition but not creative approval.
- **Do not call a video equivalent to the sample image until real side-by-side visual comparison confirms the same degree of detailed look and convincing motion.**

## Official sources
- ComfyUI Wan2.2: <https://docs.comfy.org/tutorials/video/wan/wan2_2>
- ComfyUI community model announcement: <https://blog.comfy.org/p/wan22-day-0-support-in-comfyui>
- Wan Apache 2.0 license: <https://github.com/Wan-Video/Wan2.2>
- NVIDIA CUDA on WSL2: <https://docs.nvidia.com/cuda/wsl-user-guide/>
- LTX Desktop local restrictions: <https://help.ltx.io/hc/en-us/articles/37088977573138-Local-mode-and-API-mode-in-LTX-Desktop>
- Grok 1.5/Lite video features and pricing: <https://docs.x.ai/developers/model-capabilities/video/overview>
