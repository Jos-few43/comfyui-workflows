Check GPU status, VRAM usage, and verify CUDA availability for ComfyUI.

Run these checks:
1. nvidia-smi for GPU status and memory
2. Check if ComfyUI process is using GPU
3. Verify PyTorch CUDA in venv: `source ComfyUI/venv/bin/activate && python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}, Devices: {torch.cuda.device_count()}')"`
4. Show free VRAM
