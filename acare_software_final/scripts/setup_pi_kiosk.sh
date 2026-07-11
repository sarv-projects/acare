#!/bin/bash
# ACARE Raspberry Pi Kiosk Setup
# Run this ON THE RASPBERRY PI using: sudo bash setup_pi_kiosk.sh
# This script configures the Pi to automatically boot into the dashboard on the Waveshare LCD.

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo bash setup_pi_kiosk.sh)"
  exit 1
fi

echo "Installing minimal GUI and browser components..."
apt-get update
apt-get install -y xserver-xorg xserver-xorg-video-fbdev openbox xinit chromium-browser

echo "Creating dashboard backend service..."
cat << 'EOF' > /etc/systemd/system/acare-dashboard.service
[Unit]
Description=ACARE Demo Dashboard Backend
After=network.target

[Service]
User=acare
# Adjust this path if demo_dashboard.py is located elsewhere on the Pi
WorkingDirectory=/home/acare/acare_ws/src/ACARE/acare_software_final
ExecStart=/usr/bin/python3 scripts/demo_dashboard.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo "Creating kiosk UI service..."
# We use xinit to launch X11 and Chromium directly on the physical screen (tty1)
cat << 'EOF' > /etc/systemd/system/acare-kiosk.service
[Unit]
Description=ACARE Kiosk UI
After=systemd-user-sessions.service network.target acare-dashboard.service
Conflicts=getty@tty1.service

[Service]
User=acare
Environment=DISPLAY=:0
# Launch xinit -> chromium in kiosk mode. We disable DPMS (screen blanking).
ExecStart=/usr/bin/xinit /usr/bin/chromium-browser --kiosk --no-sandbox --disable-infobars --window-position=0,0 --window-size=1024,600 http://localhost:8000 -- :0 -s 0 dpms -keeptty vt1
Restart=always
RestartSec=5
StandardInput=tty
TTYPath=/dev/tty1
TTYReset=yes
TTYVHangup=yes

[Install]
WantedBy=graphical.target
EOF

echo "Enabling services..."
systemctl daemon-reload
# Disable the console login prompt so X11 can take over the screen
systemctl disable getty@tty1.service
systemctl enable acare-dashboard.service
systemctl enable acare-kiosk.service

echo ""
echo "=========================================================="
echo "Setup complete! The Pi is now configured as a Kiosk."
echo "The dashboard will automatically appear on the LCD when the Pi boots."
echo ""
echo "To start it right now without rebooting, run:"
echo "  sudo systemctl start acare-dashboard"
echo "  sudo systemctl start acare-kiosk"
echo "=========================================================="
