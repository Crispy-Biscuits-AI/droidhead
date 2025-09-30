# Makefile — Mac mini M4 (teacher-student-LAN) — All-in-one

PY=python

ROUTER_SEED=prompts/router_seed.txt
STYLE_SEED=prompts/style_seed.txt

ROUTER_OUT=data/routes.jsonl
STYLE_OUT=data/style.jsonl

ROUTER_BASE=TinyLlama/TinyLlama-1.1B-Chat-v1.0
ROUTER_LORA=models/router_student_mlx
ROUTER_MERGED=models/router_merged
GGUF=gguf/router-student.gguf

DROIDHOST=droidhead.local
DROIDPATH=~/models/gguf
REMOTE_OLLAMA_CREATE="ollama create router-student -f ~/ollama/RouterStudent.Modelfile"

.PHONY: all collect collect_async train merge gguf eval deploy remote_create

all: collect train merge gguf

collect:
	$(PY) scripts/collect_routes.py --config config/teacher.json --input $(ROUTER_SEED) --out $(ROUTER_OUT)
	$(PY) scripts/collect_style.py  --config config/teacher.json --input $(STYLE_SEED)  --out $(STYLE_OUT)

collect_async:
	$(PY) scripts/collect_async.py --mode routes --config config/teacher.json --input $(ROUTER_SEED) --out $(ROUTER_OUT) --concurrency 8
	$(PY) scripts/collect_async.py --mode style  --config config/teacher.json --input $(STYLE_SEED)  --out $(STYLE_OUT)  --concurrency 8

train:
	$(PY) train/finetune_router_mlx.py --base $(ROUTER_BASE) --train_jsonl $(ROUTER_OUT) --out $(ROUTER_LORA) --epochs 2 --lr 5e-5 --batch 8

merge:
	$(PY) tools/merge_lora.py --base $(ROUTER_BASE) --lora $(ROUTER_LORA) --out $(ROUTER_MERGED)

gguf:
	$(PY) tools/convert_to_gguf.py --in $(ROUTER_MERGED) --out $(GGUF)

eval:
	$(PY) scripts/eval_router.py --pred $(ROUTER_OUT)

deploy:
	scp $(GGUF) $(DROIDHOST):$(DROIDPATH)/router-student.gguf
	scp -r ../droidhead_runtime/ollama $(DROIDHOST):~/ollama
	@echo "GGUF copied to $(DROIDHOST). Next step on droidhead-LAN:"
	@echo "  ollama create router-student -f ~/ollama/RouterStudent.Modelfile"

remote_create:
	ssh $(DROIDHOST) $(REMOTE_OLLAMA_CREATE)
