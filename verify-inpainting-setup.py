#!/usr/bin/env python3
"""
ComfyUI Inpainting Setup Verification Script
Checks if your environment is ready for inpainting workflows
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_check(passed, message, details=""):
    status = f"{Colors.GREEN}✓{Colors.RESET}" if passed else f"{Colors.RED}✗{Colors.RESET}"
    print(f"{status} {message}")
    if details:
        print(f"  {Colors.YELLOW}{details}{Colors.RESET}")

def check_python_version():
    """Check if Python version is compatible (3.10 or 3.11)"""
    print_header("Python Environment")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major == 3 and version.minor in [10, 11]:
        print_check(True, f"Python version: {version_str}")
        return True
    else:
        print_check(False, f"Python version: {version_str}",
                   "ComfyUI requires Python 3.10 or 3.11")
        return False

def check_pytorch_cuda():
    """Check if PyTorch is installed with CUDA support"""
    print_header("PyTorch & CUDA")
    try:
        import torch
        pytorch_version = torch.__version__
        cuda_available = torch.cuda.is_available()

        print_check(True, f"PyTorch installed: {pytorch_version}")

        if cuda_available:
            cuda_version = torch.version.cuda
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3

            print_check(True, f"CUDA available: {cuda_version}")
            print_check(True, f"GPU: {gpu_name} ({gpu_memory:.1f} GB)")
            return True
        else:
            print_check(False, "CUDA not available",
                       "GPU acceleration won't work")
            return False
    except ImportError:
        print_check(False, "PyTorch not installed",
                   "Run: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124")
        return False

def check_models():
    """Check for available models"""
    print_header("Model Files")

    base_dir = Path("ComfyUI/models")
    results = {
        'checkpoints': [],
        'inpaint': [],
        'vae': [],
        'loras': []
    }

    # Check checkpoints
    checkpoint_dir = base_dir / "checkpoints"
    if checkpoint_dir.exists():
        results['checkpoints'] = list(checkpoint_dir.glob("*.safetensors"))
        if results['checkpoints']:
            print_check(True, f"Found {len(results['checkpoints'])} checkpoint model(s):")
            for model in results['checkpoints']:
                size_gb = model.stat().st_size / 1024**3
                model_type = "SDXL" if size_gb > 5 else "SD1.5"
                print(f"  • {model.name} ({size_gb:.1f}GB - {model_type})")
        else:
            print_check(False, "No checkpoint models found",
                       "Download from civitai.com or run ./download-models.sh")

    # Check inpaint models
    inpaint_dir = base_dir / "inpaint"
    if inpaint_dir.exists():
        results['inpaint'] = list(inpaint_dir.glob("*.safetensors")) + list(inpaint_dir.glob("*.pth"))
        if results['inpaint']:
            print_check(True, f"Found {len(results['inpaint'])} inpainting model(s)")
            for model in results['inpaint']:
                print(f"  • {model.name}")
        else:
            print_check(False, "No dedicated inpainting models found",
                       "Standard checkpoints can still do inpainting using VAEEncodeForInpaint")

    # Check VAE
    vae_dir = base_dir / "vae"
    if vae_dir.exists():
        results['vae'] = list(vae_dir.glob("*.safetensors")) + list(vae_dir.glob("*.pth"))
        if results['vae']:
            print_check(True, f"Found {len(results['vae'])} VAE model(s)")
        else:
            print_check(False, "No VAE models found",
                       "Built-in VAE from checkpoints will be used")

    # Check LoRAs
    lora_dir = base_dir / "loras"
    if lora_dir.exists():
        results['loras'] = list(lora_dir.glob("*.safetensors"))
        if results['loras']:
            print_check(True, f"Found {len(results['loras'])} LoRA model(s)")

    return results

def check_workflow_json():
    """Check if workflow JSON files are valid"""
    print_header("Workflow Files")

    workflow_files = [
        "inpainting-workflow.json",
        "img2img-workflow.json",
        "batch-overnight-workflow.json"
    ]

    valid_workflows = []
    for workflow in workflow_files:
        if Path(workflow).exists():
            try:
                with open(workflow, 'r') as f:
                    data = json.load(f)

                # Check for required keys
                if 'nodes' in data and 'links' in data:
                    node_count = len(data['nodes'])
                    print_check(True, f"{workflow}: Valid ({node_count} nodes)")

                    # Check for inpainting-specific nodes
                    if "inpainting" in workflow:
                        has_vae_encode = any(
                            node.get('type') == 'VAEEncodeForInpaint'
                            for node in data['nodes']
                        )
                        if has_vae_encode:
                            print(f"  {Colors.GREEN}Contains VAEEncodeForInpaint node{Colors.RESET}")
                        else:
                            print(f"  {Colors.YELLOW}Missing VAEEncodeForInpaint node{Colors.RESET}")

                        # Check model reference
                        for node in data['nodes']:
                            if node.get('type') == 'CheckpointLoaderSimple':
                                model_name = node.get('widgets_values', [None])[0]
                                if model_name:
                                    model_path = Path(f"ComfyUI/models/checkpoints/{model_name}")
                                    if model_path.exists():
                                        print(f"  {Colors.GREEN}Model exists: {model_name}{Colors.RESET}")
                                    else:
                                        print(f"  {Colors.RED}Model missing: {model_name}{Colors.RESET}")

                    valid_workflows.append(workflow)
                else:
                    print_check(False, f"{workflow}: Invalid structure")
            except json.JSONDecodeError:
                print_check(False, f"{workflow}: JSON parsing error")
        else:
            print_check(False, f"{workflow}: File not found")

    return valid_workflows

def check_input_output_dirs():
    """Check input/output directories"""
    print_header("Directories")

    dirs_to_check = {
        'ComfyUI/input': 'Input images directory',
        'ComfyUI/output': 'Generated images directory',
        'ComfyUI/models': 'Models directory'
    }

    all_exist = True
    for dir_path, description in dirs_to_check.items():
        path = Path(dir_path)
        if path.exists():
            file_count = len(list(path.glob("*"))) if path.is_dir() else 0
            print_check(True, f"{description}: {dir_path} ({file_count} files)")
        else:
            print_check(False, f"{description}: {dir_path} not found")
            all_exist = False

    return all_exist

def generate_recommendations(model_results, workflow_valid):
    """Generate recommendations based on checks"""
    print_header("Recommendations")

    recommendations = []

    # Check for checkpoint models
    if not model_results['checkpoints']:
        recommendations.append(
            "📥 Download a checkpoint model:\n"
            "   Run: ./download-realistic-vision-NOW.sh\n"
            "   Or: ./download-models.sh"
        )

    # Check for inpainting models
    if not model_results['inpaint']:
        recommendations.append(
            "🎨 For dedicated inpainting models:\n"
            "   Download SD1.5 Inpainting model from:\n"
            "   https://huggingface.co/runwayml/stable-diffusion-inpainting\n"
            "   Save to: ComfyUI/models/checkpoints/"
        )

    # Check for VAE
    if not model_results['vae'] and model_results['checkpoints']:
        has_vae_model = any('vae' in str(m).lower() for m in model_results['checkpoints'])
        if not has_vae_model:
            recommendations.append(
                "🔧 Optional - Download VAE for better quality:\n"
                "   https://huggingface.co/stabilityai/sd-vae-ft-mse-original\n"
                "   Save to: ComfyUI/models/vae/"
            )

    # Workflow recommendations
    if not workflow_valid:
        recommendations.append(
            "📋 Update your workflow JSON:\n"
            "   • Change model name to an existing checkpoint\n"
            "   • Verify VAEEncodeForInpaint node is present\n"
            "   • Test in ComfyUI web interface"
        )

    # General tips
    recommendations.append(
        "💡 Quick Start Tips:\n"
        "   1. Place test image in ComfyUI/input/\n"
        "   2. Create a white mask (PNG) for areas to inpaint\n"
        "   3. Start ComfyUI: ./start-comfyui.sh\n"
        "   4. Load your workflow in the web interface\n"
        "   5. Adjust prompts and generate!"
    )

    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"{Colors.YELLOW}{rec}{Colors.RESET}\n")
    else:
        print(f"{Colors.GREEN}✓ Your setup looks good! Ready for inpainting.{Colors.RESET}\n")

def main():
    print(f"\n{Colors.BOLD}ComfyUI Inpainting Setup Verification{Colors.RESET}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Run all checks
    python_ok = check_python_version()
    cuda_ok = check_pytorch_cuda()
    model_results = check_models()
    workflow_valid = check_workflow_json()
    dirs_ok = check_input_output_dirs()

    # Summary
    print_header("Summary")

    total_checks = 5
    passed_checks = sum([
        python_ok,
        cuda_ok,
        len(model_results['checkpoints']) > 0,
        len(workflow_valid) > 0,
        dirs_ok
    ])

    print(f"Passed: {passed_checks}/{total_checks} checks")

    if passed_checks == total_checks:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All checks passed! Your inpainting setup is ready!{Colors.RESET}\n")
    elif passed_checks >= 3:
        print(f"\n{Colors.YELLOW}⚠️  Setup is mostly ready, but some improvements needed.{Colors.RESET}\n")
    else:
        print(f"\n{Colors.RED}❌ Several issues need to be resolved before inpainting will work.{Colors.RESET}\n")

    # Generate recommendations
    generate_recommendations(model_results, len(workflow_valid) > 0)

    return passed_checks == total_checks

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
