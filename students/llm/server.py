from fastapi import FastAPI, Request
import os, httpx
app = FastAPI(title="LLM Student (OpenAI proxy)")
BASE = os.getenv("OAI_BASE_URL", "http://host.docker.internal:11434/v1").rstrip("/")
KEY = os.getenv("OAI_API_KEY", "")
HEADERS = {"Authorization": f"Bearer {KEY}"} if KEY else {}
@app.get("/health") async def health(): return {"ok": True, "base": BASE}
@app.post("/v1/chat/completions")
async def chat_completions(req: Request):
    body = await req.json()
    async with httpx.AsyncClient(timeout=None) as client:
        r = await client.post(f"{BASE}/chat/completions", json=body, headers=HEADERS)
        return r.json()
