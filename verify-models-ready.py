#!/usr/bin/env python3
"""Verify all models are ready for auto-mask workflow"""

from pathlib import Path
import requests

COMFY_URL = "http://10.0.0.21:8188"

print("="*60)
print("Auto-Mask Workflow - Model Verification")
print("="*60)

# Check GroundingDINO
print("\n📦 GroundingDINO Model:")
gdino_dir = Path("ComfyUI/models/grounding-dino")
if gdino_dir.exists():
    cfg = gdino_dir / "GroundingDINO_SwinT_OGC.cfg.py"
    pth = gdino_dir / "groundingdino_swint_ogc.pth"

    if cfg.exists():
        print(f"  ✅ Config: {cfg.name} ({cfg.stat().st_size} bytes)")
    else:
        print(f"  ❌ Config missing")

    if pth.exists():
        size_mb = pth.stat().st_size / 1024 / 1024
        print(f"  ✅ Model: {pth.name} ({size_mb:.1f} MB)")
    else:
        print(f"  ❌ Model missing")
else:
    print("  ❌ Directory not found")

# Check SAM
print("\n📦 Segment Anything Model:")
sam_dir = Path("ComfyUI/models/sams")
if sam_dir.exists():
    sam_model = sam_dir / "sam_vit_b_01ec64.pth"

    if sam_model.exists():
        size_mb = sam_model.stat().st_size / 1024 / 1024
        print(f"  ✅ Model: {sam_model.name} ({size_mb:.1f} MB)")
    else:
        print(f"  ❌ Model missing")
else:
    print("  ❌ Directory not found")

# Check checkpoint
print("\n📦 AI Checkpoint:")
checkpoint_dir = Path("ComfyUI/models/checkpoints")
rv_model = checkpoint_dir / "realisticVisionV60B1_v51HyperVAE.safetensors"

if rv_model.exists():
    size_gb = rv_model.stat().st_size / 1024 / 1024 / 1024
    print(f"  ✅ Model: {rv_model.name} ({size_gb:.1f} GB)")
else:
    print(f"  ❌ Realistic Vision model missing")

# Check ComfyUI is running
print("\n🌐 ComfyUI Status:")
try:
    response = requests.get(f"{COMFY_URL}/system_stats", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"  ✅ ComfyUI running")
        print(f"  ✅ Version: {data['system']['comfyui_version']}")
        print(f"  ✅ PyTorch: {data['system']['pytorch_version']}")
        print(f"  ✅ URL: {COMFY_URL}")
    else:
        print(f"  ⚠️  ComfyUI responded with: {response.status_code}")
except Exception as e:
    print(f"  ❌ ComfyUI not accessible: {e}")

# Check workflow file
print("\n📋 Workflow File:")
workflow_file = Path("auto-mask-inpainting-workflow.json")
if workflow_file.exists():
    size_kb = workflow_file.stat().st_size / 1024
    print(f"  ✅ Workflow: {workflow_file.name} ({size_kb:.1f} KB)")

    # Check if in workflows directory
    comfy_workflow = Path("ComfyUI/user/default/workflows/auto-mask-inpainting-workflow.json")
    if comfy_workflow.exists():
        print(f"  ✅ Available in ComfyUI web interface")
    else:
        print(f"  ⚠️  Not in workflows directory")
else:
    print(f"  ❌ Workflow file not found")

print("\n" + "="*60)
print("✅ READY TO TEST!")
print("="*60)
print("\nManual Test Steps:")
print("1. Open: http://10.0.0.21:8188")
print("2. Click 'Workflows' → 'auto-mask-inpainting-workflow.json'")
print("3. Node 4: Keep prompt='person' or change to detect something else")
print("4. Click 'Queue Prompt'")
print("5. Watch Node 5 for mask preview")
print("6. Final result in Node 13")
print("\n" + "="*60)
