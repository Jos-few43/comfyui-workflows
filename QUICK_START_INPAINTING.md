# 🎨 Quick Start: Inpainting & Photo-to-Photo in ComfyUI

## 🚀 5-Minute Quick Start

### Step 1: Start ComfyUI (NOW!)
```bash
~/Projects/comfy/start-comfyui.sh
```

Open browser: http://127.0.0.1:8188

### Step 2: You're Already Set Up!
Your installation includes:
- ✅ Python 3.10 + PyTorch 2.6.0
- ✅ CUDA support for your RTX 3060
- ✅ All ComfyUI dependencies
- ✅ Directory structure ready

### Step 3: What You Need Next
**Essential** (to start generating):
- 1 checkpoint model (~2-4GB)
- Put in: `~/Projects/comfy/ComfyUI/models/checkpoints/`

**Download options:**
```bash
# Option 1: Run the helper script
~/Projects/comfy/download-models.sh

# Option 2: Manual download
# Visit: https://civitai.com/models/4201/realistic-vision-v51
# Download: realisticVisionV51_v51VAE.safetensors
# Save to: ~/Projects/comfy/ComfyUI/models/checkpoints/
```

## 📸 Your First Photo-to-Photo

### Simple Img2Img Workflow:

1. **Put a photo in input directory:**
   ```bash
   cp /path/to/your/photo.jpg ~/Projects/comfy/ComfyUI/input/
   ```

2. **In ComfyUI web interface:**
   - Right-click → Add Node → "Image" → "Load Image"
   - Select your photo
   - Connect to existing workflow
   - Change the prompt
   - Set denoise strength (try 0.5)
   - Click "Queue Prompt"

3. **Results in:**
   ```bash
   ~/Projects/comfy/ComfyUI/output/
   ```

### Denoise Strength Guide:
- **0.1-0.2**: Tiny changes (color correction, minor touch-ups)
- **0.3-0.4**: Light transformation (add elements, style tweaks)
- **0.5-0.6**: Moderate transformation (good starting point!)
- **0.7-0.8**: Major transformation (change scene significantly)
- **0.9-1.0**: Almost completely new image

## 🖌️ Your First Inpainting

### What is Inpainting?
Remove/replace specific parts of an image:
- Remove objects (person, car, building)
- Replace elements (change sky, add objects)
- Fix/restore damaged areas

### Quick Inpainting Process:

1. **Create a mask** (white = inpaint this area):
   - Use GIMP, Photoshop, or Paint.NET
   - Paint WHITE where you want to change
   - Save as PNG

2. **In ComfyUI:**
   - Add "Load Image" node (your photo)
   - Add "Load Image (as Mask)" node (your mask)
   - Use inpainting checkpoint
   - Prompt describes what to generate in masked area
   - Generate!

### Example: Remove a Person
- Photo: `scene-with-person.jpg`
- Mask: Paint white over the person
- Prompt: "empty street, no people, daytime"
- Result: Person removed, background filled in naturally

## 🏋️ Training Your Own Model (LoRA)

### Why Train a LoRA?
- Specialize in YOUR style/subject
- Small file size (50-200MB vs 2-4GB)
- Works with any base model
- Fast training on your GPU

### What You Need:
- **20-100 photos** of similar style/subject
- **Captions** for each image
- **2-4 hours** training time

### Setup Training Environment:
```bash
# Run once to set everything up
~/Projects/comfy/setup-training.sh
```

### Prepare Your Dataset:
```bash
# Create dataset folder
mkdir ~/Projects/comfy/training/datasets/my-style

# Put images there
cp your-photos/*.jpg ~/Projects/comfy/training/datasets/my-style/

# Create caption files (one per image)
# img001.jpg → img001.txt
# Content: "a photo of a sunset over mountains, golden hour, dramatic clouds"
```

### Start Training (GUI):
```bash
~/Projects/comfy/start-training.sh
```

Opens GUI at: http://127.0.0.1:7860

### Training Settings for Your RTX 3060:
- **Resolution**: 512x512
- **Batch Size**: 1
- **Steps**: 1000-2000 (start small!)
- **Learning Rate**: 1e-4
- **Network Rank**: 32
- **Mixed Precision**: fp16
- **Optimizer**: AdamW8bit

### After Training:
```bash
# LoRA file will be in:
~/Projects/comfy/training/outputs/

# Copy to ComfyUI:
cp ~/Projects/comfy/training/outputs/my-lora.safetensors \
   ~/Projects/comfy/ComfyUI/models/loras/
```

## 🎯 Realistic Project Example

### Project: "Convert Day Photos to Night"

**Goal**: Train a LoRA to transform daytime photos into nighttime scenes

**Dataset:**
- Collect 30-50 photos of same location
- Day versions AND night versions
- Or use day photos + prompt for night style

