# app/main.py
import os
from typing import List, Literal, Optional

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Environment configuration
GPT_OSS_BASE_URL = os.getenv("GPT_OSS_BASE_URL", "http://gpt-oss:8080/v1")
TEACHER_MODEL_NAME = os.getenv("TEACHER_MODEL_NAME", "gpt-oss:20b")

app = FastAPI(title="Teacher Service", version="0.1.0")


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 512


class ChatResponse(BaseModel):
    content: str


@app.get("/health")
async def health():
    """
    Simple health check endpoint.
    """
    return {"status": "ok", "service": "teacher", "model": TEACHER_MODEL_NAME}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Proxy chat endpoint that forwards requests to GPT-OSS in an
    OpenAI-style /v1/chat/completions format.
    """
    payload = {
        "model": TEACHER_MODEL_NAME,
        "messages": [
            {"role": m.role, "content": m.content}
            for m in req.messages
        ],
        "temperature": req.temperature,
        "max_tokens": req.max_tokens,
    }

    url = f"{GPT_OSS_BASE_URL}/chat/completions"

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            resp = await client.post(url, json=payload)
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Error contacting GPT-OSS backend: {e}",
            )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail={
                "message": "GPT-OSS backend error",
                "body": resp.text,
            },
        )

    data = resp.json()

    # Expecting OpenAI-style response:
    # { "choices": [ { "message": { "content": "..." } } ], ... }
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected GPT-OSS response format: {e}",
        )

    return ChatResponse(content=content)

