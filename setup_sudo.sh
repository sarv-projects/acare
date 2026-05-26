#!/bin/bash
echo 'sarvesh' | sudo -S bash -c 'echo "sarvesh ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/sarvesh && chmod 440 /etc/sudoers.d/sarvesh'
echo "NOPASSWD configured"
