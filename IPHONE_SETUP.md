# ComfyUI iPhone Setup Guide

## Connection Methods

### Method 1: Local Network (Same WiFi)
**Use when:** iPhone and computer are on the same WiFi network

**URL:** `http://10.0.0.21:8188`

**Steps:**
1. Start ComfyUI: `cd ~/Projects/comfy && ./start-comfyui.sh`
2. Open Comfy Portal app on iPhone
3. Add server with URL: `http://10.0.0.21:8188`
4. Should connect immediately

### Method 2: Remote Access (Tailscale)
**Use when:** You're away from home and need remote access

**URL:** `http://100.106.4.119:8188`

**Setup Steps:**
1. Login to Tailscale on computer:
   ```bash
   sudo tailscale up
   ```
   Follow the authentication URL

2. Get your Tailscale IP:
   ```bash
   tailscale ip -4
   ```
   Your Tailscale IP: **100.106.4.119** ✓

3. Install Tailscale app on iPhone from App Store

4. Login to Tailscale on iPhone with same account

5. In Comfy Portal app, add server with Tailscale IP:
   `http://100.106.4.119:8188`

## Starting ComfyUI

### Option 1: Using Systemd Service (Auto-starts on boot)
ComfyUI is now configured to start automatically on boot!

```bash
# Manage the service
~/Projects/comfy/manage-comfyui.sh start    # Start ComfyUI
~/Projects/comfy/manage-comfyui.sh stop     # Stop ComfyUI
~/Projects/comfy/manage-comfyui.sh restart  # Restart ComfyUI
~/Projects/comfy/manage-comfyui.sh status   # Check status
~/Projects/comfy/manage-comfyui.sh logs     # View logs (Ctrl+C to exit)
```

### Option 2: Manual Start (If you disabled auto-start)
```bash
cd ~/Projects/comfy
./start-comfyui.sh
```

The service is configured with:
- `--lowvram` - For 6GB GPU efficiency
- `--listen 0.0.0.0` - Accept connections from network
- `--enable-cors-header "*"` - Allow cross-origin requests for Comfy Portal

## Comfy Portal App Configuration

**Server Settings:**

Add two servers in Comfy Portal:

**Server 1 - Local Network:**
- **Name:** ComfyUI Local
- **URL:** `http://10.0.0.21:8188`

**Server 2 - Remote (Tailscale):**
- **Name:** ComfyUI Remote
- **URL:** `http://100.106.4.119:8188`

**Tips:**
- You can save both local and remote servers in Comfy Portal
- Use local when at home (faster)
- Use Tailscale when remote (secure tunnel)

## Troubleshooting

### Can't connect on local network
1. Check ComfyUI is running: `ps aux | grep main.py`
2. Check you're on same WiFi network
3. Try accessing in browser: `http://10.0.0.21:8188`

### Can't connect via Tailscale
1. Check Tailscale is running: `tailscale status`
2. Verify both devices show in Tailscale admin panel
3. Try pinging your computer from iPhone Terminal

### Port already in use
If port 8188 is busy, you can specify a different port:
```bash
./start-comfyui.sh --port 8189
```

## Security Notes

- **Local network:** Only accessible on your WiFi
- **Tailscale:** Encrypted VPN tunnel, very secure
- Both methods are safe for personal use
- Don't expose port 8188 directly to the internet without authentication

## Systemd Service Commands

The systemd service is already enabled and will start ComfyUI on boot!

**Quick Commands:**
```bash
~/Projects/comfy/manage-comfyui.sh          # Show help and status
~/Projects/comfy/manage-comfyui.sh start    # Start service
~/Projects/comfy/manage-comfyui.sh stop     # Stop service
~/Projects/comfy/manage-comfyui.sh restart  # Restart service
~/Projects/comfy/manage-comfyui.sh status   # Check if running
~/Projects/comfy/manage-comfyui.sh logs     # View live logs
~/Projects/comfy/manage-comfyui.sh disable  # Disable auto-start
~/Projects/comfy/manage-comfyui.sh enable   # Re-enable auto-start
```

**Manual systemd commands:**
```bash
systemctl --user start comfyui          # Start
systemctl --user stop comfyui           # Stop
systemctl --user status comfyui         # Status
journalctl --user -u comfyui -f         # Logs
```
