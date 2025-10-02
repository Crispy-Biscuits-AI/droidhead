from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import httpx, os
TEACHER = os.getenv("TEACHER_URL","http://teacher:8000")
app = FastAPI(title="DroidHead Web UI")
INDEX = """<!doctype html><html><head><meta charset='utf-8'><title>DroidHead</title>
<meta name='viewport' content='width=device-width, initial-scale=1'/>
<style>body{font-family:system-ui,sans-serif;max-width:720px;margin:2rem auto;padding:0 1rem}
textarea{width:100%;height:120px}pre{background:#111;color:#eee;padding:1rem;border-radius:8px;overflow:auto}
button{padding:.6rem 1rem;border-radius:10px;border:1px solid #333;cursor:pointer}.row{display:flex;gap:10px}</style>
</head><body><h2>🤖 DroidHead</h2>
<section><h3>Ask</h3><textarea id='input' placeholder='Say hello...'></textarea>
<div class='row'><button onclick='ask()'>Ask</button><button onclick='battery()'>Battery</button></div>
<h3>Answer</h3><pre id='out'></pre></section>
<script>
async function ask(){const input=document.getElementById('input').value;
 const r=await fetch('/api/ask',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({input})});
 document.getElementById('out').textContent=JSON.stringify(await r.json(),null,2)}
async function battery(){const r=await fetch('/api/battery');
 document.getElementById('out').textContent=JSON.stringify(await r.json(),null,2)}
</script></body></html>"""
@app.get('/', response_class=HTMLResponse)
async def index(): return HTMLResponse(INDEX)
@app.post('/api/ask')
async def api_ask(req: Request):
    body = await req.json()
    async with httpx.AsyncClient(timeout=None) as client:
        r = await client.post(f"{TEACHER}/ask", json={"input": body.get("input","")})
        return JSONResponse(r.json())
@app.get('/api/battery')
async def api_battery():
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{TEACHER}/battery")
        return JSONResponse(r.json())
