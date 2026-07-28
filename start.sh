#!/bin/bash
set -e

echo "[LinDOS] Building C++ core optimizer..."
make

echo "[LinDOS] Starting C++ background optimization daemon..."
./lindos_core &
CORE_PID=$!

# Check if a graphical display is available
if [ -z "$DISPLAY" ]; then
    echo "[LinDOS] No X11 display detected. Initializing Virtual Framebuffer (Xvfb)..."
    if ! command -v xvfb-run &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y xvfb >/dev/null 2>&1 || apt-get update && apt-get install -y xvfb >/dev/null 2>&1
    fi
    echo "[LinDOS] Launching Python Desktop Environment inside virtual display..."
    xvfb-run -a python3 gui/desktop.py &
    GUI_PID=$!
else
    echo "[LinDOS] Launching Python Desktop Environment..."
    python3 gui/desktop.py &
    GUI_PID=$!
fi

# Ensure clean shutdown on exit
trap "kill $CORE_PID $GUI_PID 2>/dev/null" EXIT
wait
