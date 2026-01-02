#!/bin/bash
# Quick helper to open download page

echo "========================================="
echo "  Download Realistic Vision V5.1"
echo "========================================="
echo ""
echo "Opening Civitai download page in your browser..."
echo ""
echo "Steps:"
echo "1. Browser will open to the download page"
echo "2. Click the green 'Download' button"
echo "3. Save the file (it will go to ~/Downloads/)"
echo "4. Run this script again to move it to ComfyUI"
echo ""

# Check if file is already in Downloads
if [ -f ~/Downloads/realisticVisionV51_v51VAE.safetensors ]; then
    echo "✓ Found file in Downloads!"
    echo "Moving to ComfyUI..."
    mv ~/Downloads/realisticVisionV51_v51VAE.safetensors ~/Projects/comfy/ComfyUI/models/checkpoints/
    echo "✓ Moved successfully!"
    echo ""
    ls -lh ~/Projects/comfy/ComfyUI/models/checkpoints/realisticVisionV51_v51VAE.safetensors
    echo ""
    echo "🎉 Ready to use! Start ComfyUI:"
    echo "   ~/Projects/comfy/start-comfyui.sh"
    exit 0
fi

# Check if file is already in ComfyUI
if [ -f ~/Projects/comfy/ComfyUI/models/checkpoints/realisticVisionV51_v51VAE.safetensors ]; then
    echo "✓ Model already in ComfyUI!"
    ls -lh ~/Projects/comfy/ComfyUI/models/checkpoints/realisticVisionV51_v51VAE.safetensors
    echo ""
    echo "🎉 Ready to use! Start ComfyUI:"
    echo "   ~/Projects/comfy/start-comfyui.sh"
    exit 0
fi

# Open browser
echo "Opening browser..."
xdg-open "https://civitai.com/models/4201/realistic-vision-v51" 2>/dev/null || \
firefox "https://civitai.com/models/4201/realistic-vision-v51" 2>/dev/null || \
echo "Please manually open: https://civitai.com/models/4201/realistic-vision-v51"

echo ""
echo "After download completes, run this script again:"
echo "   ~/Projects/comfy/download-realistic-vision-NOW.sh"
echo ""
echo "Or manually move the file:"
echo "   mv ~/Downloads/realisticVisionV51_v51VAE.safetensors \\"
echo "      ~/Projects/comfy/ComfyUI/models/checkpoints/"
