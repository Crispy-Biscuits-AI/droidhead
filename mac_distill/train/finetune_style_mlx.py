#!/usr/bin/env python3
import argparse
from datasets import load_dataset
from mlx_lm import load
from mlx_lm.tuner import lora_finetune, save_lora, prepare_sft_dataset

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--train_jsonl", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--batch", type=int, default=4)
    args = ap.parse_args()

    ds = load_dataset("json", data_files=args.train_jsonl, split="train")
    model, tokenizer = load(args.base)
    train_data = prepare_sft_dataset(tokenizer, ds, input_key="prompt", target_key="response")

    lora_cfg = dict(r=16, alpha=32, dropout=0.05, target_modules=["q_proj","v_proj","k_proj","o_proj"])
    lora_finetune(model, tokenizer, train_data,
                  output_dir=args.out,
                  lora_config=lora_cfg,
                  epochs=args.epochs,
                  learning_rate=args.lr,
                  batch_size=args.batch)
    save_lora(model, args.out)
    print("Saved LoRA to", args.out)

if __name__ == "__main__":
    main()
