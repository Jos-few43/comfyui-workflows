# Storage Guide for ComfyUI Models

## 💾 Your Current Situation

**Available Space**: 184 GB
**Already Used**: ~6 GB (PyTorch + ComfyUI)
**Verdict**: ✅ **NO EXTERNAL SSD NEEDED!**

---

## 📊 Model Sizes Reference

### Stable Diffusion Models

| Model Type | Size | Purpose | Quantity Needed |
|------------|------|---------|-----------------|
| **SD 1.5 Checkpoint** | 2-4 GB | Main model | 1-3 to start |
| **SD 1.5 Inpainting** | 4 GB | Inpainting specific | 1 optional |
| **SDXL Checkpoint** | 6-7 GB | High quality (heavy) | Not recommended for 6GB GPU |
| **VAE** | 330 MB | Quality enhancer | 1-2 |
| **LoRA** | 50-200 MB | Style/subject addon | 5-20 |
| **ControlNet** | 1.5 GB | Precise control | 2-5 |
| **Embedding** | 5-50 KB | Text concepts | 10-50 |

### Training Data

| Type | Size | Notes |
|------|------|-------|
| **Training Images** | 5-20 GB | Depends on quantity/resolution |
| **Trained LoRAs** | 50-200 MB each | Output from training |

---

## 🎯 Recommended Storage Plans

### Plan A: Minimal (Start Today)
**Total: ~10 GB**
- 1 SD 1.5 checkpoint (4 GB)
- 1 VAE (330 MB)
- PyTorch environment (5.7 GB - already installed)
- Working space (1 GB)

**Remaining**: 174 GB ✓

### Plan B: Standard Pipeline (Recommended)
**Total: ~30 GB**
- 3 SD 1.5 checkpoints (8-12 GB)
- 2 ControlNets (3 GB)
- 10 LoRAs (1 GB)
- 2 VAEs (600 MB)
- Training datasets (10 GB)
- PyTorch environment (5.7 GB)
- Working space (2 GB)

**Remaining**: 154 GB ✓

### Plan C: Power User
**Total: ~70 GB**
- 10 checkpoints (30-40 GB)
- 5 ControlNets (7.5 GB)
- 30 LoRAs (3-5 GB)
- Training datasets (20 GB)
- PyTorch environment (5.7 GB)
- Working space (5 GB)

**Remaining**: 114 GB ✓

---

## 📥 Where to Get Models

### Hugging Face (Official)
**Best for**: Base models, official releases
**Download method**:
```bash
~/Projects/comfy/download-hf-models.sh
```

**Models available**:
- SD 1.5 Base (4 GB)
- SD 1.5 Inpainting (4 GB)
- VAE (330 MB)
- ControlNets (1.5 GB each)

### Civitai (Community)
**Best for**: Fine-tuned models, LoRAs, specialized models
**URL**: https://civitai.com/
**Popular models**:
- Realistic Vision V5.1 (2 GB)
- DreamShaper (2 GB)
- Thousands of LoRAs (50-200 MB each)

**Download method**: Manual (browser download)

---

## 💡 Storage Best Practices

### 1. Start Small
- Download 1 checkpoint to test
- Add more as you learn what you need
- Don't hoard models you won't use

### 2. Organize Models
```bash
~/Projects/comfy/ComfyUI/models/
├── checkpoints/          # Main SD models (2-7GB each)
│   ├── sd-v1-5.safetensors
│   ├── realistic-vision.safetensors
│   └── inpainting.ckpt
├── vae/                  # VAE files (~330MB)
│   └── vae-ft-mse.safetensors
├── loras/                # LoRA files (50-200MB)
│   ├── your-trained-lora.safetensors
│   ├── style-1.safetensors
│   └── style-2.safetensors
├── controlnet/           # ControlNet models (~1.5GB)
│   ├── control_inpaint.pth
│   └── control_canny.pth
└── embeddings/           # Text embeddings (5-50KB)
    └── concept.pt
```

