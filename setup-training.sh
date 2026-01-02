#!/bin/bash
# Setup LoRA training environment with Kohya_ss

set -e

echo "========================================="
echo "  ComfyUI LoRA Training Setup"
echo "========================================="
echo ""

TRAIN_DIR="$HOME/Projects/comfy/training"

echo "Step 1: Creating training directory structure..."
mkdir -p "$TRAIN_DIR"/{kohya_ss,datasets,outputs,configs}
mkdir -p ~/Projects/comfy/ComfyUI/models/loras
echo "  ✓ Directories created"
echo ""

echo "Step 2: Checking system requirements..."
echo "  GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader)"
echo "  VRAM: $(nvidia-smi --query-gpu=memory.total --format=csv,noheader)"
echo "  Python: $(python3 --version)"
echo ""

echo "Step 3: Installing Kohya_ss (GUI-based LoRA trainer)..."
cd "$TRAIN_DIR"
if [ ! -d "kohya_ss" ]; then
    echo "  Cloning Kohya_ss..."
    git clone https://github.com/bmaltais/kohya_ss.git
    cd kohya_ss
    echo "  ✓ Kohya_ss cloned"
else
    echo "  ✓ Kohya_ss already exists"
    cd kohya_ss
fi
echo ""

echo "Step 4: Setting up Kohya_ss virtual environment..."
if [ ! -d "venv" ]; then
    echo "  Creating venv with Python 3.10..."
    /usr/bin/python3.10 -m venv venv
    source venv/bin/activate

    echo "  Installing dependencies..."
    pip install --upgrade pip
    pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu121
    pip install -r requirements.txt
    echo "  ✓ Dependencies installed"
else
    echo "  ✓ Virtual environment already exists"
fi
echo ""

echo "Step 5: Creating example dataset structure..."
mkdir -p "$TRAIN_DIR/datasets/example-dataset"
cat > "$TRAIN_DIR/datasets/example-dataset/README.md" << 'EOF'
# Training Dataset Structure

Place your training images here with corresponding caption files:

```
example-dataset/
├── img001.jpg (or .png)
├── img001.txt (caption: "a photo of...")
├── img002.jpg
├── img002.txt
...
```

## Caption Guidelines:
- Describe what's in the image
- Be specific but concise
- Include style/lighting/composition details
- Example: "a photo of a red car parked on a city street at sunset"

## Image Guidelines:
- Resolution: 512x512 or 768x768 (will be resized)
- Format: JPG or PNG
- Quantity: 20-100 images minimum
- Quality: High quality, clear images
- Consistency: Similar style/subject matter
EOF
echo "  ✓ Example dataset structure created"
echo ""

echo "Step 6: Creating training config template..."
cat > "$TRAIN_DIR/configs/example-config.json" << 'EOF'
{
  "model": {
    "pretrained_model_name_or_path": "runwayml/stable-diffusion-v1-5",
    "v2": false,
    "v_parameterization": false
  },
  "train": {
    "train_data_dir": "/home/yish/Projects/comfy/training/datasets/example-dataset",
    "output_dir": "/home/yish/Projects/comfy/training/outputs",
    "output_name": "my-first-lora",
    "max_train_steps": 1000,
    "learning_rate": 1e-4,
    "lr_scheduler": "cosine",
    "network_dim": 32,
    "network_alpha": 16,
    "resolution": "512,512",
    "train_batch_size": 1,
    "mixed_precision": "fp16",
    "save_every_n_epochs": 1,
    "keep_tokens": 0,
    "clip_skip": 2,
    "prior_loss_weight": 1.0,
    "max_token_length": 225,
    "caption_extension": ".txt",
    "cache_latents": true,
    "optimizer_type": "AdamW8bit"
  }
}
EOF
echo "  ✓ Training config template created"
echo ""

echo "========================================="
echo "  ✓ Training Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Prepare your dataset:"
echo "   cd $TRAIN_DIR/datasets"
echo "   mkdir my-dataset"
echo "   # Copy images and create caption files"
echo ""
echo "2. Start Kohya_ss GUI:"
echo "   cd $TRAIN_DIR/kohya_ss"
echo "   source venv/bin/activate"
echo "   python gui.py --listen 127.0.0.1 --server_port 7860"
echo "   # Then open: http://127.0.0.1:7860"
echo ""
echo "3. Or use the quick start script:"
echo "   ~/Projects/comfy/start-training.sh"
echo ""
echo "Documentation:"
echo "  - Training guide: ~/Projects/comfy/INPAINTING_GUIDE.md"
echo "  - Example config: $TRAIN_DIR/configs/example-config.json"
echo "  - Dataset template: $TRAIN_DIR/datasets/example-dataset/"
echo ""
