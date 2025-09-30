import os, json, logging
from typing import Dict, Any
from fastapi import FastAPI, Body
import httpx

app = FastAPI(title="droidhead Conductor")
STUDENT_URL = os.getenv("STUDENT_URL", "http://127.0.0.1:11434")
STT_URL = os.getenv("STT_URL", "http://127.0.0.1:9000")
TTS_HOST = os.getenv("TTS_HOST", "127.0.0.1")
TTS_PORT = int(os.getenv("TTS_PORT", "10200"))
MODEL_NAME = os.getenv("MODEL_NAME", "router-student")

logging.basicConfig(level=logging.INFO)
client = httpx.AsyncClient(timeout=30.0)

async def ollama_generate(prompt: str, model: str) -> str:
    url = f"{STUDENT_URL}/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    r = await client.post(url, json=payload)
    r.raise_for_status()
    data = r.json()
    return data.get("response","")

async def speak(text: str):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(text.encode("utf-8"), (TTS_HOST, TTS_PORT))
    sock.close()

@app.post("/ask")
async def ask(payload: Dict[str, Any] = Body(...)):
    text = payload.get("text","").strip()
    if not text:
        return {"error":"empty input"}
    route = await ollama_generate(
        f"Route the user text to a skill label and args.\nTEXT: {text}\nFormat: JSON with fields 'skill' and 'args'.",
        MODEL_NAME
    )
    try:
        route_obj = json.loads(route)
    except Exception:
        route_obj = {"skill":"chat","args":{"text":text}}
    skill = route_obj.get("skill","chat")
    args = route_obj.get("args",{"text": text})

    if skill == "volume.up":
        await speak("Volume up")
        return {"ok":True,"skill":skill}
    elif skill == "volume.down":
        await speak("Volume down")
        return {"ok":True,"skill":skill}
    elif skill == "airgap.on":
        await speak("Air gap engaged.")
        return {"ok":True,"skill":skill}
    else:
        reply = await ollama_generate(
            f"You are a friendly droid head. Answer briefly.\nUser: {text}\nAssistant:",
            "qwen2.5:7b-instruct"
        )
        await speak(reply)
        return {"ok":True,"skill":"chat","reply":reply}

@app.get("/healthz")
async def healthz():
    return {"status":"ok"}
