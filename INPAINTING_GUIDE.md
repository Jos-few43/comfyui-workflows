# ComfyUI Inpainting & Photo-to-Photo Pipeline Guide

## 🎯 Overview

This guide covers:
1. **Inpainting**: Removing/replacing objects in images
2. **Img2Img (Photo-to-Photo)**: Transforming existing photos
3. **Training Custom Models**: Creating your own specialized models
4. **ControlNet**: Precise control over generation

## 📥 Required Models

### Essential Models to Download

#### 1. Base Model (Choose ONE to start):
**For 6GB VRAM - SD 1.5 (Recommended):**
- **Realistic Vision V5.1** (Best for photo-realistic)
  - URL: https://civitai.com/models/4201/realistic-vision-v51
  - Download: `realisticVisionV51_v51VAE.safetensors`
  - Size: ~2GB
  - Put in: `~/Projects/comfy/ComfyUI/models/checkpoints/`

**Alternative - SD 1.5 Inpainting Specialized:**
- **SD 1.5 Inpainting Model**
  - URL: https://huggingface.co/runwayml/stable-diffusion-inpainting
  - File: `sd-v1-5-inpainting.ckpt`
  - Put in: `~/Projects/comfy/ComfyUI/models/checkpoints/`

#### 2. VAE (Image Quality Enhancer):
- **vae-ft-mse-840000-ema-pruned**
  - URL: https://huggingface.co/stabilityai/sd-vae-ft-mse-original
  - Put in: `~/Projects/comfy/ComfyUI/models/vae/`
  - Size: ~330MB

#### 3. ControlNet (Optional but Recommended):
- **ControlNet Inpaint**
  - URL: https://huggingface.co/lllyasviel/control_v11p_sd15_inpaint
  - File: `control_v11p_sd15_inpaint.pth`
  - Put in: `~/Projects/comfy/ComfyUI/models/controlnet/`

### Quick Download Commands:
```bash
cd ~/Projects/comfy/ComfyUI/models/checkpoints/

# Download SD 1.5 Inpainting (via wget or curl)
# You'll need to get the direct link from the websites above
# Or use the ComfyUI Manager to install models directly
```

## 🔧 Setup Instructions

### Step 1: Install ComfyUI Manager (Highly Recommended)
```bash
cd ~/Projects/comfy/ComfyUI/custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
```

### Step 2: Create Input Directory for Your Photos
```bash
mkdir -p ~/Projects/comfy/ComfyUI/input/my-photos
```

### Step 3: Put Your Test Images There
```bash
# Copy some test images
cp /path/to/your/photos/*.jpg ~/Projects/comfy/ComfyUI/input/my-photos/
```

## 🎨 Inpainting Workflow

### Basic Inpainting Process:
1. **Load your image** in ComfyUI
2. **Create a mask** (black = keep, white = inpaint)
3. **Set prompts** (what to generate in masked area)
4. **Generate** with inpainting model

### Creating a Mask:
You have several options:
1. **External tools**: GIMP, Photoshop (save as PNG)
2. **ComfyUI built-in**: Use the mask editor in the UI
3. **AI-based masking**: Use SAM (Segment Anything Model)

## 📸 Photo-to-Photo (Img2Img) Workflow

### What is Img2Img?
- Takes an existing image as input
- Transforms it based on a prompt
- Keeps overall composition but changes style/details

### Key Parameters:
- **Denoise Strength** (0.0-1.0):
  - 0.1-0.3: Minor changes, keep most details
  - 0.4-0.6: Moderate transformation
  - 0.7-1.0: Major changes, less resemblance to original

### Example Use Cases:
- Photo → Painting
- Day → Night
- Summer → Winter
- Add/remove objects
- Change artistic style

## 🏋️ Training Your Own Model

### Option 1: LoRA Training (Recommended for Beginners)
LoRAs are small, efficient add-ons to existing models.

#### What You Need:
- **20-100 training images** (similar style/subject)
- **8GB+ system RAM** (you have 15GB ✓)
- **Captions for each image** (text descriptions)

#### Training Tools:
1. **Kohya_ss** (Most popular, GUI-based)
   ```bash
   cd ~/Projects
   git clone https://github.com/bmaltais/kohya_ss.git
   cd kohya_ss
   ./setup.sh
   ```

2. **SimpleTuner** (Newer, easier)
   ```bash
   pip install SimpleTuner
   ```

#### Training Steps:
1. **Prepare dataset**:
   ```
   training-data/
   ├── img1.jpg
   ├── img1.txt  (caption)
   ├── img2.jpg
   ├── img2.txt
   ...
   ```

2. **Configure training**:
   - Resolution: 512x512 (SD 1.5) or 768x768
   - Steps: 1000-3000 (start small)
   - Learning rate: 1e-4 (default)
   - Batch size: 1-2 (for 6GB VRAM)

3. **Start training**:
   ```bash
   # Will take several hours
   # Monitor GPU with: watch -n 1 nvidia-smi
   ```

4. **Test LoRA**:
   - Put `.safetensors` file in `models/loras/`
   - Use in ComfyUI with LoRA Loader node

### Option 2: Fine-tuning Full Model (Advanced)
- Requires more VRAM (may need `--lowvram`)
- Longer training time
- More powerful but harder to manage

