# ComfyUI Diagnosis Report

## 🔍 Issues Found

### 1. **Wrong Python Version**
- **Current**: Python 3.13.7
- **Problem**: Too new - ComfyUI and PyTorch aren't fully compatible with Python 3.13
- **Solution**: Use Python 3.10 (already installed on your system)

### 2. **No Virtual Environment**
- **Problem**: No isolated Python environment (venv)
- **Impact**: Dependencies install globally, can cause conflicts
- **Solution**: Create venv with Python 3.10

### 3. **Missing Dependencies**
- **PyTorch**: Not installed (ModuleNotFoundError: No module named 'torch')
- **PyYAML**: Not installed (ModuleNotFoundError: No module named 'yaml')
- **Others**: Likely missing many from requirements.txt
- **Solution**: Install all requirements in venv

### 4. **Installation Method**
- **Problem**: Dependencies were never properly installed
- **Likely cause**: Cloned repo but didn't run pip install -r requirements.txt

## ✅ Recommended Fix

### Quick Fix (Automated)
Run the setup script:
```bash
~/Projects/comfy/setup-comfyui.sh
```

This will:
1. Create Python 3.10 virtual environment
2. Install PyTorch (CUDA or CPU version)
3. Install all ComfyUI requirements
4. Verify installation

### Manual Fix
If you prefer to do it manually:

```bash
cd ~/Projects/comfy/ComfyUI

# Create venv with Python 3.10
/usr/bin/python3.10 -m venv venv

# Activate venv
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install PyTorch (CUDA version - adjust for your GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Or CPU version if no GPU:
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install ComfyUI requirements
pip install -r requirements.txt

# Test
python main.py --help
```

## 📋 System Info

- **OS**: Arch Linux
- **Available Python Versions**:
  - Python 3.13.7 (current default, too new)
  - Python 3.10 (recommended, installed at /usr/bin/python3.10)
- **ComfyUI Location**: ~/Projects/comfy/ComfyUI
- **NVIDIA GPU**: Checking... (run `nvidia-smi` to verify)

## 🎯 After Setup

### Start ComfyUI
```bash
# Quick start (recommended)
~/Projects/comfy/start-comfyui.sh

# Or manually
cd ~/Projects/comfy/ComfyUI
source venv/bin/activate
python main.py
```

### Common Options
```bash
# Start with browser auto-launch
python main.py --auto-launch

# Use specific port
python main.py --port 8188

# CPU mode (if no GPU)
python main.py --cpu

# Low VRAM mode
python main.py --lowvram
```

## 🐛 Debugging Tips

### If it still doesn't work:

1. **Check Python version in venv**:
   ```bash
   source ~/Projects/comfy/ComfyUI/venv/bin/activate
   python --version  # Should show Python 3.10.x
   ```

2. **Verify PyTorch installation**:
   ```bash
   python -c "import torch; print(torch.__version__)"
   ```

3. **Check CUDA availability** (if you have NVIDIA GPU):
   ```bash
   python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
   ```

4. **Check requirements**:
   ```bash
   pip list | grep -E "(torch|comfy|numpy|yaml)"
   ```

5. **Run with verbose logging**:
   ```bash
   python main.py --verbose DEBUG
   ```

## 📚 Useful Commands

```bash
# Activate venv (always do this first!)
source ~/Projects/comfy/ComfyUI/venv/bin/activate

# Deactivate venv
deactivate

# Update ComfyUI
cd ~/Projects/comfy/ComfyUI
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Check for GPU
nvidia-smi  # If you have NVIDIA GPU
```

## 🔧 Quick Reference

| Command | Description |
|---------|-------------|
| `~/Projects/comfy/setup-comfyui.sh` | Initial setup (run once) |
| `~/Projects/comfy/start-comfyui.sh` | Start ComfyUI |
| `source venv/bin/activate` | Activate virtual environment |
| `deactivate` | Exit virtual environment |
| `python main.py --help` | See all options |

## ⚠️ Important Notes

1. **Always activate venv before running ComfyUI**
2. **Don't use system Python 3.13** - it's too new
3. **GPU drivers**: Make sure NVIDIA drivers are up to date if using CUDA
4. **Disk space**: PyTorch + models can take several GB

## 🎉 Expected Result

After setup, you should see:
```
Total VRAM 24564 MB, total RAM 32000 MB
pytorch version: 2.x.x
Set vram state to: NORMAL_VRAM
Device: cuda:0 NVIDIA GeForce RTX ...
...
Starting server

To see the GUI go to: http://127.0.0.1:8188
```
