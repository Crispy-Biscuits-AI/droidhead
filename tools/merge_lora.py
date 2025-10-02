#!/usr/bin/env python3
# Merge LoRA into base weights using transformers+peft (CPU ok)
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--lora", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(args.base, use_fast=True)
    base = AutoModelForCausalLM.from_pretrained(args.base)
    peft = PeftModel.from_pretrained(base, args.lora)
    merged = peft.merge_and_unload()
    merged.save_pretrained(args.out)
    tok.save_pretrained(args.out)
    print("Merged weights written to", args.out)

if __name__ == "__main__":
    main()
