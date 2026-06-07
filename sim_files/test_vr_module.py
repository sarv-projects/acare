"""
Test Elechouse Voice Recognition V3 module over UART.
Run on Pi: python3 test_vr_module.py
"""
import serial
import time

PORTS = ['/dev/ttyAMA0', '/dev/ttyAMA10', '/dev/serial0']

# Elechouse VR V3 protocol:
# Send: AA [len] [cmd] [data...] [checksum]
# AA 37 03 00 00 00 = check-busy command
CHECK_CMD = bytes([0xAA, 0x37, 0x03, 0x00, 0x00, 0x00])

for port in PORTS:
    try:
        print(f"Trying {port} at 9600 baud...")
        s = serial.Serial(port, 9600, timeout=2)
        time.sleep(0.3)
        s.write(CHECK_CMD)
        time.sleep(0.5)
        data = s.read(100)
        if data:
            print(f"  Response: {data.hex()}")
        else:
            print(f"  No response (module may be on different port or wiring issue)")
        s.close()
    except Exception as e:
        print(f"  Error: {e}")

print("Done.")
