from fastapi import FastAPI, Body
from pydantic import BaseModel
import httpx, os, yaml, json, time
import paho.mqtt.client as mqtt

class AskIn(BaseModel):
    input: str
    session_id: str | None = None
    stream: bool = False

app = FastAPI(title="DroidHead Teacher", version="0.1.0")

with open(os.getenv("STUDENTS_CONFIG", "/app/app/config.yaml"), "r", encoding="utf-8") as f:
    STUDENTS = yaml.safe_load(f)

MQTT_HOST = os.getenv("MQTT_HOST", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"droidhead-teacher-{int(time.time())}")
mqttc.connect(MQTT_HOST, MQTT_PORT, 60)
mqttc.loop_start()

@app.get("/health")
async def health():
    return {"ok": True, "time": time.time()}

@app.get("/students")
async def students():
    return STUDENTS

@app.post("/ask")
async def ask(payload: AskIn):
    llm = STUDENTS["llm"]["endpoint"].rstrip("/")
    model = os.getenv(STUDENTS["llm"].get("model_env", "OAI_MODEL"), "gpt-3.5-turbo")
    body = {"model": model, "messages": [{"role": "user", "content": payload.input}], "temperature": 0.5}
    mqttc.publish("droidhead/teacher/ask", json.dumps({"input": payload.input, "session": payload.session_id or ""}), qos=0)
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(f"{llm}/chat/completions", json=body, headers={"authorization": f"Bearer {os.getenv('OAI_API_KEY','')}"})
        r.raise_for_status()
        data = r.json()
    text = data["choices"][0]["message"]["content"]
    mqttc.publish("droidhead/teacher/answer", json.dumps({"output": text, "session": payload.session_id or ""}), qos=0)
    return {"output": text, "raw": data}

@app.post("/asr")
async def transcribe(audio_url: str = Body(..., embed=True)):
    asr = STUDENTS["asr"]["endpoint"].rstrip("/")
    async with httpx.AsyncClient(timeout=None) as client:
        r = await client.post(f"{asr}/transcribe", json={"audio_url": audio_url})
        r.raise_for_status()
        return r.json()

@app.post("/tts")
async def speak(text: str = Body(..., embed=True)):
    tts = STUDENTS["tts"]["endpoint"].rstrip("/")
    async with httpx.AsyncClient(timeout=None) as client:
        r = await client.post(f"{tts}/speak", json={"text": text})
        r.raise_for_status()
        return r.json()

@app.get("/battery")
async def battery():
    periph = STUDENTS["periph"]["endpoint"].rstrip("/")
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{periph}/battery")
        r.raise_for_status()
        return r.json()
