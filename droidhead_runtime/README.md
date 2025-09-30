# droidhead_runtime — Orin Nano stack

- **Ollama** serves the router student and your chat model.
- **Faster-Whisper** for STT.
- **Piper** for TTS (Wyoming).
- **Conductor** (FastAPI) glues it together.

## Usage
```bash
docker compose up -d
# After copying GGUF + Modelfile (see mac_distill Makefile):
ollama create router-student -f ~/ollama/RouterStudent.Modelfile
curl -s http://127.0.0.1:8080/ask -H 'content-type: application/json' -d '{"text":"increase the volume"}'
```
