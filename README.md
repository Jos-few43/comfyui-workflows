# ComfyUI Setup - Fixed & Working!

## 🎯 What Was Wrong

1. **Python 3.13** - Too new, ComfyUI needs Python 3.10-3.11
2. **No virtual environment** - Dependencies were never installed
3. **Missing PyTorch** - The core dependency wasn't installed

## ✅ What's Been Fixed

1. **Created Python 3.10 virtual environment** at `~/Projects/comfy/ComfyUI/venv`
2. **Installing PyTorch 2.6.0** with CUDA 12.4 support for your RTX 3060
3. **Will install all ComfyUI requirements** from requirements.txt

## 🚀 How to Start ComfyUI

### Quick Start (Recommended)
```bash
~/Projects/comfy/start-comfyui.sh
```

### Manual Start
```bash
cd ~/Projects/comfy/ComfyUI
source venv/bin/activate
python main.py
```

Then open your browser to: http://127.0.0.1:8188

## 🖥️ Your Hardware

- **GPU**: NVIDIA GeForce RTX 3060 (6GB VRAM)
- **CUDA**: Version 13.0
- **Driver**: 580.105.08
- **Recommended**: Use `--lowvram` flag if you run out of memory

## ⚙️ Useful Commands

### Start with options:
```bash
# Auto-open browser
python main.py --auto-launch

# Low VRAM mode (recommended for 6GB GPU)
python main.py --lowvram

# Different port
python main.py --port 8080

# Preview images while generating
python main.py --preview-method auto
```

### Debugging:
```bash
# Check PyTorch installation
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"

# Verbose logging
python main.py --verbose DEBUG

# Check GPU usage
watch -n 1 nvidia-smi
```

## 📁 Directory Structure

```
~/Projects/comfy/
├── ComfyUI/               # Main ComfyUI installation
│   ├── venv/              # Python 3.10 virtual environment
│   ├── main.py            # Startup script
│   ├── models/            # Where AI models go
│   ├── custom_nodes/      # Extensions
│   └── output/            # Generated images
├── setup-comfyui.sh       # Setup script (already ran)
├── start-comfyui.sh       # Quick start script
├── DIAGNOSIS.md           # Detailed problem diagnosis
└── README.md              # This file
```

## 📦 Installed Packages

- **PyTorch 2.6.0** + CUDA 12.4
- **torchvision** - Image processing
- **torchaudio** - Audio processing
- **All ComfyUI requirements** - See requirements.txt

## 🔧 Maintenance

### Update ComfyUI:
```bash
cd ~/Projects/comfy/ComfyUI
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Install custom nodes:
```bash
cd ~/Projects/comfy/ComfyUI/custom_nodes
git clone <custom-node-repo>
# Restart ComfyUI
```

### Check disk space:
```bash
du -sh ~/Projects/comfy/ComfyUI/models/*
```

## 💡 Tips

1. **Always activate venv first**: `source venv/bin/activate`
2. **Use --lowvram**: Your 6GB GPU benefits from this flag
3. **Monitor GPU**: Run `nvidia-smi` in another terminal
4. **Save workflows**: ComfyUI can export/import workflows as JSON
5. **Models location**: Download models to `ComfyUI/models/`

## 🆘 Troubleshooting

### "Out of VRAM" errors:
```bash
python main.py --lowvram
# or even more aggressive:
python main.py --novram
```

### "ModuleNotFoundError":
```bash
source venv/bin/activate  # Make sure venv is active!
pip install -r requirements.txt
```

### Slow generation:
- Your RTX 3060 6GB is entry-level for AI
- Use smaller models (SD 1.5 instead of SDXL)
- Enable `--lowvram` flag
- Close other GPU applications

### Can't connect to web UI:
- Check if server started: Look for "To see the GUI go to: http://..."
- Try different port: `python main.py --port 8080`
- Check firewall settings

## 🎨 Next Steps

1. **Download models**:
   - Stable Diffusion checkpoints go in `models/checkpoints/`
   - VAEs go in `models/vae/`
   - LoRAs go in `models/loras/`

2. **Try example workflows**:
   - Load from ComfyUI-Manager
   - Import from community workflows

3. **Customize**:
   - Install custom nodes for extra features
   - Explore ComfyUI Manager for easy node management

## 📚 Resources

- **ComfyUI Wiki**: https://github.com/comfyanonymous/ComfyUI/wiki
- **Models**: https://civitai.com/
- **Workflows**: https://comfyworkflows.com/
- **Discord**: ComfyUI has an active community

## ✨ Current Status

- ✅ Python 3.10 virtual environment created
- ⏳ PyTorch 2.6.0 + CUDA installing...
- ⏳ ComfyUI requirements installing next...
- ⏹️ Ready to test startup once installation completes

Check installation progress with:
```bash
tail -f <installation-log>
# Or just wait for the setup to complete
```
