<img width="576" height="326" alt="cbdh-logo-01" src="https://github.com/user-attachments/assets/e1f8b88a-a169-439e-96a5-a1e4ed89fa7c" />


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
