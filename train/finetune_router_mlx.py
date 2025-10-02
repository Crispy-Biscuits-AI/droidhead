#!/usr/bin/env python3
# Minimal MLX LoRA fine-tune for router using mlx-lm
import argparse, json
from datasets import load_dataset
from mlx_lm import load
from mlx_lm.tuner import lora_finetune, save_lora, prepare_text_dataset

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="HF model id (TinyLlama/Llama-3.2-3B, etc.)")
    ap.add_argument("--train_jsonl", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--batch", type=int, default=8)
    args = ap.parse_args()

    ds = load_dataset("json", data_files=args.train_jsonl, split="train")
    def fmt(example):
        prompt = f"Route the user text to a skill label and args.\nTEXT: {example['text']}\nFormat: JSON with fields 'skill' and 'args'."
        target = json.dumps({"skill": example['skill'], "args": example.get('args',{})}, ensure_ascii=False)
        return {"text": prompt + "\n" + target}
    ds = ds.map(fmt)
    model, tokenizer = load(args.base)
    train_data = prepare_text_dataset(tokenizer, ds["text"])

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
