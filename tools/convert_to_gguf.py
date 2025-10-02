#!/usr/bin/env python3
# Print instructions for GGUF conversion with llama.cpp
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--in", dest="inp", required=True)
ap.add_argument("--out", dest="out", required=True)
args = ap.parse_args()

print("Build llama.cpp with Metal on macOS (see its README). Then run the converter, e.g.:")
print("  python3 ./llama.cpp/convert.py --vocab-dir {inp} --outfile {out}".format(inp=args.inp, out=args.out))
print("Finally quantize (optional) and place GGUF at ./gguf/router-student.gguf for Ollama.")
