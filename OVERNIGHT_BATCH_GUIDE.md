# Overnight Batch Processing Guide

## What This Does

This workflow will generate multiple variations of your photo overnight with different settings, so you can wake up and compare which works best!

## The Workflow Setup

**File**: `batch-overnight-workflow.json`

This creates **2 parallel processing chains** that run simultaneously:

### Chain 1: Subtle Enhancement (Denoise 0.3)
- 30 steps
- CFG 7.5
- Saves as: `denoise_0.3_*.png`
- **Result**: Light enhancement, preserves original very closely

### Chain 2: Moderate Enhancement (Denoise 0.4)
- 40 steps (higher quality)
- CFG 8.0
- Saves as: `denoise_0.4_*.png`
- **Result**: More noticeable improvement, still preserves subject

## How to Run It

### Method 1: In ComfyUI Interface

1. Load the workflow:
   - Click menu (☰) → Load
   - Navigate to: `/home/yish/Projects/comfy/batch-overnight-workflow.json`

2. Click "Queue Prompt" **multiple times** (10-20 times)
   - Each click adds one batch to the queue
   - You'll get 2 images per batch (one from each chain)
   - 10 batches = 20 images total
   - 20 batches = 40 images total

3. Check the queue:
   - Look at bottom/side panel to see how many are queued

4. Let it run overnight!
   - Close browser (ComfyUI keeps running)
   - Server stays active in terminal
   - Find results in: `~/Projects/comfy/ComfyUI/output/`

### Method 2: Automated Batch Script (Coming soon)

We can create a script that automatically queues 50+ variations with different:
- Denoise levels (0.2, 0.3, 0.4, 0.5)
- Different seeds (for variety)
- Different prompts/styles

## Timing Estimates

On your RTX 3060 6GB with --lowvram:

- **One generation** (30 steps): ~45-60 seconds
- **One batch** (2 generations): ~2 minutes
- **10 batches** (20 images): ~20 minutes
- **50 batches** (100 images): ~1.5-2 hours
- **200 batches** (400 images): ~6-8 hours (full overnight)

## Finding Your Results

All outputs save to:
```
~/Projects/comfy/ComfyUI/output/
```

Files will be named:
- `denoise_0.3_00001.png`
- `denoise_0.3_00002.png`
- `denoise_0.4_00001.png`
- `denoise_0.4_00002.png`

## Customizing the Workflow

### Change Denoise Levels

In each KSampler node, the last number is denoise:
- Current: `0.3` and `0.4`
- Try: `0.2` (very subtle) to `0.6` (more creative)

### Change Steps

More steps = higher quality but slower:
- Fast: 20 steps (~30 sec)
- Balanced: 30 steps (~45 sec)
- High Quality: 50 steps (~75 sec)
- Ultra: 100 steps (~2.5 min)

### Change Prompts

Edit the CLIP Text Encode nodes:

**Positive prompt ideas**:
- `portrait of a woman, cinematic lighting, professional photography`
- `portrait of a woman, golden hour, warm tones, professional`
- `portrait of a woman, studio lighting, fashion photography`
- `portrait of a woman, natural light, soft focus, dreamy`

**Keep "portrait of a woman"** at the start to preserve the subject!

## Monitoring Progress

### While Running:
- Terminal shows progress
- Browser shows queue count decreasing
- Output folder fills with images

### Check Current Output:
```bash
ls -lh ~/Projects/comfy/ComfyUI/output/ | tail -20
```

### View Latest Image:
```bash
# Most recently created image
ls -t ~/Projects/comfy/ComfyUI/output/*.png | head -1
```

## Stopping the Process

If you need to stop:
1. In browser: Click "Clear Queue"
2. Or press Ctrl+C in terminal (stops ComfyUI entirely)

## Tips for Best Results

1. **Start Small**: Queue 5-10 batches first to test
2. **Check Progress**: After 10 minutes, check if results look good
3. **Adjust if Needed**: If not right, stop and tweak settings
4. **Then Go Big**: Queue 100+ batches for overnight

## What to Look For

Compare the outputs to find:
- Best denoise level for your photo
- Which prompts give best results
- Sweet spot between preservation and enhancement

## Next Steps

After your overnight batch:
1. Review all outputs
2. Note which settings worked best
3. We can create a refined workflow with those optimal settings
4. Scale up to process multiple photos!

---

**Created**: 2025-12-01
**For**: RTX 3060 6GB Laptop GPU
**Model**: Realistic Vision V6
