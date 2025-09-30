#!/usr/bin/env python3
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--in", dest="inp", required=True)
ap.add_argument("--out", dest="out", required=True)
args = ap.parse_args()
print("Build llama.cpp with Metal on macOS (see its README). Then run the converter, e.g.:")
print(f"  python3 ./llama.cpp/convert.py --vocab-dir {args.inp} --outfile {args.out}")
print("Quantize if desired. Place GGUF at mac_distill/gguf/router-student.gguf for Ollama.")
