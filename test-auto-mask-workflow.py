#!/usr/bin/env python3
"""
Test the auto-mask inpainting workflow
Detects and removes a person from example.png
"""

import json
import requests
import time
from pathlib import Path

COMFY_URL = "http://10.0.0.21:8188"
WORKFLOW_FILE = "auto-mask-inpainting-workflow.json"
TEST_IMAGE = "example.png"

def load_workflow():
    """Load the workflow JSON"""
    print("📋 Loading workflow...")
    with open(WORKFLOW_FILE, 'r') as f:
        workflow = json.load(f)
    print(f"✅ Workflow loaded: {len(workflow['nodes'])} nodes")
    return workflow

def convert_to_api_format(workflow):
    """Convert workflow to ComfyUI API format"""
    print("\n🔄 Converting to API format...")

    prompt = {}

    # Map node types to their widget parameter names
    widget_mappings = {
        'LoadImage': ['image'],
        'GroundingDinoModelLoader (SegmentAnything)': ['model_name'],
        'SAMModelLoader (SegmentAnything)': ['model_name', 'device_mode'],
        'GroundingDinoSAMSegment (SegmentAnything)': ['prompt', 'threshold'],
        'CheckpointLoaderSimple': ['ckpt_name'],
        'CLIPTextEncode': ['text'],
        'VAEEncodeForInpaint': ['grow_mask_by'],
        'KSampler': ['seed', 'control_after_generate', 'steps', 'cfg', 'sampler_name', 'scheduler', 'denoise'],
        'SaveImage': ['filename_prefix'],
    }

    for node in workflow['nodes']:
        node_id = str(node['id'])
        node_type = node['type']

        prompt[node_id] = {
            "inputs": {},
            "class_type": node_type
        }

        # Add widget values
        if 'widgets_values' in node and node_type in widget_mappings:
            param_names = widget_mappings[node_type]
            for i, param_name in enumerate(param_names):
                if i < len(node['widgets_values']):
                    prompt[node_id]['inputs'][param_name] = node['widgets_values'][i]

    # Add connections from links
    for link in workflow['links']:
        link_id, source_node, source_slot, target_node, target_slot, link_type = link

        # Find the target node's input name
        target_node_data = next(n for n in workflow['nodes'] if n['id'] == target_node)
        if 'inputs' in target_node_data and target_slot < len(target_node_data['inputs']):
            input_name = target_node_data['inputs'][target_slot]['name']
            prompt[str(target_node)]['inputs'][input_name] = [str(source_node), source_slot]

    print(f"✅ API format ready: {len(prompt)} nodes")
    return prompt

def queue_workflow(prompt):
    """Queue the workflow via API"""
    print(f"\n🚀 Queueing workflow to {COMFY_URL}...")

    try:
        response = requests.post(
            f"{COMFY_URL}/prompt",
            json={"prompt": prompt}
        )

        if response.status_code == 200:
            result = response.json()
            prompt_id = result.get('prompt_id')
            print(f"✅ Workflow queued!")
            print(f"   Prompt ID: {prompt_id}")
            return prompt_id
        else:
            print(f"❌ Failed to queue: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def monitor_progress(prompt_id):
    """Monitor workflow execution"""
    print(f"\n⏳ Monitoring progress...")
    print("   This may take a while on first run (model loading)...")

    start_time = time.time()
    last_status = None

    while True:
        try:
            response = requests.get(f"{COMFY_URL}/history/{prompt_id}")
            if response.status_code == 200:
                history = response.json()

                if prompt_id in history:
                    prompt_info = history[prompt_id]

                    # Check status
                    if 'status' in prompt_info:
                        status_info = prompt_info['status']
                        if 'completed' in status_info and status_info['completed']:
                            elapsed = time.time() - start_time
                            print(f"\n✅ Complete! (took {elapsed:.1f}s)")
                            return True
                        elif 'messages' in status_info:
                            for msg in status_info['messages']:
                                if msg != last_status:
                                    print(f"   📝 {msg}")
                                    last_status = msg

                    # Check outputs
                    if 'outputs' in prompt_info:
                        elapsed = time.time() - start_time
                        print(f"\n✅ Generation complete! (took {elapsed:.1f}s)")
                        return True

            # Check queue status
            response = requests.get(f"{COMFY_URL}/queue")
            if response.status_code == 200:
                queue_data = response.json()
                running = queue_data.get('queue_running', [])
                pending = queue_data.get('queue_pending', [])

                is_running = any(str(item[1]) == str(prompt_id) for item in running)
                is_pending = any(str(item[1]) == str(prompt_id) for item in pending)

                if not is_running and not is_pending:
                    elapsed = time.time() - start_time

                    # Check if it completed via history
                    response = requests.get(f"{COMFY_URL}/history/{prompt_id}")
                    if response.status_code == 200:
                        history = response.json()
                        if prompt_id in history and 'outputs' in history[prompt_id]:
                            print(f"\n✅ Generation complete! (took {elapsed:.1f}s)")
                            return True

                    print(f"\n⚠️  No longer in queue after {elapsed:.1f}s")
                    print("   Check ComfyUI web interface for results")
                    return True

            time.sleep(2)

        except KeyboardInterrupt:
            print("\n⚠️  Monitoring interrupted")
            return False
        except Exception as e:
            print(f"❌ Error monitoring: {e}")
            time.sleep(2)

def check_output():
    """Check for generated output"""
    print(f"\n📁 Checking outputs...")

    output_dir = Path("ComfyUI/output")
    auto_inpainted = sorted(
        output_dir.glob("auto_inpainted_*.png"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if auto_inpainted:
        latest = auto_inpainted[0]
        size_mb = latest.stat().st_size / 1024 / 1024
        mtime = time.strftime('%H:%M:%S', time.localtime(latest.stat().st_mtime))

        print(f"✅ Latest output: {latest.name}")
        print(f"   Size: {size_mb:.2f} MB")
        print(f"   Time: {mtime}")
        print(f"   Path: {latest}")

        if len(auto_inpainted) > 1:
            print(f"\n   Recent outputs ({len(auto_inpainted)} total):")
            for f in auto_inpainted[:5]:
                t = time.strftime('%H:%M:%S', time.localtime(f.stat().st_mtime))
                print(f"   • {f.name} ({t})")

        return True
    else:
        print("❌ No auto_inpainted outputs found")

        # Check for any recent outputs
        all_outputs = sorted(
            output_dir.glob("*.png"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:5]

        if all_outputs:
            print(f"\n   Recent outputs in ComfyUI/output/:")
            for f in all_outputs:
                t = time.strftime('%H:%M:%S', time.localtime(f.stat().st_mtime))
                print(f"   • {f.name} ({t})")

        return False

def main():
    print("="*60)
    print("Auto-Mask Inpainting Workflow Test")
    print("="*60)
    print(f"\nTest: Remove person from {TEST_IMAGE}")
    print(f"Detection: GroundingDINO + SAM")
    print(f"Model: Realistic Vision")

    # Load and convert workflow
    workflow = load_workflow()
    prompt = convert_to_api_format(workflow)

    # Queue workflow
    prompt_id = queue_workflow(prompt)
    if not prompt_id:
        print("\n❌ Failed to queue workflow")
        return

    # Monitor progress
    success = monitor_progress(prompt_id)

    # Check output
    check_output()

    print("\n" + "="*60)
    print("🎉 Test complete!")
    print(f"   View results at: {COMFY_URL}")
    print("="*60)

if __name__ == "__main__":
    main()
