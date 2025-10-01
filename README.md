# droidhead — All‑in‑One Kit (120B Teacher + Orin Runtime)

This bundle contains **everything** to build tiny **distillates on your Mac mini M4** (with a 120B teacher)
and deploy them to your **droidhead** (Jetson Orin Nano).

**Networks**
- **teacher-student-LAN** — your Mac mini (120B teacher + distillation)
- **droidhead-LAN** — your Orin Nano on the LAN
- **droidhead-local** — loopback inside the Orin (air‑gap mode)

Folders:
- `mac_distill/` — collect traces (from 120B), fine‑tune tiny router/style students (MLX), merge + GGUF, and deploy.
- `droidhead_runtime/` — docker stack for the Orin Nano (Ollama + STT + TTS + conductor).

Start by reading `mac_distill/README.md`, then deploy to the Orin with `make deploy` from `mac_distill/`.
<img width="564" height="564" alt="Crispy-Biscuits-Droid-Head" src="https://github.com/user-attachments/assets/e725a69d-3042-48ef-8522-e8448701faec" />
