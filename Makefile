SHELL := /bin/bash

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

rebuild:
	docker compose build --no-cache

ps:
	docker compose ps
