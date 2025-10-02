“Crispy Biscuits is where we bake new AI minds — experiments in distillation, orchestration, and droidhead design.”

# CrispyBiscuits.ai: Droid Head — gpt-oss-20b Teacher-Student "trainging-bed".

This repo helps you collect traces from a **20B teacher** running on your Mac mini (Docker) and fine‑tune **tiny students** on Apple Silicon using **MLX** (Metal). Students target two roles:

1. **Router student (1–3B)** — classifies text → {skill,args} (always‑on on droidhead).
2. **Style student (1–3B or 7–8B)** — copies tone/voice for short answers (optional).

**Networks we’ll reference**
- **teacher-student-LAN** — your Mac mini M4 hosting the 20B and these scripts.
- **droidhead-LAN** — your Orin Nano on the LAN.
- **droidhead-local** — loopback (127.0.0.1) on the Orin when radios are off.

---

## Prereqs (macOS Apple Silicon)
```bash
# Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python env manager
brew install uv
uv venv .venv && source .venv/bin/activate

# Core libs
uv pip install mlx mlx-lm transformers datasets peft accelerate sentencepiece jsonlines requests
```

> Make sure your **20B teacher** is up and exposes an OpenAI‑compatible endpoint (adjust host/port as needed):
> `http://localhost:8000/v1/chat/completions`

Configure it in `config/teacher.json`.

---

## 1) Collect traces from the teacher

**Router labels**
```bash
python scripts/collect_routes.py   --config config/teacher.json   --input prompts/router_seed.txt   --out data/routes.jsonl
```

**Style pairs**
```bash
python scripts/collect_style.py   --config config/teacher.json   --input prompts/style_seed.txt   --out data/style.jsonl
```

---

## 2) Fine‑tune tiny students on the Mac (MLX)

**Router (choose a small base)** e.g. TinyLlama 1.1B or Llama‑3.2‑3B:
```bash
python train/finetune_router_mlx.py   --base TinyLlama/TinyLlama-1.1B-Chat-v1.0   --train_jsonl data/routes.jsonl   --out models/router_student_mlx   --epochs 2 --lr 5e-5 --batch 8
```

**Style (optional)** e.g. Llama‑3.2‑3B:
```bash
python train/finetune_style_mlx.py   --base meta-llama/Llama-3.2-3B-Instruct   --train_jsonl data/style.jsonl   --out models/style_student_mlx   --epochs 1 --lr 5e-5 --batch 4
```

---

## 3) Merge LoRA + convert to GGUF (for Ollama on droidhead)

```bash
# Merge LoRA into base
python tools/merge_lora.py   --base TinyLlama/TinyLlama-1.1B-Chat-v1.0   --lora models/router_student_mlx   --out models/router_merged

# Convert to GGUF (follow llama.cpp instructions printed by the helper)
python tools/convert_to_gguf.py   --in models/router_merged   --out gguf/router-student.gguf
```

---

## 4) Deploy to droidhead (Orin Nano)

Copy `gguf/router-student.gguf` to the Orin. On the Orin:
```bash
ollama create router-student -f ollama/RouterStudent.Modelfile
```

Then point your **droidhead** conductor to `router-student` for routing, and keep your bigger chat model in Ollama or another runtime.

---

## Tips
- Keep router data **small and clean**; aim for precision.
- Track confidence and fall back to your bigger chat model when in doubt.
- Quantize to **Q4** for always‑on low‑power on the Orin.
