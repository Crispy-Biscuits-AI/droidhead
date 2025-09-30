#!/usr/bin/env python3
import argparse, json, requests

SYS = "You are the teacher model. Answer helpfully and concisely in the droidhead voice."

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/teacher.json")
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    url = cfg["openai_compatible_url"]
    api_key = cfg.get("api_key","")
    model = cfg.get("model","gpt-oss-120b")

    headers = {"Content-Type":"application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    prompts = [l.strip() for l in open(args.input) if l.strip()]
    with open(args.out,"w") as out:
        for p in prompts:
            payload = {
                "model": model,
                "messages": [
                    {"role":"system","content":SYS},
                    {"role":"user","content":p}
                ],
                "temperature": 0.2
            }
            r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=300)
            r.raise_for_status()
            ans = r.json()["choices"][0]["message"]["content"]
            out.write(json.dumps({"prompt": p, "response": ans}) + "\n")
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
