#!/usr/bin/env python3
"""
ACARE SPI Validation — Phase 1: Basic Byte Test
Target: Raspberry Pi 5 (SPI Master)
Purpose: Verify raw SPI wiring, clock, CS, MOSI/MISO — NO structs, NO protocol

Install dependency if needed:
    sudo apt install python3-spidev
    # or: pip3 install spidev

Enable SPI on Pi5:
    sudo raspi-config → Interface Options → SPI → Enable
    # SPI device will appear as /dev/spidev0.0

Usage:
    python3 phase1_pi5_spi_master.py

What this script does:
    1. Opens /dev/spidev0.0 (SPI0, CE0 = BCM GPIO8 = Pi5 physical pin 24)
    2. Sends a sequence of test bytes one at a time
    3. Reads back the echo (Teensy returns received_byte + 1)
    4. Prints pass/fail for each transaction
    5. Reports overall wiring health

Wiring (MUST share GND between Pi5 and Teensy):
    Pi5 GPIO 11 (SPI0 CLK,  physical 23) → Teensy pin 13  (SCK)
    Pi5 GPIO 10 (SPI0 MOSI, physical 19) → Teensy pin 11  (MOSI)
    Pi5 GPIO  9 (SPI0 MISO, physical 21) → Teensy pin 12  (MISO)
    Pi5 GPIO  8 (SPI0 CE0,  physical 24) → Teensy pin 10  (CS)
    Pi5 GND     (physical  6 or any GND) → Teensy GND     (MANDATORY)

Logic level:
    Pi5 GPIO is 3.3V. Teensy 4.1 is 3.3V tolerant on SPI pins.
    Direct connection is safe — NO level shifter needed.
"""

import spidev
import time
import sys

# ── Configuration ─────────────────────────────────────────────────────────────

SPI_BUS      = 0          # /dev/spidev0.X
SPI_DEVICE   = 0          # /dev/spidevX.0  (CE0 = GPIO8)
SPI_SPEED_HZ = 1_000_000  # 1 MHz — conservative for initial bringup
                           # Raise to 5 MHz or 10 MHz once basic test passes
SPI_MODE     = 0          # MODE0: CPOL=0, CPHA=0 — MUST match Teensy sketch

DELAY_S      = 0.1        # 100 ms between transactions — Teensy has time to print


# ── Test byte sequences ───────────────────────────────────────────────────────

# Three test patterns chosen to catch common wiring faults:
#   0x55 = 0101_0101  — alternating bits, catches clock phase errors
#   0xAA = 1010_1010  — inverse of above
#   0x00, 0xFF        — all-low and all-high, catches stuck lines
#   0x01..0x0A        — incrementing, verifies sequential integrity

TEST_SEQUENCE = [
    0x55, 0xAA,                          # alternating bit patterns
    0x00, 0xFF,                          # stuck-line test
    0x01, 0x02, 0x03, 0x04, 0x05,       # incrementing counter
    0x10, 0x20, 0x40, 0x80,             # walking bit
    0xDE, 0xAD, 0xBE, 0xEF,            # recognisable pattern in logic analyser
]


def open_spi():
    spi = spidev.SpiDev()
    spi.open(SPI_BUS, SPI_DEVICE)
    spi.max_speed_hz = SPI_SPEED_HZ
    spi.mode         = SPI_MODE
    spi.bits_per_word = 8
    spi.no_cs        = False   # let spidev control CE0
    return spi


def send_byte(spi, tx_byte):
    """
    Send one byte, receive one byte.
    spi.xfer2([tx]) asserts CS, clocks 8 bits, deasserts CS.
    Returns list of one received byte.
    """
    rx = spi.xfer2([tx_byte])
    return rx[0]


