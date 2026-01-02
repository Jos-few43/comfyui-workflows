# Download Realistic Vision V5.1

## 🎯 Best Model for Photo-to-Photo Work

**Realistic Vision V5.1** is perfect for:
- Photo-realistic img2img transformations
- High quality results
- Works great on 6GB GPU
- Built-in VAE (no separate download needed)

---

## 📥 Download Instructions

### Step 1: Visit Civitai
**URL**: https://civitai.com/models/4201/realistic-vision-v51

### Step 2: Click Download Button
Look for the green "Download" button on the page.

**Model to download**: `realisticVisionV51_v51VAE.safetensors`
- **Size**: ~2.0 GB
- **Version**: V5.1 (includes VAE)

### Step 3: Save to ComfyUI
**Save location**:
```bash
~/Projects/comfy/ComfyUI/models/checkpoints/realisticVisionV51_v51VAE.safetensors
```

**Full path**:
```
/home/yish/Projects/comfy/ComfyUI/models/checkpoints/realisticVisionV51_v51VAE.safetensors
```

---

## 🖥️ Download Methods

### Method A: Browser Download (Easiest)
1. Open browser
2. Go to: https://civitai.com/models/4201/realistic-vision-v51
3. Click green "Download" button
4. Save to Downloads folder
5. Move to ComfyUI:
   ```bash
   mv ~/Downloads/realisticVisionV51_v51VAE.safetensors ~/Projects/comfy/ComfyUI/models/checkpoints/
   ```

### Method B: wget (If you have direct link)
```bash
cd ~/Projects/comfy/ComfyUI/models/checkpoints/
# You'll need the direct download URL from Civitai
# wget <direct-url>
```

### Method C: aria2c (Faster, resumable)
```bash
sudo pacman -S aria2
cd ~/Projects/comfy/ComfyUI/models/checkpoints/
# aria2c -x 16 <direct-url>
```

---

## ✅ Verify Download

After downloading, check it's there:
```bash
ls -lh ~/Projects/comfy/ComfyUI/models/checkpoints/
```

You should see:
```
realisticVisionV51_v51VAE.safetensors  (~2.0 GB)
```

---

## 🚀 After Download

### Start ComfyUI:
```bash
~/Projects/comfy/start-comfyui.sh
```

### In ComfyUI Web Interface:
1. Open: http://127.0.0.1:8188
2. Load default workflow
3. Click on "Load Checkpoint" node
4. Select: `realisticVisionV51_v51VAE.safetensors`
5. Enter your prompt
6. Click "Queue Prompt"
7. See the magic! ✨

---

## 🎨 Example Prompts for Realistic Vision

### Photo Enhancement:
```
Prompt: "professional photography, high quality, detailed, 8k, sharp focus"
Negative: "blurry, low quality, distorted"
```

### Portrait Enhancement:
```
Prompt: "professional portrait, soft lighting, detailed face, photorealistic"
Negative: "cartoon, anime, painting, illustration"
```

### Landscape:
```
Prompt: "beautiful landscape, golden hour, professional photography, HDR"
Negative: "oversaturated, artificial, fake"
```

---

## 💡 Settings for Your 6GB GPU

When using Realistic Vision:
- **Resolution**: 512x512 or 640x640 (start here)
- **Denoise** (for img2img): 0.5-0.6
- **Steps**: 20-30
- **CFG Scale**: 7-8
- **Sampler**: DPM++ 2M Karras (good default)

**Launch with**:
```bash
python main.py --lowvram
```

---

## 📊 File Size & Space

**Before download**:
- Free space: 184 GB

**After download**:
- Realistic Vision: 2.0 GB
- Free space: 182 GB
- Still plenty of room! ✓

---

## 🆘 Troubleshooting

### "Download requires login"
- Create free Civitai account
- Login before downloading
- No payment required!

### "File is incomplete"
- Check file size: should be ~2.0 GB
- If smaller, download was interrupted
- Try downloading again

### "Can't find model in ComfyUI"
- Check file location:
  ```bash
  ls ~/Projects/comfy/ComfyUI/models/checkpoints/
  ```
- Restart ComfyUI if it was running during download
- Refresh browser page

### "Out of memory"
- Use: `python main.py --lowvram`
- Or even: `python main.py --novram`
- Reduce resolution to 512x512

---

## 🎯 Alternative Models (If Civitai is slow)

If Civitai download is slow, you can also use:

### DreamShaper 8 (Similar quality)
- URL: https://civitai.com/models/4384/dreamshaper
- Size: ~2.0 GB
- Also photo-realistic

### SD 1.5 Base (From Hugging Face)
```bash
~/Projects/comfy/download-hf-models.sh
# Select option 1
```
- Size: 4.0 GB
- Official model, good baseline

---

## 🎉 You're Almost There!

After downloading Realistic Vision:
1. ✅ ComfyUI is installed and working
2. ✅ GPU is detected (RTX 3060)
3. ✅ Model will be ready
4. ✅ Ready to generate!

**Next**: Put a photo in `~/Projects/comfy/ComfyUI/input/` and try img2img!
