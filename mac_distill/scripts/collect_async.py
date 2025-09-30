#!/usr/bin/env python3
import argparse, asyncio, json, aiohttp

SYS_ROUTE = (
"You are an expert router for an embedded assistant called droidhead.\n"
"Given a user TEXT, return a strict JSON with fields:\n"
"- 'skill' in ['chat','volume.up','volume.down','airgap.on','airgap.off','status','network.on','network.off']\n"
"- 'args' as an object (can be empty).\n"
"Return only JSON, no commentary."
)

SYS_STYLE = "You are the teacher model. Answer helpfully and concisely in the droidhead voice."

async def call_openai(url, api_key, model, sys_prompt, user_content, session, temperature=0.1):
    headers = {"Content-Type":"application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    payload = {
        "model": model,
        "messages": [
            {"role":"system","content":sys_prompt},
            {"role":"user","content":user_content}
        ],
        "temperature": temperature
    }
    async with session.post(url, headers=headers, json=payload, timeout=300) as resp:
        resp.raise_for_status()
        data = await resp.json()
        return data["choices"][0]["message"]["content"]

async def collect_routes(cfg, seeds, out_path, concurrency=8):
    url, api_key, model = cfg["openai_compatible_url"], cfg.get("api_key",""), cfg.get("model","gpt-oss-120b")
    sem = asyncio.Semaphore(concurrency)
    async with aiohttp.ClientSession() as session, open(out_path, "w") as out:
        async def worker(text):
            async with sem:
                content = await call_openai(url, api_key, model, SYS_ROUTE, f"TEXT: {text}", session, temperature=0.05)
                try:
                    obj = json.loads(content)
                except Exception:
                    obj = {"skill":"chat","args":{"text":text}}
                rec = {"text": text, "skill": obj.get("skill","chat"), "args": obj.get("args",{})}
                out.write(json.dumps(rec)+"\n")
        await asyncio.gather(*[worker(s) for s in seeds])

async def collect_style(cfg, prompts, out_path, concurrency=8):
    url, api_key, model = cfg["openai_compatible_url"], cfg.get("api_key",""), cfg.get("model","gpt-oss-120b")
    sem = asyncio.Semaphore(concurrency)
    async with aiohttp.ClientSession() as session, open(out_path, "w") as out:
        async def worker(p):
            async with sem:
                ans = await call_openai(url, api_key, model, SYS_STYLE, p, session, temperature=0.2)
                out.write(json.dumps({"prompt": p, "response": ans}) + "\n")
        await asyncio.gather(*[worker(p) for p in prompts])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/teacher.json")
    ap.add_argument("--input", required=True, help="seed file, one per line")
    ap.add_argument("--out", required=True, help="output JSONL")
    ap.add_argument("--mode", choices=["routes","style"], default="routes")
    ap.add_argument("--concurrency", type=int, default=8)
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    seeds = [l.strip() for l in open(args.input) if l.strip()]

    if args.mode == "routes":
        asyncio.run(collect_routes(cfg, seeds, args.out, concurrency=args.concurrency))
    else:
        asyncio.run(collect_style(cfg, seeds, args.out, concurrency=args.concurrency))

if __name__ == "__main__":
    main()
