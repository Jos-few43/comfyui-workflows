#!/bin/bash
# ComfyUI Setup Script - Fix Python version and dependencies

set -e  # Exit on error

echo "========================================="
echo "  ComfyUI Setup & Repair Script"
echo "========================================="
echo ""

COMFY_DIR="$HOME/Projects/comfy/ComfyUI"
cd "$COMFY_DIR"

echo "Step 1: Checking Python versions..."
echo "  Current Python: $(python --version)"
echo "  Python 3.10: $(/usr/bin/python3.10 --version)"
echo ""

echo "Step 2: Creating virtual environment with Python 3.10..."
if [ -d "venv" ]; then
    echo "  ⚠ Virtual environment already exists"
    read -p "  Remove and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "  Removing old venv..."
        rm -rf venv
    else
        echo "  Keeping existing venv"
    fi
fi

if [ ! -d "venv" ]; then
    echo "  Creating venv with Python 3.10..."
    /usr/bin/python3.10 -m venv venv
    echo "  ✓ Virtual environment created!"
fi
echo ""

echo "Step 3: Activating virtual environment..."
source venv/bin/activate
echo "  Active Python: $(which python)"
echo "  Active Python version: $(python --version)"
echo ""

echo "Step 4: Upgrading pip..."
python -m pip install --upgrade pip
echo ""

echo "Step 5: Installing PyTorch..."
echo "  This may take a few minutes..."
# Install PyTorch for CUDA 12.x (adjust if you have different CUDA or want CPU-only)
if command -v nvidia-smi &> /dev/null; then
    echo "  NVIDIA GPU detected, installing CUDA version..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
else
    echo "  No NVIDIA GPU detected, installing CPU version..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
fi
echo ""

echo "Step 6: Installing ComfyUI requirements..."
pip install -r requirements.txt
echo ""

echo "Step 7: Verifying installation..."
python -c "import torch; print(f'✓ PyTorch {torch.__version__} installed successfully')"
python -c "import yaml; print('✓ PyYAML installed successfully')"
python -c "import numpy; print(f'✓ NumPy {numpy.__version__} installed successfully')"
echo ""

echo "========================================="
echo "  ✓ ComfyUI Setup Complete!"
echo "========================================="
echo ""
echo "To start ComfyUI:"
echo "  1. cd $COMFY_DIR"
echo "  2. source venv/bin/activate"
echo "  3. python main.py"
echo ""
echo "Or use the start script: ~/Projects/comfy/start-comfyui.sh"
echo ""
