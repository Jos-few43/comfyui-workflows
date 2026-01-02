#!/bin/bash
# Download models from Hugging Face for img2img/inpainting

set -e

MODELS_DIR="$HOME/Projects/comfy/ComfyUI/models"

echo "========================================="
echo "  Hugging Face Model Downloader"
echo "========================================="
echo ""

# Check disk space
FREE_SPACE=$(df -h ~/Projects/comfy | tail -1 | awk '{print $4}')
echo "Available disk space: $FREE_SPACE"
echo ""

# Install huggingface-cli if not present
echo "Checking for huggingface-cli..."
cd ~/Projects/comfy/ComfyUI
source venv/bin/activate

if ! command -v huggingface-cli &> /dev/null; then
    echo "Installing huggingface-hub..."
    pip install huggingface-hub -q
    echo "✓ Installed"
fi
echo ""

echo "Available models for download:"
echo ""
echo "1. SD 1.5 Base (4 GB) - General purpose img2img"
echo "2. SD 1.5 Inpainting (4 GB) - Specialized for inpainting"
echo "3. VAE (330 MB) - Image quality enhancer"
echo ""

# Function to download from HF
download_hf_model() {
    local repo=$1
    local filename=$2
    local dest=$3

    echo "Downloading $filename from $repo..."
    huggingface-cli download "$repo" "$filename" \
        --local-dir "$dest" \
        --local-dir-use-symlinks False
}

# Menu
read -p "Which model to download? (1-3, or 'all'): " choice

case $choice in
    1)
        echo "Downloading SD 1.5 Base..."
        mkdir -p "$MODELS_DIR/checkpoints"
        download_hf_model "runwayml/stable-diffusion-v1-5" \
            "v1-5-pruned-emaonly.safetensors" \
            "$MODELS_DIR/checkpoints"
        ;;
    2)
        echo "Downloading SD 1.5 Inpainting..."
        mkdir -p "$MODELS_DIR/checkpoints"
        download_hf_model "runwayml/stable-diffusion-inpainting" \
            "sd-v1-5-inpainting.ckpt" \
            "$MODELS_DIR/checkpoints"
        ;;
    3)
        echo "Downloading VAE..."
        mkdir -p "$MODELS_DIR/vae"
        download_hf_model "stabilityai/sd-vae-ft-mse-original" \
            "vae-ft-mse-840000-ema-pruned.safetensors" \
            "$MODELS_DIR/vae"
        ;;
    all)
        echo "Downloading all models (will take a while)..."
        mkdir -p "$MODELS_DIR/checkpoints" "$MODELS_DIR/vae"

        echo "1/3: SD 1.5 Base..."
        download_hf_model "runwayml/stable-diffusion-v1-5" \
            "v1-5-pruned-emaonly.safetensors" \
            "$MODELS_DIR/checkpoints"

        echo "2/3: SD 1.5 Inpainting..."
        download_hf_model "runwayml/stable-diffusion-inpainting" \
            "sd-v1-5-inpainting.ckpt" \
            "$MODELS_DIR/checkpoints"

        echo "3/3: VAE..."
        download_hf_model "stabilityai/sd-vae-ft-mse-original" \
            "vae-ft-mse-840000-ema-pruned.safetensors" \
            "$MODELS_DIR/vae"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "  ✓ Download Complete!"
echo "========================================="
echo ""
echo "Downloaded models:"
ls -lh "$MODELS_DIR"/checkpoints/*.{ckpt,safetensors} 2>/dev/null || echo "No checkpoints yet"
ls -lh "$MODELS_DIR"/vae/*.safetensors 2>/dev/null || echo "No VAE yet"
echo ""
echo "Disk usage:"
du -sh "$MODELS_DIR"/*
echo ""
echo "Start ComfyUI: ~/Projects/comfy/start-comfyui.sh"