**Training:**
```bash
# Setup
mkdir ~/Projects/comfy/training/datasets/day-to-night
cp day-night-photos/* ~/Projects/comfy/training/datasets/day-to-night/

# Caption examples:
# day001.txt: "daytime city street, bright sunlight, blue sky"
# night001.txt: "nighttime city street, street lights, dark sky, neon signs"

# Train for 1500 steps
# Time: ~2 hours on RTX 3060
```

**Usage:**
- Load day photo in ComfyUI
- Use your day-to-night LoRA
- Prompt: "nighttime, street lights, dark atmosphere"
- Denoise: 0.6
- Generate!

## 📊 Directory Overview

```bash
~/Projects/comfy/
├── ComfyUI/
│   ├── models/
│   │   ├── checkpoints/      ← Download models here (2-4GB each)
│   │   ├── vae/               ← VAE files (~330MB)
│   │   ├── loras/             ← Your trained LoRAs (50-200MB)
│   │   └── controlnet/        ← ControlNet models (optional)
│   ├── input/                 ← Put your photos here
│   └── output/                ← Generated images appear here
├── training/
│   ├── datasets/              ← Your training images + captions
│   ├── outputs/               ← Trained LoRAs
│   └── kohya_ss/              ← Training GUI
├── start-comfyui.sh           ← Start ComfyUI
├── start-training.sh          ← Start training GUI
├── setup-training.sh          ← Setup training (run once)
└── INPAINTING_GUIDE.md        ← Full detailed guide
```

## ⚡ Performance Tips for Your 6GB GPU

### For Generation (ComfyUI):
```bash
# Always start with lowvram
python main.py --lowvram

# If still OOM:
python main.py --novram

# Use these settings:
- Resolution: 512x512 (not 768 or 1024)
- Batch size: 1
- Close other GPU apps
```

### For Training:
```bash
# These settings work best:
- Batch size: 1
- Resolution: 512x512
- Mixed precision: fp16
- Gradient checkpointing: enabled
- Cache latents: true

# Expect:
- ~500-800 steps/hour
- 1-3 hours for 1000-2000 steps
```

### Monitor GPU:
```bash
# In another terminal:
watch -n 1 nvidia-smi

# You should see:
- GPU utilization: 95-100%
- Memory usage: ~5.5GB / 5.8GB (almost full is good!)
- Temperature: <85°C (safe)
```

## 🎨 Workflow Templates

### Template 1: Photo Enhancement
```
Input: Your photo
Denoise: 0.2-0.3
Prompt: "high quality, detailed, professional photography"
Result: Enhanced, cleaned up version
```

### Template 2: Style Transfer
```
Input: Regular photo
Denoise: 0.6-0.7
Prompt: "oil painting style, impressionist, vibrant colors"
Result: Photo rendered as painting
```

### Template 3: Object Removal (Inpainting)
```
Input: Photo + Mask (white over object to remove)
Prompt: Background description
Result: Object removed, background filled naturally
```

### Template 4: Season Change
```
Input: Summer photo
Denoise: 0.6
Prompt: "winter scene, snow covered, cold atmosphere"
Result: Same location in winter
```

## 🆘 Common Issues & Solutions

### "No checkpoint models found"
```bash
# Download a model first!
~/Projects/comfy/download-models.sh
# Or manually from civitai.com
```

### "CUDA out of memory"
```bash
# Restart with more aggressive memory management:
python main.py --novram

# Or reduce image size in workflow
```

### "Training is very slow"
- Normal for 6GB GPU
- Expect 500-800 steps/hour
- Run overnight for best results
- Don't interrupt! Save checkpoints every 250 steps

### "Generated images look nothing like input"
- Decrease denoise strength (try 0.3-0.5)
- Use more specific prompts
- Check if you're using img2img correctly

## 🎯 Your Learning Path

### Week 1: Basics
- [ ] Download a checkpoint model
- [ ] Generate your first image (text2img)
- [ ] Try img2img with your own photo
- [ ] Experiment with denoise strengths

### Week 2: Advanced
- [ ] Try inpainting (remove an object)
- [ ] Create custom masks in GIMP
- [ ] Experiment with different prompts
- [ ] Learn prompt engineering

### Week 3: Training
- [ ] Collect 30 training images
- [ ] Write captions for each
- [ ] Train your first LoRA (500 steps)
- [ ] Test and iterate

### Week 4: Master
- [ ] Train specialized LoRAs
- [ ] Build custom workflows
- [ ] Combine techniques (img2img + LoRA + inpainting)
- [ ] Share your results!

## 🎉 You're Ready!

**Everything is set up:**
- ✅ ComfyUI working
- ✅ GPU detected
- ✅ Scripts ready
- ✅ Guides written

**Next immediate steps:**
1. Download a model (Realistic Vision recommended)
2. Start ComfyUI: `~/Projects/comfy/start-comfyui.sh`
3. Try your first generation!

**For training:**
1. Collect your training images
2. Run: `~/Projects/comfy/setup-training.sh`
3. Start training GUI: `~/Projects/comfy/start-training.sh`

Need help with any step? I can guide you through it!
