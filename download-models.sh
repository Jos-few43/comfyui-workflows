#!/bin/bash
# Helper script to download recommended models for inpainting

set -e

MODELS_DIR="$HOME/Projects/comfy/ComfyUI/models"

echo "========================================="
echo "  ComfyUI Model Downloader"
echo "========================================="
echo ""

# Function to download with progress
download_model() {
    local url=$1
    local output=$2
    local name=$3

    if [ -f "$output" ]; then
        echo "  ✓ $name already exists, skipping"
        return
    fi

    echo "  Downloading $name..."
    wget -c "$url" -O "$output" --progress=bar:force 2>&1 | tail -n 1
    echo "  ✓ Downloaded $name"
}

echo "This script will help you download essential models."
echo "Models are large (2-7GB each), so this may take a while."
echo ""
echo "Available models:"
echo "  1. SD 1.5 Base (runwayml) - ~4GB"
echo "  2. SD 1.5 Inpainting - ~4GB"
echo "  3. Realistic Vision V5.1 - ~2GB (from Civitai)"
echo "  4. VAE (vae-ft-mse) - ~330MB"
echo ""

# VAE (smaller, download first)
echo "Downloading VAE..."
mkdir -p "$MODELS_DIR/vae"
VAE_URL="https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors"
download_model "$VAE_URL" "$MODELS_DIR/vae/vae-ft-mse-840000-ema-pruned.safetensors" "VAE"
echo ""

echo "========================================="
echo "  Manual Download Required"
echo "========================================="
echo ""
echo "For the main models, please download manually from:"
echo ""
echo "1. SD 1.5 Inpainting:"
echo "   URL: https://huggingface.co/runwayml/stable-diffusion-inpainting"
echo "   File: sd-v1-5-inpainting.ckpt"
echo "   Save to: $MODELS_DIR/checkpoints/"
echo ""
echo "2. Realistic Vision V5.1 (Recommended):"
echo "   URL: https://civitai.com/models/4201/realistic-vision-v51"
echo "   File: realisticVisionV51_v51VAE.safetensors"
echo "   Save to: $MODELS_DIR/checkpoints/"
echo ""
echo "3. Or use ComfyUI Manager:"
echo "   - Start ComfyUI"
echo "   - Click 'Manager' button"
echo "   - Go to 'Model Manager'"
echo "   - Search and install models"
echo ""

echo "========================================="
echo "  Directory Structure Created"
echo "========================================="
echo ""
ls -lh "$MODELS_DIR"/*/
echo ""
echo "Next steps:"
echo "  1. Download models to the directories shown above"
echo "  2. Start ComfyUI: ~/Projects/comfy/start-comfyui.sh"
echo "  3. Load your first workflow!"
echo ""
