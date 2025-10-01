
<img width="896" height="507" alt="cbdh-logo" src="https://github.com/user-attachments/assets/6925e87c-f2cf-4045-9883-4000b88f3571" />

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
