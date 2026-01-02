#!/bin/bash
# ComfyUI Service Management Script

case "$1" in
    start)
        echo "Starting ComfyUI service..."
        systemctl --user start comfyui.service
        echo "✓ ComfyUI started"
        ;;
    stop)
        echo "Stopping ComfyUI service..."
        systemctl --user stop comfyui.service
        echo "✓ ComfyUI stopped"
        ;;
    restart)
        echo "Restarting ComfyUI service..."
        systemctl --user restart comfyui.service
        echo "✓ ComfyUI restarted"
        ;;
    status)
        systemctl --user status comfyui.service
        ;;
    logs)
        journalctl --user -u comfyui.service -f
        ;;
    enable)
        echo "Enabling ComfyUI to start on boot..."
        systemctl --user enable comfyui.service
        echo "✓ ComfyUI will start automatically on boot"
        ;;
    disable)
        echo "Disabling ComfyUI auto-start..."
        systemctl --user disable comfyui.service
        echo "✓ ComfyUI will not start automatically"
        ;;
    *)
        echo "ComfyUI Service Manager"
        echo "======================="
        echo ""
        echo "Usage: $0 {start|stop|restart|status|logs|enable|disable}"
        echo ""
        echo "Commands:"
        echo "  start    - Start ComfyUI service"
        echo "  stop     - Stop ComfyUI service"
        echo "  restart  - Restart ComfyUI service"
        echo "  status   - Show service status"
        echo "  logs     - Show and follow service logs (Ctrl+C to exit)"
        echo "  enable   - Enable auto-start on boot"
        echo "  disable  - Disable auto-start on boot"
        echo ""
        echo "Current status:"
        systemctl --user is-active comfyui.service >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "  Service: RUNNING ✓"
        else
            echo "  Service: STOPPED"
        fi
        systemctl --user is-enabled comfyui.service >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "  Auto-start: ENABLED ✓"
        else
            echo "  Auto-start: DISABLED"
        fi
        ;;
esac
