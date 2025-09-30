#!/usr/bin/env python3
import argparse, json, collections

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred", required=True, help="router predictions JSONL")
    ap.add_argument("--gold", help="optional gold labels JSONL with fields text,skill")
    args = ap.parse_args()

    preds = [json.loads(l) for l in open(args.pred)]
    if args.gold:
        golds = {x["text"]: x for x in map(json.loads, open(args.gold))}
        total = 0
        correct = 0
        conf = collections.Counter()
        for p in preds:
            g = golds.get(p["text"])
            if not g: continue
            total += 1
            if g["skill"] == p["skill"]:
                correct += 1
            conf[(g["skill"], p["skill"])] += 1
        print(f"Accuracy: {correct}/{total} = {correct/total if total else 0:.3f}")
        print("Confusion (gold→pred):")
        for (g,p), c in conf.most_common():
            print(f"{g:12s} -> {p:12s}: {c}")
    else:
        from collections import Counter
        c = Counter(p["skill"] for p in preds)
        print("Pred counts by skill:", dict(c))

if __name__ == "__main__":
    main()
