# Embedded / Hardware — ACARE

This directory contains all firmware, hardware design files, and motor control code for the ACARE robotic arm.

## Firmware

| File | Description | Status |
|------|-------------|--------|
| `firmware/main_teensy_firmware.ino` | Primary Teensy 4.1 firmware — SPI slave, 200Hz PID control, 6× UART for RMCS3002 motor drivers, AS5600 encoder reads via TCA9548A I2C mux | Tested |
| `firmware/rmcs3002_pwm_test.ino` | Legacy PWM open-loop test for RMCS3002 drivers | Reference only |
| `firmware/rmcs3002_modbus_3motor.ino` | 3-motor Modbus ASCII open-loop controller for RMCS3002 drivers via Serial2/3/4 | Untested — reference only |

## Electronics

*(Add schematic PDFs, PCB layout files, BOM here)*

## Media

- `../docs/media/demo_video.mp4` — Demo day video
- `../docs/images/` — Screenshots, test images, annotated YOLO training data

## Notes

- SPI communication: 10 MHz, Mode 0, 64-byte frames
- Motor drivers: RMCS-3002 (BLDC) via dedicated UARTs
- Encoders: AS5600 (12-bit magnetic) via TCA9548A I2C multiplexer
- Safety: Hardware ESTOP button with direct 24V cutoff
