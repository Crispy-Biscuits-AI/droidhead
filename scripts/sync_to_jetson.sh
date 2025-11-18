#!/usr/bin/env bash
# Simple example script to sync prompts/system to a Jetson device.
# Edit DEVICE, PATHS, and auth to match your environment.

DEVICE=jetson-orin-nano.local
TARGET_DIR=/opt/j0n1

rsync -av prompts system "${DEVICE}:${TARGET_DIR}/"
