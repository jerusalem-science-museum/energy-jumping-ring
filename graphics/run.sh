#!/bin/bash

# ==============================================================================
# Jerusalem Science Museum - Energy & Jumping Ring Exhibit Launch Script
# System Python Deployment (Direct Launch)
# ==============================================================================

# Ensure the script runs from the directory it is located in
cd "$(dirname "$0")"

echo "=================================================="
echo " Starting JSM Exhibit: Energy - Jumping Ring      "
echo "=================================================="

# 1. Display & Screen Configuration (Museum Floor Standards)
# Prevents screen blanking, screensavers, and DPMS sleeping during museum hours
export DISPLAY=:0
xset s off      # Disable screen saver timeout
xset -dpms      # Disable Display Power Management Signaling
xset s noblank  # Prevent screen from short-term blanking

# 2. Permanent Execution & Crash Recovery Loop
# Keeps the exhibit running continuously on the floor. Restarts if crashed.
while true; do
    echo "[LAUNCH] Launching main.py using system python3..."
    python3 main.py
    
    EXIT_CODE=$?
    
    # Check if the program was manually and cleanly terminated (Exit Code 0)
    if [ $EXIT_CODE -eq 0 ]; then
        echo "[EXIT] Application closed normally by user. Terminating script."
        break
    else
        # Crash recovery phase - triggers alert and logs error code
        echo "[CRASH] Application exited unexpectedly (Code: $EXIT_CODE)."
        echo "[RECOVERY] Restarting exhibit loop in 3 seconds..."
        sleep 3
    fi
done