#### Tools:
- **EveryDream2** - Full model training
- **Dreambooth** - Subject-specific training

## 🎮 ComfyUI Workflows for You

### Workflow 1: Basic Img2Img
```
Load Image → VAE Encode → KSampler (denoise: 0.5) → VAE Decode → Save Image
              ↑                    ↑
         Load VAE          Load Checkpoint + CLIP Text Encode (prompt)
```

### Workflow 2: Inpainting
```
Load Image → Inpaint Model Conditioning → KSampler → VAE Decode → Save
Load Mask ↗                                ↑
                               Load Inpaint Checkpoint
```

### Workflow 3: ControlNet Inpaint (Most Control)
```
Load Image → ControlNet Apply → KSampler → VAE Decode → Save
Load Mask ↗        ↑
            ControlNet Loader (inpaint)
```

## 💾 Directory Structure

```
~/Projects/comfy/
├── ComfyUI/
│   ├── models/
│   │   ├── checkpoints/       ← Main SD models (2-7GB each)
│   │   ├── vae/               ← VAE models (~330MB)
│   │   ├── loras/             ← Your trained LoRAs (50-200MB)
│   │   ├── controlnet/        ← ControlNet models (~1.5GB)
│   │   └── inpaint/           ← Inpainting-specific models
│   ├── input/
│   │   └── my-photos/         ← Your source photos
│   └── output/                ← Generated images
└── training-data/             ← Your training images + captions
    ├── dataset1/
    │   ├── img1.jpg
    │   ├── img1.txt
    │   ...
```

## 🚀 Quick Start Guide

### 1. Start ComfyUI
```bash
~/Projects/comfy/start-comfyui.sh
# Add --lowvram for 6GB GPU
```

### 2. Open Browser
Navigate to: http://127.0.0.1:8188

### 3. Load Default Workflow
- Click "Load" button
- Choose "default" workflow

### 4. For Img2Img:
- Add "Load Image" node
- Connect to VAE Encode
- Set denoise strength in KSampler
- Generate!

### 5. For Inpainting:
- Add "Load Image" node
- Add "Load Image (as Mask)" node
- Use inpainting model
- Generate!

## 📚 Learning Resources

### Tutorials:
- **ComfyUI Basics**: https://github.com/comfyanonymous/ComfyUI/wiki
- **Inpainting Guide**: Search "ComfyUI inpainting workflow"
- **LoRA Training**: https://github.com/bmaltais/kohya_ss

### Communities:
- **r/StableDiffusion** (Reddit)
- **ComfyUI Discord**
- **Civitai** (model sharing)

### Model Sources:
- **Civitai**: https://civitai.com/ (community models)
- **Hugging Face**: https://huggingface.co/ (official models)

## 🎯 Recommended Training Path

### Week 1: Learn ComfyUI
1. Install base model (Realistic Vision)
2. Practice img2img with your photos
3. Experiment with different denoise strengths
4. Learn prompt engineering

### Week 2: Advanced Techniques
1. Install ControlNet
2. Practice inpainting
3. Create masks in GIMP/Photoshop
4. Combine multiple techniques

### Week 3: Start Training
1. Collect 30-50 similar images
2. Write captions (or use BLIP for auto-captioning)
3. Set up Kohya_ss
4. Train your first LoRA (start small: 500 steps)

### Week 4: Refine & Iterate
1. Test your LoRA
2. Adjust training parameters
3. Create more specialized LoRAs
4. Build custom workflows

## ⚡ Performance Tips for 6GB GPU

### For Training:
```bash
# Use gradient checkpointing
# Set batch size = 1
# Use mixed precision (fp16)
# Train at 512x512 resolution
```

### For Generation:
```bash
# Always use --lowvram flag
python main.py --lowvram

# Or if still running out of memory:
python main.py --novram

# Use smaller resolutions (512x512)
# Avoid SDXL models (too heavy for 6GB)
# Close other GPU applications
```

## 🔧 Troubleshooting

### "Out of VRAM" during training:
- Reduce batch size to 1
- Lower resolution to 512x512
- Enable gradient checkpointing
- Use --lowvram flag

### "Out of VRAM" during generation:
- Use --lowvram or --novram
- Reduce image resolution
- Use SD 1.5 instead of SDXL
- Clear VRAM: restart ComfyUI

### Slow training:
- Normal for 6GB GPU
- Expect 1-3 hours for 1000 steps
- Train overnight for best results
- Monitor with `nvidia-smi`

## 📊 Realistic Expectations for Your GPU

### What Works Well:
- ✅ SD 1.5 img2img (smooth)
- ✅ Inpainting 512x512 (works great)
- ✅ LoRA training (slower but possible)
- ✅ ControlNet with SD 1.5
- ✅ Batch processing with --lowvram

### What's Challenging:
- ⚠️ SDXL (possible with --novram, but slow)
- ⚠️ Large batch sizes (stick to 1-2)
- ⚠️ Very high resolutions (stay at 512-768)
- ⚠️ Multiple ControlNets at once

## 🎉 Next Steps

1. **Start ComfyUI** and explore the UI
2. **Download a base model** (Realistic Vision recommended)
3. **Try img2img** with your own photos
4. **Experiment with inpainting** on test images
5. **Collect training data** for your custom model
6. **Train your first LoRA** when ready

Need help with any of these steps? I can guide you through each one!
