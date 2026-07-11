// ACARE Phase 1 — Teensy SPI Slave Byte Echo Test
// Target: Teensy 4.1
// Echoes received_byte + 1 back to Pi5 master.
//
// Uses direct LPSPI4 register config for SLAVE mode.
// (Arduino SPI library has no native slave mode on Teensy 4.1)
//
// Wiring:
//   Pi5 GPIO11 (SCK)  → Teensy pin 13
//   Pi5 GPIO10 (MOSI) → Teensy pin 11
//   Pi5 GPIO9  (MISO) → Teensy pin 12
//   Pi5 GPIO8  (CS)   → Teensy pin 10
//   Pi5 GND           → Teensy GND
//
// Library needed: Teensyduino (board package for Teensy 4.1)
// No extra libraries required.

#include <SPI.h>

#define CS_PIN   10

// LPSPI4 register bit definitions (from imxrt.h, included by SPI.h)
volatile bool got_byte = false;
volatile uint8_t rx_val = 0;
uint8_t next_tx = 0x01;
uint32_t count = 0;

// Single ISR for both CS edges — use CHANGE trigger
void cs_change() {
  if (digitalReadFast(CS_PIN) == LOW) {
    // CS falling — Pi is about to start SCK.
    // Pre-load TX response byte into FIFO so it's ready.
    LPSPI4_TDR = next_tx;
  } else {
    // CS rising — transaction complete.
    // Read received byte from RX FIFO.
    if (LPSPI4_SR & LPSPI_SR_RDF) {
      rx_val = LPSPI4_RDR & 0xFF;
      got_byte = true;
    }
  }
}

void setup() {
  Serial.begin(115200);
  while (!Serial) ;
  delay(100);

  Serial.println("ACARE Phase 1 — SPI Slave Byte Echo (LPSPI4)");

  // Step 1: Enable module clock via CCM
  CCM_CCGR3 |= CCM_CCGR3_LPSPI4(CCM_CCGR_ON);

  // Step 2: Let SPI.begin() configure pin muxing (pins 10-13 → LPSPI4)
  // Then disable and reconfigure as slave
  SPI.begin();
  SPI.endTransaction();

  // Step 3: Direct LPSPI4 register config for SLAVE mode
  LPSPI4_CR = 0;                    // Disable while reconfiguring
  LPSPI4_CFGR1 = 0;                 // Clear MASTER bit (bit 4) → SLAVE mode
  LPSPI4_CCR = 0;                   // No prescaler — Pi provides SCK
  LPSPI4_FCR = 0;                   // No FIFO watermark

  // Re-enable with FIFOs cleared, slave mode
  LPSPI4_CR = LPSPI_CR_MEN | LPSPI_CR_RRF | LPSPI_CR_GRF
            | LPSPI_CR_DBGEN | LPSPI_CR_DOZEN;

  pinMode(CS_PIN, INPUT_PULLUP);

  // IMPORTANT: Use single CHANGE interrupt, NOT two separate attachInterrupt calls
  // (second call would override the first on same pin)
  attachInterrupt(digitalPinToInterrupt(CS_PIN), cs_change, CHANGE);

  Serial.println("Slave ready on pins 10-13, MODE0, 1MHz");
  Serial.println();
}

void loop() {
  if (!got_byte) return;
  got_byte = false;

  count++;

  // Compute response byte for NEXT Pi transaction
  next_tx = rx_val + 1;

  // Print to Serial
  Serial.print("#");
  Serial.print(count);
  Serial.print("  RX=0x");
  if (rx_val < 0x10) Serial.print("0");
  Serial.print(rx_val, HEX);
  Serial.print("  NEXT_TX=0x");
  if (next_tx < 0x10) Serial.print("0");
  Serial.print(next_tx, HEX);
  Serial.println();
}
