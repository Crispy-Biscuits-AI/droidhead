from fastapi import FastAPI, UploadFile, File, Body
from faster_whisper import WhisperModel
import os, io, httpx
app = FastAPI(title="ASR Student (Faster-Whisper)")
MODEL_SIZE = os.getenv("ASR_MODEL_SIZE", "small")
DEVICE = os.getenv("ASR_DEVICE", "auto")
COMPUTE_TYPE = os.getenv("ASR_COMPUTE_TYPE", "auto")
BEAM_SIZE = int(os.getenv("ASR_BEAM_SIZE", "1"))
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE, download_root="/models")
@app.post("/transcribe")
async def transcribe(audio: UploadFile | None = File(default=None), audio_url: str | None = Body(default=None, embed=True)):
    if audio is None and audio_url is None:
        return {"error": "Provide multipart file 'audio' or 'audio_url'."}
    if audio is not None:
        wav_bytes = await audio.read()
    else:
        async with httpx.AsyncClient(timeout=None) as client:
            r = await client.get(audio_url); r.raise_for_status(); wav_bytes = r.content
    segments, info = model.transcribe(io.BytesIO(wav_bytes), beam_size=BEAM_SIZE)
    text = "".join([seg.text for seg in segments])
    return {"text": text, "language": info.language, "duration": info.duration}
