#!/usr/bin/env python3
"""
Test the inpainting workflow via ComfyUI API
Creates a test mask and queues the workflow
"""

import json
import requests
import time
from pathlib import Path
from PIL import Image, ImageDraw

# Configuration
COMFY_URL = "http://10.0.0.21:8188"
INPUT_IMAGE = "example.png"
WORKFLOW_FILE = "inpainting-workflow.json"

def create_test_mask():
    """Create a simple test mask (white square in center)"""
    print("📝 Creating test mask...")

    # Load the input image to get dimensions
    input_path = Path("ComfyUI/input") / INPUT_IMAGE
    if not input_path.exists():
        print(f"❌ Input image not found: {input_path}")
        return False

    img = Image.open(input_path)
    width, height = img.size

    # Create black mask
    mask = Image.new('RGB', (width, height), 'black')
    draw = ImageDraw.Draw(mask)

    # Draw white square in center (this is the area to inpaint)
    center_x, center_y = width // 2, height // 2
    square_size = min(width, height) // 4

    draw.rectangle(
        [
            center_x - square_size,
            center_y - square_size,
            center_x + square_size,
            center_y + square_size
        ],
        fill='white'
    )

    # Save mask
    mask_path = Path("ComfyUI/input") / "example_mask.png"
    mask.save(mask_path)

    print(f"✅ Test mask created: {mask_path}")
    print(f"   Image size: {width}x{height}")
    print(f"   Mask: White square in center ({square_size*2}x{square_size*2})")

    return True

def load_workflow():
    """Load and prepare the workflow"""
    print(f"\n📋 Loading workflow from {WORKFLOW_FILE}...")

    with open(WORKFLOW_FILE, 'r') as f:
        workflow = json.load(f)

    # Update the LoadImage node to use our test image
    for node in workflow['nodes']:
        if node['type'] == 'LoadImage':
            node['widgets_values'] = [INPUT_IMAGE]
            print(f"✅ Workflow loaded - using image: {INPUT_IMAGE}")
            break

    return workflow

def queue_prompt(workflow):
    """Queue the workflow via ComfyUI API"""
    print(f"\n🚀 Queueing workflow to {COMFY_URL}...")

    # Convert workflow to API format
    prompt = {}
    for node in workflow['nodes']:
        node_id = str(node['id'])
        prompt[node_id] = {
            "inputs": {},
            "class_type": node['type']
        }

        # Add inputs from links
        if 'inputs' in node:
            for inp in node['inputs']:
                if 'link' in inp:
                    # Find the source node
                    for link in workflow['links']:
                        if link[0] == inp['link']:
                            source_node_id = str(link[1])
                            source_output_index = link[2]
                            prompt[node_id]['inputs'][inp['name']] = [source_node_id, source_output_index]

        # Add widget values
        if 'widgets_values' in node:
            widget_names = {
                'CheckpointLoaderSimple': ['ckpt_name'],
                'CLIPTextEncode': ['text'],
                'LoadImage': ['image'],
                'SaveImage': ['filename_prefix'],
                'KSampler': ['seed', 'control_after_generate', 'steps', 'cfg', 'sampler_name', 'scheduler', 'denoise'],
                'VAEEncodeForInpaint': ['grow_mask_by']
            }

            if node['type'] in widget_names:
                for i, name in enumerate(widget_names[node['type']]):
                    if i < len(node['widgets_values']):
                        prompt[node_id]['inputs'][name] = node['widgets_values'][i]

    # Queue the prompt
    try:
        response = requests.post(
            f"{COMFY_URL}/prompt",
            json={"prompt": prompt}
        )

        if response.status_code == 200:
            result = response.json()
            prompt_id = result.get('prompt_id')
            print(f"✅ Workflow queued successfully!")
            print(f"   Prompt ID: {prompt_id}")
            return prompt_id
        else:
            print(f"❌ Failed to queue workflow: {response.status_code}")
            print(f"   Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error queueing workflow: {e}")
        return None

def monitor_progress(prompt_id):
    """Monitor the generation progress"""
    print(f"\n⏳ Monitoring progress...")

    start_time = time.time()
    last_status = None

    while True:
        try:
            # Check queue status
            response = requests.get(f"{COMFY_URL}/queue")
            if response.status_code == 200:
                queue_data = response.json()

                # Check if prompt is still running
                running = queue_data.get('queue_running', [])
                pending = queue_data.get('queue_pending', [])

                is_running = any(item[1] == prompt_id for item in running)
                is_pending = any(item[1] == prompt_id for item in pending)

                if is_running:
                    status = "🔄 Running..."
                elif is_pending:
                    status = "⏸️  Pending in queue..."
                else:
                    status = "✅ Complete!"

                if status != last_status:
                    elapsed = time.time() - start_time
                    print(f"   {status} (elapsed: {elapsed:.1f}s)")
                    last_status = status

                if not is_running and not is_pending:
                    print(f"\n✅ Generation complete! (took {elapsed:.1f}s)")
                    return True

            time.sleep(1)

        except KeyboardInterrupt:
            print("\n⚠️  Monitoring interrupted")
            return False
        except Exception as e:
            print(f"❌ Error monitoring: {e}")
            return False

def check_outputs():
    """Check the generated outputs"""
    print(f"\n📁 Checking outputs in ComfyUI/output/...")

    output_dir = Path("ComfyUI/output")

    # Find recent inpainted images
    inpainted_files = sorted(
        output_dir.glob("inpainted_*.png"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if inpainted_files:
        latest = inpainted_files[0]
        size_mb = latest.stat().st_size / 1024 / 1024
        print(f"✅ Latest output: {latest.name}")
        print(f"   Size: {size_mb:.2f} MB")
        print(f"   Path: {latest}")

        # Show a few recent outputs
        if len(inpainted_files) > 1:
            print(f"\n   Recent outputs:")
            for f in inpainted_files[:5]:
                mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(f.stat().st_mtime))
                print(f"   • {f.name} ({mtime})")

        return True
    else:
        print("❌ No inpainted outputs found")
        return False

def main():
    print("="*60)
    print("ComfyUI Inpainting Workflow Test")
    print("="*60)

    # Step 1: Create test mask
    if not create_test_mask():
        return

    # Step 2: Load workflow
    try:
        workflow = load_workflow()
    except Exception as e:
        print(f"❌ Failed to load workflow: {e}")
        return

    # Step 3: Queue workflow
    prompt_id = queue_prompt(workflow)
    if not prompt_id:
        return

    # Step 4: Monitor progress
    if not monitor_progress(prompt_id):
        print("\n⚠️  Could not confirm completion, check manually")

    # Step 5: Check outputs
    check_outputs()

    print("\n" + "="*60)
    print("🎉 Test complete! Check the output in ComfyUI/output/")
    print(f"   Web UI: {COMFY_URL}")
    print("="*60)

if __name__ == "__main__":
    main()
