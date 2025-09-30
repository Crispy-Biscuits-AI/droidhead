# mac_distill — Distill tiny students with a 120B teacher (Mac mini M4)

This uses **gpt-oss-120b** (in Docker) as teacher on **teacher-student-LAN**, collects traces concurrently,
fine‑tunes **router/style** students using **MLX** (Metal), merges LoRA, converts to **GGUF**, and **deploys** to **droidhead-LAN**.

## Prereqs
```bash
brew install uv
uv venv .venv && source .venv/bin/activate
uv pip install mlx mlx-lm transformers datasets peft accelerate sentencepiece jsonlines aiohttp requests
```

## One‑liners
```bash
make collect_async   # concurrent labeling from 120B (routes + style)
make train           # MLX LoRA fine‑tune (router student)
make merge           # merge LoRA into base
make gguf            # GGUF conversion helper (prints llama.cpp commands)
make eval            # quick router stats
make deploy          # scp GGUF to droidhead-LAN (edit DROIDHOST/DROIDPATH first)
make remote_create   # (optional) SSH to droidhead-LAN and run 'ollama create' remotely
```
