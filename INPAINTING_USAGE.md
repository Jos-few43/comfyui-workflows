# 🎨 Inpainting Workflow - Quick Usage Guide

## ✅ Your Workflow is Ready!

File: `inpainting-workflow.json`
Model: `realisticVisionV60B1_v51HyperVAE.safetensors`

## 🚀 How to Use

### Step 1: Prepare Your Image and Mask

**Option A: Use ComfyUI's Built-in Mask Editor**
1. Place your image in `ComfyUI/input/`
2. Load it in ComfyUI interface
3. Use the built-in mask painter (easiest!)

**Option B: Create Mask Externally**
1. Open your image in GIMP, Photoshop, or Paint.NET
2. Create a new layer
3. Paint **WHITE** on areas you want to inpaint/change
4. Paint **BLACK** on areas to keep unchanged
5. Save the mask as PNG

Example:
```
ComfyUI/input/photo.png       ← Your original image
ComfyUI/input/photo_mask.png  ← White = inpaint, Black = keep
```

### Step 2: Start ComfyUI

```bash
./start-comfyui.sh
```

Open browser: http://127.0.0.1:8188

### Step 3: Load the Workflow

1. In ComfyUI interface, click **"Load"** button
2. Select `inpainting-workflow.json`
3. The workflow will appear with all nodes connected

### Step 4: Configure the Workflow

**LoadImage Node:**
- Click and select your image from `ComfyUI/input/`
- The mask will be loaded automatically (if using built-in editor)
- Or select your mask file separately

**Positive Prompt (CLIPTextEncode Node #3):**
- Default: `"photorealistic, high quality, detailed, natural lighting..."`
- **Replace with what you want in the masked area**
- Examples:
  - Remove person: `"empty street, natural background, no people"`
  - Add object: `"red sports car, parked, realistic, detailed"`
  - Change background: `"sunset sky, golden hour, clouds"`

**Negative Prompt (CLIPTextEncode Node #4):**
- Keep as: `"blurry, deformed, ugly, low quality, artifacts..."`
- Add unwanted elements specific to your case

**KSampler Settings:**
- **Steps:** 30 (good default, increase to 40-50 for better quality)
- **CFG:** 6.0 (increase to 7-8 for stronger prompt adherence)
- **Sampler:** dpmpp_2m (good default)
- **Denoise:** 0.8 (how much to change)
  - 0.5-0.6: Minor changes, preserve most details
  - 0.7-0.8: Moderate changes (recommended)
  - 0.9-1.0: Major changes, almost complete regeneration

**VAEEncodeForInpaint:**
- **grow_mask_by:** 8 (pixels to expand mask - helps blend edges)
  - Increase to 12-16 for better blending
  - Decrease to 4-6 for precise edits

### Step 5: Generate!

1. Click **"Queue Prompt"** button
2. Watch the progress in the interface
3. Results appear in **PreviewImage** node
4. Saved to `ComfyUI/output/inpainted_*.png`

## 📊 Performance on RTX 3060

- **Resolution:** 512x512 optimal
- **Generation time:** ~10-20 seconds per image
- **VRAM usage:** ~4-5GB
- **Batch size:** Keep at 1

If you get OOM errors, start ComfyUI with:
```bash
python ComfyUI/main.py --lowvram
```

## 🎯 Common Use Cases

### Remove an Object
```
Mask: Paint white over the object
Positive: "natural background, seamless, no artifacts"
Denoise: 0.8
```

### Change a Person's Clothing
```
Mask: Paint white over clothing area
Positive: "blue jeans and red t-shirt, casual wear, realistic fabric"
Denoise: 0.7
```

### Replace Background
```
Mask: Paint white over entire background
Positive: "beach sunset, ocean waves, golden hour, realistic"
Denoise: 0.9
```

### Fix/Restore Damaged Area
```
Mask: Paint white over damaged area
Positive: Match the style of surrounding area
Denoise: 0.6-0.7
```

### Add Object to Scene
```
Mask: Paint white where you want the object
Positive: "wooden chair, realistic lighting, shadows, detailed"
Denoise: 0.8
```

## 🔧 Troubleshooting

### "Image doesn't change much"
- Increase denoise strength to 0.9
- Make prompt more specific
- Increase CFG scale to 7-8
- Check mask is white (not gray)

### "Changes look unrealistic/blended poorly"
- Increase `grow_mask_by` to 12-16
- Decrease denoise to 0.7
- Add "seamless, natural lighting" to positive prompt
- Increase steps to 40-50

### "Too much of the image changed"
- Decrease denoise to 0.5-0.6
- Check mask - ensure only target area is white
- Verify mask is loaded correctly

### "Colors don't match"
- Add "matching colors, consistent lighting" to prompt
- Use img2img first to match color palette
- Decrease denoise to 0.6

## 💡 Pro Tips

1. **Start conservative:** Use denoise 0.6-0.7 first, then increase
2. **Feather your masks:** Soft edges blend better than hard edges
3. **Match the style:** Describe lighting, time of day, weather in prompt
4. **Iterate:** Generate 3-4 variants, pick the best
5. **Combine techniques:** Use inpainting + img2img for best results

## 📝 Workflow Node Explanation

```
LoadImage (Node 1)
  ↓ [image + mask]
  ↓
VAEEncodeForInpaint (Node 5) ← The key inpainting node!
  ↓ [latent]
  ↓
KSampler (Node 6) ← Uses prompts to generate
  ↓ [latent]
  ↓
VAEDecode (Node 7) ← Converts back to image
  ↓ [image]
  ↓
SaveImage (Node 8) + PreviewImage (Node 9)
```

The magic happens in **VAEEncodeForInpaint** which:
- Takes your image + mask
- Preserves non-masked areas
- Prepares masked areas for regeneration

## 🎨 Next Steps

1. **Try it now!** Place a test image and generate
2. **Experiment** with different denoise values
3. **Create multiple masks** for the same image
4. **Combine with LoRAs** for specific styles
5. **Batch process** using the batch workflow

Happy inpainting! 🎉
