# 🤖 Auto-Mask Inpainting Workflow Guide

## What This Does

**Automatically detects and removes/replaces objects using AI** - no manual mask painting needed!

## Quick Start (3 Steps)

### 1. Load the Workflow

**In ComfyUI Web Interface:**
- Click **"Workflows"** button (top menu)
- Select **`auto-mask-inpainting-workflow.json`**
- Workflow will load with 13 connected nodes

### 2. Configure Detection

**Node 1: Load Your Image**
- Click "Choose File to Upload"
- Select image with object you want to remove/replace

**Node 4: Auto-Detect (MOST IMPORTANT!)**
- **prompt**: Change `"person"` to what you want to detect
  - Examples: `"car"`, `"dog"`, `"tree"`, `"background"`, `"face"`
  - Multiple objects: `"person . car . tree"`
- **threshold**: 0.3 (default is good, adjust if needed)
  - Lower (0.2) = detect more objects
  - Higher (0.4-0.5) = detect fewer, more confident objects

**Node 7: Positive Prompt**
- Describe what to generate in the detected area
- Default: `"empty background, natural scenery, seamless blend"`
- Examples:
  - Remove person: `"empty street, no people, natural background"`
  - Replace car: `"green grass, park, trees"`
  - Remove object: `"clean wall, seamless, matching texture"`

**Node 8: Negative Prompt**
- What to avoid generating
- Default includes: `"person, people, human, blurry, low quality"`
- Add what you DON'T want to see

### 3. Generate!

- Click **"Queue Prompt"**
- Watch the magic happen:
  1. GroundingDINO detects object
  2. SAM creates precise mask
  3. Preview shows mask (Node 5)
  4. AI inpaints the area
  5. Result appears (Node 13)

## First Run (Models Download)

**First time only - downloads ~1GB of models:**
- GroundingDINO_SwinT_OGC: ~694MB
- sam_vit_b: ~375MB
- Takes 5-10 minutes
- Saved to `ComfyUI/models/` for future use

**You'll see:**
```
Downloading GroundingDINO...
Downloading SAM model...
```

**After first run:** Generation takes 15-30 seconds per image

## Common Use Cases

### Remove a Person

**Node 4 Settings:**
```
prompt: "person"
threshold: 0.3
```

**Node 7 (Positive):**
```
"empty background, natural scenery, no people, seamless blend, photorealistic"
```

**Result:** Person removed, background filled naturally

### Remove Car from Photo

**Node 4:**
```
prompt: "car"
threshold: 0.3
```

**Node 7:**
```
"empty parking lot, asphalt, street markings, realistic lighting"
```

### Replace Background

**Node 4:**
```
prompt: "background"
threshold: 0.25
```

**Node 7:**
```
"beach sunset, ocean waves, golden hour, beautiful sky"
```

**Result:** Keeps subject, changes entire background

### Remove Multiple Objects

**Node 4:**
```
prompt: "person . car . bicycle"
threshold: 0.3
```

**Node 7:**
```
"clean street, empty sidewalk, no objects"
```

## Advanced Settings

### Node 10: KSampler

**steps**: 35 (default)
- More steps = higher quality but slower
- Try 40-50 for best quality

**cfg**: 7 (default)
- How closely to follow prompt
- Higher (8-9) = stronger prompt adherence
- Lower (5-6) = more creative freedom

**denoise**: 0.85 (default)
- How much to change masked area
- 0.7-0.8 = preserve some original details
- 0.85-0.95 = completely regenerate area
- 1.0 = maximum change

**sampler_name**: dpmpp_2m (default)
- Good default, works well for most cases
- Alternative: euler_a, dpm_2

### Node 9: VAEEncodeForInpaint

**grow_mask_by**: 12 (default)
- Expands mask edges for better blending
- Increase to 16-20 for softer transitions
- Decrease to 6-8 for precise edits

## Troubleshooting

### "Nothing Detected"

**Solutions:**
1. Lower threshold to 0.2 or 0.25
2. Try simpler prompts: `"person"` instead of `"person wearing hat"`
3. Check object is clearly visible in image
4. Try alternative descriptions: `"human"` instead of `"person"`

### "Detected Wrong Object"

