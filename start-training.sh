#!/bin/bash
# Quick start script for Kohya_ss training GUI

TRAIN_DIR="$HOME/Projects/comfy/training/kohya_ss"

if [ ! -d "$TRAIN_DIR" ]; then
    echo "❌ Training environment not set up!"
    echo "Please run: ~/Projects/comfy/setup-training.sh"
    exit 1
fi

echo "Starting Kohya_ss training GUI..."
cd "$TRAIN_DIR"
source venv/bin/activate

echo "✓ Virtual environment activated"
echo "✓ Starting GUI on http://127.0.0.1:7860"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python gui.py --listen 127.0.0.1 --server_port 7860
