#!/usr/bin/env bash
set -euo pipefail

STACK_NAME="crispy-biscuits-ai"

echo ">>> Bringing up Crispy Biscuits AI stack (n8n + GPT-OSS)..."

# Optional: prune stopped containers for this project
echo ">>> Cleaning old containers (if any)..."
docker compose -p "$STACK_NAME" down || true

echo ">>> Starting fresh stack..."
docker compose -p "$STACK_NAME" up -d

echo ">>> Current status:"
docker compose -p "$STACK_NAME" ps

echo ">>> Services:"
echo "  - n8n UI:       http://localhost:5678"
echo "  - GPT-OSS API:  http://localhost:8080"
echo ""
echo "Reminder: n8n basic auth is set to 'logan' / 'change-this' in docker-compose.yml."