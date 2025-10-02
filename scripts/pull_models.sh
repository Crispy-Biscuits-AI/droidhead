#!/usr/bin/env bash
set -euo pipefail
mkdir -p models/tts models/asr
if [[ -n "${PIPER_VOICE_URL:-}" ]]; then curl -L "$PIPER_VOICE_URL" -o models/tts/voice.onnx.gz && gunzip -f models/tts/voice.onnx.gz || true; fi
echo "ASR models auto-download on first run."
