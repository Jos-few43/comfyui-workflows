#!/bin/bash
# Quick start script for ComfyUI

COMFY_DIR="$HOME/Projects/comfy/ComfyUI"

echo "Starting ComfyUI..."
cd "$COMFY_DIR"

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup first: ~/Projects/comfy/setup-comfyui.sh"
    exit 1
fi

# Activate venv and start
source venv/bin/activate
echo "✓ Virtual environment activated"
echo "✓ Python version: $(python --version)"
echo "✓ Starting ComfyUI with --lowvram (recommended for 6GB GPU)..."
echo ""

# Start with lowvram flag for 6GB GPU
# --listen 0.0.0.0 allows access from network (iPhone, Tailscale)
# --enable-cors-header allows cross-origin requests (needed for Comfy Portal)
python main.py --lowvram --listen 0.0.0.0 --enable-cors-header "*" "$@"