### 3. Clean Up Regularly
```bash
# Check model sizes
du -sh ~/Projects/comfy/ComfyUI/models/*

# Remove unused models
rm ~/Projects/comfy/ComfyUI/models/checkpoints/unused-model.safetensors

# Clear output folder
rm ~/Projects/comfy/ComfyUI/output/*.png
```

### 4. Training Data Management
```bash
# Keep training data separate
~/Projects/comfy/training/datasets/

# After training, archive to external drive
tar -czf dataset1.tar.gz ~/Projects/comfy/training/datasets/dataset1/
# Move to external storage

# Keep only the trained LoRA
cp trained-lora.safetensors ~/Projects/comfy/ComfyUI/models/loras/
```

---

## 🔍 Monitoring Storage

### Check total usage:
```bash
du -sh ~/Projects/comfy/
```

### Check by category:
```bash
du -sh ~/Projects/comfy/ComfyUI/models/*
```

### Check free space:
```bash
df -h ~/Projects/comfy/
```

### Find large files:
```bash
find ~/Projects/comfy -type f -size +1G -exec ls -lh {} \;
```

---

## 🚨 When You MIGHT Need External Storage

### Consider external SSD if:
- ❌ You collect 20+ different checkpoints (60+ GB)
- ❌ You work with SDXL exclusively (7 GB per model)
- ❌ You train multiple large models (datasets 50+ GB)
- ❌ You need <50GB free space for other projects

### You're fine with internal storage if:
- ✅ You use 3-5 main checkpoints (your case)
- ✅ You focus on SD 1.5 models (smaller)
- ✅ You have 150+ GB free (your case - 184GB!)
- ✅ You archive training data after use

---

## 💾 External SSD Setup (Optional)

If you ever DO want to use external storage:

### 1. Mount External Drive
```bash
# Find device
lsblk

# Mount (example: /dev/sdb1)
sudo mkdir -p /mnt/comfy-models
sudo mount /dev/sdb1 /mnt/comfy-models
```

### 2. Move Models
```bash
# Move existing models
mv ~/Projects/comfy/ComfyUI/models/* /mnt/comfy-models/

# Create symlink
ln -s /mnt/comfy-models ~/Projects/comfy/ComfyUI/models
```

### 3. Configure ComfyUI
Edit: `~/Projects/comfy/ComfyUI/extra_model_paths.yaml`
```yaml
comfyui:
    base_path: /mnt/comfy-models/
    checkpoints: checkpoints/
    vae: vae/
    loras: loras/
```

---

## 📊 Quick Reference

| Scenario | Storage Needed | Your Available | Status |
|----------|----------------|----------------|--------|
| Just starting | ~10 GB | 184 GB | ✅ Perfect |
| Full pipeline | ~30 GB | 184 GB | ✅ Perfect |
| Power user | ~70 GB | 184 GB | ✅ Perfect |
| Model hoarder | 100+ GB | 184 GB | ✅ Still okay |
| Everything | 200+ GB | 184 GB | ⚠️ Might be tight |

---

## 🎯 Recommendation for You

**Proceed with internal storage!**

You have **184 GB free** which is:
- ✅ Enough for 40+ SD 1.5 models
- ✅ Enough for extensive training
- ✅ Enough for all workflows
- ✅ Room to grow

**Start downloading models now:**
```bash
# For Hugging Face models:
~/Projects/comfy/download-hf-models.sh

# Or manually from Civitai:
# Visit https://civitai.com/
# Download to ~/Projects/comfy/ComfyUI/models/checkpoints/
```

**Monitor as you go:**
```bash
# Check usage anytime:
df -h ~/Projects/comfy/
du -sh ~/Projects/comfy/ComfyUI/models/
```

---

## 💡 Bottom Line

**You don't need an external SSD!**

Your 184 GB is plenty for:
- Learning and experimenting
- Building full img2img pipeline
- Training custom LoRAs
- Collecting favorite models

Start downloading and let's build your pipeline! 🚀
