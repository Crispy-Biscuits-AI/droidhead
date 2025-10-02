from fastapi import FastAPI, Body, Response
import subprocess, os, tempfile
app = FastAPI(title="TTS Student (Piper)")
PIPER_BIN = os.getenv("PIPER_BIN", "piper")
MODEL = os.getenv("PIPER_MODEL", "/models/tts/voice.onnx")
@app.post("/speak")
async def speak(text: str = Body(..., embed=True)):
    if not os.path.exists(MODEL):
        return {"error":"Missing Piper voice model (.onnx)", "PIPER_MODEL": MODEL}
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = tmp.name
    try:
        subprocess.check_call([PIPER_BIN, "-m", MODEL, "-f", wav_path, "-t", text])
        data = open(wav_path, "rb").read()
        os.unlink(wav_path)
        return Response(content=data, media_type="audio/wav")
    except Exception as e:
        return {"error": str(e)}
