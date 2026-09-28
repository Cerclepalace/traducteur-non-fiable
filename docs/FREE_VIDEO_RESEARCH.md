# VIDEO FACTORY V2 — FREE VIDEO RESEARCH

Date: 2026-09-28

## Objective

Determine whether Video Factory V2 can produce videos at 0 EUR per generated video without ElevenLabs or mandatory paid APIs.

## Reference architecture

Script
→ Chatterbox
→ audio analysis
→ WhisperX alignment
→ scene planner
→ image/keyframe
→ video generation
→ subtitles
→ FFmpeg
→ QC
→ final MP4

## Findings

### Software / model layer

- Chatterbox: local TTS; MIT-licensed model/project; no mandatory paid API.
- WhisperX: local ASR/alignment; BSD-2-Clause; no mandatory paid API.
- FFmpeg: free/open-source; licensing depends on the build and enabled components.
- WAN 2.2: open model family; official repository uses Apache-2.0 for the referenced models.
- Wan-Animate-2: open implementation; suitable as an optional character-animation backend.
- HunyuanVideo-1.5: technically relevant, but its Tencent community license must be checked before commercial deployment.
- LTX-2.x: technically relevant, especially for audio/video generation, but its license contains commercial conditions; it must remain optional until the exact commercial use case is cleared.

## Cost distinction

0 EUR software/model access does NOT imply unlimited free computation.

The real cost constraints are:

1. GPU availability
2. VRAM
3. model storage
4. download bandwidth
5. electricity
6. cloud/API usage

## Local zero-variable-cost path

Preferred architecture:

Chatterbox local
→ WhisperX local
→ WAN local
→ FFmpeg local
→ local storage

This removes mandatory per-generation API charges.

## Cloud-free path

Google Colab Free can provide GPU access subject to availability, quotas and changing resource limits. It must therefore be treated as an optional execution backend, not as guaranteed production infrastructure.

## Hardware constraint

The current target machine has 12 GB VRAM.

Large video models cannot be assumed compatible with 12 GB VRAM. Compatibility must be measured for each exact model, quantization, resolution, duration and offloading configuration.

Status:
- Chatterbox: likely compatible; must be benchmarked.
- WhisperX: likely compatible; must be benchmarked.
- FFmpeg: compatible.
- Large WAN/Hunyuan/LTX variants: UNKNOWN until executed on the target environment.
- Colab Free: availability UNKNOWN per runtime.

## Economic conclusion

### VERIFIED CONCEPT

A 0 EUR-per-video architecture is technically possible when:
- all mandatory components run locally;
- no paid API is required;
- the available GPU is already owned or obtained through a free quota.

### NOT VERIFIED

The following are NOT established:
- unlimited free cloud GPU;
- guaranteed Colab Free availability;
- 60-second video generation at a fixed throughput on a 12 GB GPU;
- commercial eligibility for every model/license;
- production-scale volume at 0 EUR.

## Architectural rule

Paid cloud providers may be implemented as optional providers, never as mandatory dependencies of the Video Factory core.

Recommended abstraction:

VideoProvider
→ VideoRegistry
→ VideoRouter
→ local/free provider first
→ optional paid fallback only when explicitly enabled

## Decision status

FREE SOFTWARE CORE: VERIFIED
NO MANDATORY PAID API: ARCHITECTURALLY ACHIEVABLE
0 EUR PER VIDEO: CONDITIONALLY ACHIEVABLE
UNLIMITED 0 EUR CLOUD PRODUCTION: NOT ESTABLISHED
12 GB VIDEO GENERATION: UNKNOWN UNTIL BENCHMARKED

## Validation requirement

No component receives VERIFIED status for runtime compatibility until it is executed and measured on the actual target environment.

No mock or simulated generation may be reported as real.

## External reference projects reviewed

- NilhanHub/video-factory: evidence-led local short-form pipeline using local TTS, FFmpeg and QA; useful architectural reference for reproducibility and no-fake-functionality discipline.
- NesDevr/video-factory: automated video factory architecture with checkpoints, retries and cost traces.
- lisering/video-translator: local-first video processing with local models and no mandatory API keys.
- overcrash66/video-translator: local video translation architecture without cloud APIs/subscriptions.

These projects are references only and do not establish compatibility with Video Factory V2.

## Final reference principle

The objective is not “free SaaS”.

The objective is:

local/open models + deterministic orchestration + measurable GPU execution + no mandatory paid API.
