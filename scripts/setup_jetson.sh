#!/usr/bin/env bash
set -euo pipefail
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit docker.io docker-compose-plugin
sudo nvidia-ctk runtime configure --runtime=docker || true
sudo systemctl restart docker
