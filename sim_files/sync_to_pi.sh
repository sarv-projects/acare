#!/bin/bash
# Sync active ACARE packages to Pi over SSH.
# Usage: PI="acare@<pi-ip>" ./sync_to_pi.sh

PI="${PI:-acare@pi}"
SRC="./acare_software_final"

echo "Syncing ACARE packages to $PI..."

for pkg in acare_bringup acare_msgs acare_planner acare_safety acare_logging acare_vision acare_voice acare_auth acare_dialogue acare_embedded_interface acare_admin; do
    echo "  $pkg..."
    scp -r -o StrictHostKeyChecking=no "$SRC/$pkg" "$PI:~/acare_ws/src/"
done

echo "Syncing models..."
scp -o StrictHostKeyChecking=no "$SRC/models/acare_v26.onnx" "$PI:~/acare_ws/src/models/" 2>/dev/null

echo "Done."
