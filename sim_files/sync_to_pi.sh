#!/bin/bash
# Sync active ACARE packages from Windows to Pi over SSH.
# Run from PowerShell: scp this file to Pi, then execute.
# Or just use the scp commands below directly.

PI="acare@10.12.133.174"
SRC="C:\Users\Sonali\Desktop\ACARE\acare_software_final"

echo "Syncing ACARE packages to Pi..."

for pkg in acare_bringup acare_msgs acare_planner acare_safety acare_logging acare_vision acare_voice acare_auth acare_dialogue acare_embedded_interface acare_admin; do
    echo "  $pkg..."
    scp -r -o StrictHostKeyChecking=no "$SRC\\$pkg" $PI:~/acare_ws/src/
done

echo "Syncing models..."
scp -o StrictHostKeyChecking=no "$SRC\\models\\acare_v26.onnx" $PI:~/acare_ws/src/models/ 2>/dev/null

echo "Done."
