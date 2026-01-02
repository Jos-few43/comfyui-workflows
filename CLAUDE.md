# CLAUDE.md - ComfyUI Project

## Overview
ComfyUI for Stable Diffusion image generation with node-based workflows. Python 3.10-3.11 only, runs on RTX 3060 GPU with CUDA 12.4.

## Key Information
- **Virtual Environment**: `ComfyUI/venv/`
- **Start Command**: `./start-comfyui.sh` (launches at http://127.0.0.1:8188)
- **Setup Command**: `./setup-comfyui.sh`
- **Models Directory**: `ComfyUI/models/` (checkpoints, VAE, LoRA, ControlNet, inpainting)
- **Output Directory**: `ComfyUI/output/`
- **GPU**: RTX 3060 (12GB VRAM) - CUDA required

## Important Files
- `QUICK_START_INPAINTING.md` - Inpainting workflow guide
- `OVERNIGHT_BATCH_GUIDE.md` - Batch processing setup
- `batch-overnight-workflow.json` - Batch workflow configuration
- `img2img-workflow.json` - Image-to-image workflow

## Python Environment
**CRITICAL**: ComfyUI requires Python 3.10 or 3.11 (NOT 3.12+)
```bash
# Verify Python version
python --version  # Must be 3.10.x or 3.11.x

# Activate virtual environment
source ComfyUI/venv/bin/activate

# Verify PyTorch CUDA
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

## Common Tasks

### Start ComfyUI
```bash
./start-comfyui.sh
# Access at http://127.0.0.1:8188
```

### Download Models
```bash
./download-realistic-vision-NOW.sh  # Download Realistic Vision model
./download-models.sh                # Download essential models
./download-hf-models.sh             # Download from HuggingFace
```

### GPU Monitoring
```bash
nvidia-smi                          # Check GPU status
watch -n 1 nvidia-smi               # Monitor in real-time
```

## Development Guidelines

### File Operations
- **Never modify** files in `ComfyUI/models/` (large binary files)
- **Never read** .safetensors, .ckpt, .pt files (model weights)
- **Focus on** workflow JSON files and Python scripts

### Workflow Files
- JSON workflow files define the node graph
- Test workflows in ComfyUI web interface before saving
- Keep backup of working workflows

### Model Management
- Models go in `ComfyUI/models/[type]/` (checkpoints, loras, vae, etc.)
- Use symlinks for shared models to save space
- Verify model compatibility before downloading (SD1.5 vs SDXL)

## Troubleshooting

### CUDA Issues
```bash
# Verify CUDA
nvidia-smi

# Reinstall PyTorch with CUDA 12.4
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

### Python Version Issues
```bash
# If Python 3.12+ detected
sudo apt install python3.11
python3.11 -m venv ComfyUI/venv
source ComfyUI/venv/bin/activate
pip install -r ComfyUI/requirements.txt
```

### Out of Memory
- Reduce batch size in workflow
- Use `--lowvram` flag in start script
- Close other GPU applications
- Check `nvidia-smi` for memory usage

## Quick Commands Reference
```bash
./start-comfyui.sh                  # Start server
./setup-comfyui.sh                  # Reinstall/update
nvidia-smi                          # GPU status
ls ComfyUI/models/checkpoints/      # List models
ls ComfyUI/output/                  # View generated images
```

## Security Notes
- Don't commit model files to git (already in .gitignore)
- Don't expose ComfyUI port to public internet
- Keep API keys in .env files, never in workflows