def run_phase1():
    print("=" * 56)
    print(" ACARE Phase 1 — Pi5 SPI Master Basic Byte Test")
    print("=" * 56)
    print(f"  Bus:   /dev/spidev{SPI_BUS}.{SPI_DEVICE}")
    print(f"  Speed: {SPI_SPEED_HZ // 1000} kHz")
    print(f"  Mode:  {SPI_MODE}")
    print()

    try:
        spi = open_spi()
    except FileNotFoundError:
        print("ERROR: /dev/spidev0.0 not found.")
        print("  Run: sudo raspi-config → Interface Options → SPI → Enable")
        sys.exit(1)
    except PermissionError:
        print("ERROR: Permission denied on /dev/spidev0.0.")
        print("  Run: sudo usermod -aG spi $USER  then log out and back in")
        sys.exit(1)

    print(f"{'TX':>6}  {'RX':>6}  {'Expected RX':>12}  {'Result':>8}")
    print("-" * 42)

    pass_count  = 0
    fail_count  = 0
    stuck_zero  = 0
    stuck_ff    = 0

    for tx_byte in TEST_SEQUENCE:
        rx_byte = send_byte(spi, tx_byte)
        # Teensy echoes back (received_byte + 1)
        expected = (tx_byte + 1) & 0xFF

        ok = (rx_byte == expected)
        if ok:
            pass_count += 1
            result = "PASS"
        else:
            fail_count += 1
            result = "FAIL"

        if rx_byte == 0x00:
            stuck_zero += 1
        if rx_byte == 0xFF:
            stuck_ff += 1

        print(f"  0x{tx_byte:02X}  ->  0x{rx_byte:02X}   (expect 0x{expected:02X})   {result}")
        time.sleep(DELAY_S)

    spi.close()

    # ── Summary ──────────────────────────────────────────────────────────────
    print()
    print("=" * 42)
    print(f"  PASSED : {pass_count}/{len(TEST_SEQUENCE)}")
    print(f"  FAILED : {fail_count}/{len(TEST_SEQUENCE)}")
    print()

    if fail_count == 0:
        print("  ✓ All bytes match — SPI wiring is healthy")
        print("  ✓ MOSI: Pi5 → Teensy working")
        print("  ✓ MISO: Teensy → Pi5 working")
        print("  ✓ CS toggling correctly")
        print("  ✓ SPI MODE0 confirmed")
        print()
        print("  Ready to proceed to Phase 2 (struct packets).")
    else:
        print("  ✗ Failures detected. Diagnosis:")
        if stuck_zero == len(TEST_SEQUENCE):
            print("    → All RX = 0x00: MISO line stuck LOW or disconnected")
            print("      Check: Teensy pin 12 → Pi5 GPIO9")
        elif stuck_ff == len(TEST_SEQUENCE):
            print("    → All RX = 0xFF: MISO line stuck HIGH (possible pull-up)")
        elif fail_count == len(TEST_SEQUENCE):
            print("    → All bytes wrong bit pattern: likely wrong SPI MODE")
            print("      Try SPI_MODE = 1 or 3 on both sides")
        else:
            print("    → Intermittent failures: check GND connection")
            print("      or reduce SPI_SPEED_HZ (try 500_000)")
        print()
        print("  Do NOT proceed to Phase 2 until all bytes pass.")

    print("=" * 42)


if __name__ == "__main__":
    run_phase1()


# =============================================================================
# EXPECTED TERMINAL OUTPUT (when wiring is correct):
# =============================================================================
#
# ========================================================
#  ACARE Phase 1 — Pi5 SPI Master Basic Byte Test
# ========================================================
#   Bus:   /dev/spidev0.0
#   Speed: 1000 kHz
#   Mode:  0
#
#     TX      RX    Expected RX    Result
# ------------------------------------------
#   0x55  ->  0x56   (expect 0x56)   PASS
#   0xAA  ->  0xAB   (expect 0xAB)   PASS
#   0x00  ->  0x01   (expect 0x01)   PASS
#   0xFF  ->  0x00   (expect 0x00)   PASS   ← 0xFF+1 wraps to 0x00
#   0x01  ->  0x02   (expect 0x02)   PASS
#   ...
# ==========================================
#   PASSED : 17/17
#   FAILED : 0/17
#
#   ✓ All bytes match — SPI wiring is healthy
#   ✓ MOSI: Pi5 → Teensy working
#   ✓ MISO: Teensy → Pi5 working
#   ✓ CS toggling correctly
#   ✓ SPI MODE0 confirmed
#
#   Ready to proceed to Phase 2 (struct packets).
# ==========================================
