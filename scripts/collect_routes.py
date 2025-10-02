#!/usr/bin/env python3
import argparse, json, time, requests

SYS = (
"You are an expert router for an embedded assistant called droidhead.\n"
"Given a user TEXT, return a strict JSON with fields:\n"
"- 'skill' in ['chat','volume.up','volume.down','airgap.on','airgap.off','status','network.on','network.off']\n"
"- 'args' as an object (can be empty).\n"
"Return only JSON, no commentary."
)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/teacher.json")
    ap.add_argument("--input", required=True, help="seed text file, one per line")
    ap.add_argument("--out", required=True, help="output JSONL")
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    url = cfg["openai_compatible_url"]
    api_key = cfg.get("api_key","")
    model = cfg.get("model","gpt-oss-20b")

    headers = {"Content-Type":"application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    seeds = [l.strip() for l in open(args.input) if l.strip()]
    with open(args.out, "w") as out:
        for text in seeds:
            payload = {
                "model": model,
                "messages": [
                    {"role":"system","content":SYS},
                    {"role":"user","content":f"TEXT: {text}"}
                ],
                "temperature": 0.1
            }
            r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"]
            try:
                obj = json.loads(content)
            except Exception:
                obj = {"skill":"chat","args":{"text":text}}
            rec = {"text": text, "skill": obj.get("skill","chat"), "args": obj.get("args",{})}
            out.write(json.dumps(rec)+"\n")
            time.sleep(0.05)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