**Solutions:**
1. Increase threshold to 0.4 or 0.5
2. Be more specific: `"red car"` instead of `"car"`
3. Preview mask (Node 5) to verify detection
4. Adjust and re-run until mask is correct

### "Inpainted Area Looks Bad"

**Solutions:**
1. Improve positive prompt - be specific about lighting, style, texture
2. Increase denoise to 0.9 or 0.95
3. Increase steps to 40-50
4. Increase grow_mask_by to 16-20 for better blending
5. Add to negative prompt what you see wrong

### "Out of Memory Error"

**Solutions:**
1. Already using sam_vit_b (smallest SAM model)
2. Reduce image size before uploading
3. Restart ComfyUI: `pkill -f "python main.py" && ./start-comfyui.sh`
4. Close other applications

### "Models Not Found"

**First Run:**
- Models auto-download on first use
- Wait for downloads to complete
- Check terminal output for progress

**If downloads fail:**
```bash
# Check models downloaded:
ls -lh ComfyUI/models/grounding-dino/
ls -lh ComfyUI/models/sams/

# Should see:
# grounding-dino/groundingdino_swint_ogc.pth
# sams/sam_vit_b_01ec64.pth
```

## Workflow Node Breakdown

```
1. LoadImage ──────┐
                   ├──> 4. GroundingDinoSAMSegment ──> 5. Preview Mask
2. GroundingDINO ──┤           ↓
3. SAM Model ──────┘           │ (mask)
                               ↓
                    9. VAEEncodeForInpaint
                               ↓
6. Checkpoint ──> 10. KSampler ──> 11. VAEDecode ──> 12. Save
   ↓                  ↑                               ↓
7. Positive Prompt ───┤                        13. Preview
8. Negative Prompt ───┘
```

## Tips for Best Results

1. **Preview the Mask First**
   - Always check Node 5 (Preview Mask)
   - Make sure detected area is correct
   - Adjust threshold if needed
   - Re-run detection before inpainting

2. **Be Specific in Prompts**
   - Good: `"sunny day, blue sky, green grass, park setting, natural lighting"`
   - Bad: `"background"`

3. **Match Original Style**
   - Look at original image lighting, time of day, weather
   - Include these in positive prompt
   - Example: `"overcast lighting, grey sky, rainy day, wet pavement"`

4. **Use Negative Prompts Effectively**
   - Include what you're removing: removed `"person"` → negative: `"person, people, human"`
   - Add common artifacts: `"blurry, distorted, deformed, unnatural, artifacts"`

5. **Iterate**
   - First attempt might not be perfect
   - Adjust prompts based on results
   - Try different denoise values
   - Generate 3-4 variations

## Performance Notes

**RTX 3060 (6GB VRAM):**
- ✓ Supports all features
- ✓ Using sam_vit_b (optimal for 6GB)
- ✓ --lowvram mode active
- Generation time: ~20-40 seconds per image
- First run: +5-10 min for model downloads

## Example Workflows

### Portrait Background Replacement

```
Node 4: prompt="background", threshold=0.25
Node 7: "professional studio backdrop, grey gradient, soft lighting, photography studio"
Node 8: "outdoor, nature, people, objects, cluttered"
Node 10: denoise=0.9
```

### Object Removal (Clean Plate)

```
Node 4: prompt="car . person . trash bin", threshold=0.3
Node 7: "empty clean street, asphalt, no objects, seamless continuation"
Node 8: "objects, people, vehicles, blur, artifacts"
Node 10: denoise=0.95
```

### Fashion/Clothing Swap

```
Node 4: prompt="shirt", threshold=0.35
Node 7: "red t-shirt, casual wear, cotton fabric, realistic clothing"
Node 8: "deformed clothing, unnatural folds, wrong colors"
Node 10: denoise=0.8
```

## Save Your Settings

After finding settings that work well:
- Right-click canvas → "Save Workflow"
- Name it descriptively: `"remove-person-settings.json"`
- Save to `ComfyUI/user/default/workflows/`
- Reuse for similar images!

## Need Help?

Common questions:
- Mask not accurate? → Adjust threshold
- Inpainting looks wrong? → Improve prompts, increase denoise
- Too slow? → Using optimal settings already
- Models missing? → Wait for auto-download on first run

Happy automatic inpainting! 🎨
