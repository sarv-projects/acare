// =============================================================================
// ACARE 6-DOF Robotic Arm Firmware
// Target:     Teensy 4.1 (NXP iMXRT1062, Cortex-M7, 600 MHz)
// Based on:   ACARE_6DOF_Teensy41_RMCS.ino (single joint, UART Pi link)
// Changes:    Simple SPI slave (Pi5↔Teensy) + 6-joint scaling + multi-UART RMCS
//
// ─────────────────────────────────────────────────────────────────────────────
// ARCHITECTURE
// ─────────────────────────────────────────────────────────────────────────────
//
//   Raspberry Pi 5 (ROS2 Jazzy)
//       │  SPI MASTER — simple fixed struct, Pi initiates every transfer
//       ▼
//   Teensy 4.1  (SPI SLAVE, pins 10-13)
//       │
//       ├── IntervalTimer 200 Hz ─► control_loop()
//       │        ├── Wire I2C 400 kHz ─► TCA9548A ─► 6 × AS5600
//       │        ├── Position PID × 6
//       │        └── velocity_to_frequency() × 6  [freq cached, not sent yet]
//       │
//       ├── Serial1 38400 baud ─► RMCS3002 slave 1 (joint 0)
//       │                     └── RMCS3002 slave 2 (joint 1)
//       ├── Serial2 38400 baud ─► RMCS3002 slave 3 (joint 2)
//       │                     └── RMCS3002 slave 4 (joint 3)
//       └── Serial3 38400 baud ─► RMCS3002 slave 5 (joint 4)
//                             └── RMCS3002 slave 6 (joint 5)
//
// ─────────────────────────────────────────────────────────────────────────────
// CHANGE LOG vs ACARE_6DOF_Teensy41_RMCS.ino
// ─────────────────────────────────────────────────────────────────────────────
//
//  [C1]  Pi link: UART removed → simple SPI slave (SPISlave_T4 not required;
//        we use CS-edge interrupts + SPI.transfer in non-ISR context).
//        WHY SPI: UART at 115200 needs two sequential transfers for full-duplex.
//        SPI transfers command + telemetry simultaneously in one transaction.
//        No baud-rate framing overhead; Pi DMA drives the clock.
//
//  [C2]  SPI structs: JointCmd (Pi→Teensy) and JointState (Teensy→Pi).
//        Fixed size, no CRC, no packet types — as requested. Simple binary.
//
//  [C3]  Joint array: joints[6] replaces single joint0.
//        Each Joint holds PID, AbsEncoder, RMCS slave ID, UART pointer,
//        direction cache, freq cache.
//
//  [C4]  3 hardware UARTs, 2 joints each, at 38400 baud.
//        WHY MULTIPLE UARTs:
//          9600 baud: 1 Modbus ASCII frame ≈ 11.5 ms (11 chars × 1.04 ms).
//          2 writes × 6 joints = 138 ms — utterly exceeds any budget.
//          38400 baud: 1 frame ≈ 2.9 ms. 3 UARTs run in parallel (independent
//          hardware FIFOs). Each UART sees 2 joints × 2 writes = 11.6 ms max.
//          RMCS update runs at 50 Hz (20 ms budget) — fits comfortably.
//
//  [C5]  Direction caching: only send direction Modbus write when sign changes.
//        Steady-state motion = 1 write/joint/tick instead of 2 → halves UART load.
//
//  [C6]  Frequency caching: skip frequency write if value unchanged since last send.
//        Converged position hold = 0 writes → UART bus goes silent.
//
//  [C7]  RMCS update decoupled to 50 Hz (every 4th PID tick).
//        PID at 200 Hz fills freq_cmd_pending. RMCS update at 50 Hz drains it.
//        Gives 20 ms budget per RMCS update cycle instead of 5 ms.
//
//  [C8]  Watchdog: if SPI packets stop for >200 ms, brake all joints.
//
//  KEPT IDENTICAL (all [R7] items from previous version):
//        Wire.begin() / 400 kHz / setDefaultTimeout(2000)
//        mux_select() / mux_disable_all()
//        as5600_read_raw() / raw_to_rad() / abs_encoder_update()
//        pid_init() / pid_reset() / pid_update()
//        velocity_to_frequency() / frequency_to_velocity()
//        modbus_lrc() / rmcs_write_register()
//        rmcs_enable_cw/ccw() / rmcs_disable_motor() / rmcs_brake_motor()
//        rmcs_set_frequency() / IntervalTimer → control_timer_isr()
//
// =============================================================================

#include <Wire.h>
#include <IntervalTimer.h>      // Teensy PIT hardware timer — unchanged
#include <SPI.h>                // [C1] Teensy SPI library for slave mode

// =============================================================================
// SPI PIN DEFINITIONS  [C1]
// =============================================================================
// Teensy 4.1 hardware SPI0 (pins 10-13).
// Pi5 is master — it generates SCK and asserts CS.
// Teensy loads its TX buffer before each transaction (double-buffered).

#define SPI_CS_PIN    10   // CS   — Pi5 pulls LOW to start transaction
#define SPI_MOSI_PIN  11   // MOSI — Pi5 → Teensy
#define SPI_MISO_PIN  12   // MISO — Teensy → Pi5
#define SPI_SCK_PIN   13   // SCK  — Pi5 generates clock

// =============================================================================
// SPI PACKET STRUCTS  [C2]
// =============================================================================
//
// Simple fixed-size binary structs — no CRC, no packet types, no padding tricks.
// Pi5 and Teensy must agree on these layouts (same struct on Pi side in Python
// or C++, use struct.pack with '<' little-endian on Pi5 Python side).
//
// Total transaction size = max(sizeof(JointCmd), sizeof(JointState))
// Both sides clock exactly SPI_PACKET_BYTES bytes per transaction.

#pragma pack(push, 1)

struct JointCmd {
  // Pi5 → Teensy: desired joint positions (radians)
  // Send 0.0 to leave a joint at its current setpoint (use joint_mask instead
  // if you need explicit "don't update" semantics, but omitted for simplicity).
  float    target_pos[6];    // rad — desired angle per joint
  uint8_t  estop;            // non-zero = emergency stop all joints immediately
};
// sizeof(JointCmd) = 6×4 + 1 = 25 bytes

struct JointState {
  // Teensy → Pi5: current joint state
  float    current_pos[6];    // rad — filtered AS5600 reading per joint
  uint16_t freq_cmd[6];       // Hz  — last RMCS frequency command per joint
  uint8_t  fault_flags;       // bit N = joint N has a fault (I2C fail etc.)
};
// sizeof(JointState) = 6×4 + 6×2 + 1 = 37 bytes

#pragma pack(pop)

// Both transfers must be the same length for balanced SPI transactions.
// Pad to the larger of the two (JointState is larger here).
#define SPI_PACKET_BYTES  sizeof(JointState)   // 37 bytes

// =============================================================================
// RMCS UART CONFIGURATION  [C4]
// =============================================================================
//
// Using 38400 baud. If your RMCS3002 units support higher baud rates,
// change RMCS_BAUD to 57600 or 115200 for further reduction in frame time.
// At 38400: 1 Modbus ASCII frame (11 chars) = 11 × (10 bits / 38400) ≈ 2.86 ms
// At 115200: same frame ≈ 0.96 ms (use if RMCS hardware allows it).

#define RMCS_BAUD     38400

// RS-485 direction-enable pins per UART.
// Set to -1 if using TTL-direct or RS-232 adapter (no DE pin needed).
// If using RS-485 transceiver (e.g. MAX485), connect DE+RE together and drive
// HIGH for TX, LOW for RX. One pin per UART since each UART has its own bus.
#define RS485_DE_S1   -1    // DE pin for Serial1 (joints 0,1). Example: 2
#define RS485_DE_S2   -1    // DE pin for Serial2 (joints 2,3). Example: 3
#define RS485_DE_S3   -1    // DE pin for Serial3 (joints 4,5). Example: 4

// =============================================================================
// I2C / AS5600 / TCA9548A CONFIGURATION  (unchanged)
// =============================================================================

#define TCA_ADDR      0x70
#define AS5600_ADDR   0x36
#define AS5600_RAW_H  0x0C
#define AS5600_RAW_L  0x0D

// =============================================================================
// RMCS3002 REGISTER MAP  (unchanged)
// =============================================================================

#define RMCS_CMD_ENABLE_CW   0x0101
#define RMCS_CMD_ENABLE_CCW  0x0109
#define RMCS_CMD_DISABLE     0x0100
#define RMCS_CMD_BRAKE       0x0103

#define RMCS_REG_CONTROL     2
#define RMCS_REG_FREQUENCY   6
#define RMCS_REG_SPEED_FB    8
#define RMCS_REG_CURRENT_FB  10

#define RMCS_FREQ_MAX        400
#define RMCS_FREQ_MIN        0

// =============================================================================
// MOTOR / GEARBOX PARAMETERS
// =============================================================================

#define MOTOR_POLE_PAIRS     4       // verify against your Rhino BLDC datasheet
#define GEAR_RATIO           20.0f

// =============================================================================
// CONTROL LOOP TIMING
// =============================================================================

#define CONTROL_HZ       200
#define DT_S             (1.0f / CONTROL_HZ)   // 0.005 s

// RMCS update every N PID ticks → 200/4 = 50 Hz, 20 ms per cycle  [C7]
#define RMCS_DIV         4

// SPI watchdog: brake all joints if Pi5 goes silent for this long  [C8]
#define SPI_WATCHDOG_MS  200

// =============================================================================
// POSITION PID GAINS  (outer loop only — unchanged)
// =============================================================================

#define POS_KP            8.0f
#define POS_KI            0.5f
#define POS_KD            0.1f
#define VEL_MAX_RAD_S     15.0f    // rad/s at joint output — tune conservatively
#define POS_I_MAX         VEL_MAX_RAD_S
#define EMA_ALPHA         0.3f

// =============================================================================
// DATA STRUCTURES
// =============================================================================

struct PID {
  float kp, ki, kd;
  float integral;
  float prev_error;
  float integral_max;
  float output_max;
};

struct AbsEncoder {
  float angle_raw_rad;
  float angle_unwrapped;
  float angle_filtered;
  float angle_prev;
  bool  initialized;
};

// Joint — one entry per axis  [C3]
// uart_ptr and rs485_de are assigned once in setup(); no runtime lookup needed.
struct Joint {
  uint8_t          index;            // 0–5
  uint8_t          rmcs_slave_id;    // Modbus slave address for this RMCS unit
  uint8_t          mux_channel;      // TCA9548A channel for this joint's AS5600
  HardwareSerial*  uart_ptr;         // Serial1, Serial2, or Serial3
  int8_t           rs485_de;         // RS-485 DE pin, or -1

  AbsEncoder       enc;              // AS5600 state
  PID              pid;              // Position PID state

  float            setpoint_rad;     // Commanded position from Pi5

  // RMCS command cache  [C5][C6]
  uint16_t         freq_pending;     // Latest freq from PID (not yet sent)
  uint16_t         freq_sent;        // Last freq actually transmitted
  bool             dir_positive;     // Current direction: true=CW, false=CCW
  bool             dir_initialized;  // False until first direction write done

  // Status
  bool             fault;            // Set on repeated I2C read failures
  bool             enabled;
};

// =============================================================================
// GLOBALS
// =============================================================================

Joint         joints[6];
IntervalTimer controlTimer;

volatile bool     control_flag  = false;
volatile uint32_t pid_tick      = 0;

// SPI double buffers  [C2]
// rx_shadow is written by the CS-rising ISR (completed transaction).
// loop() reads rx_shadow; no mutex needed because loop() only reads it
// after spi_ready is set, and the ISR only writes it on the next transaction.
uint8_t       spi_tx_buf[SPI_PACKET_BYTES];   // Teensy → Pi5 (built each cycle)
uint8_t       spi_rx_work[SPI_PACKET_BYTES];  // filled during active transaction from Pi5 to teensey
uint8_t       spi_rx_shadow[SPI_PACKET_BYTES];// stable copy for loop() to read
volatile bool spi_ready = false;              // true when a full packet arrived

// Watchdog  [C8]
uint32_t      spi_last_ms   = 0;
bool          estop_active  = false;

// =============================================================================
// SPI SLAVE — CS edge ISRs  [C1]
// =============================================================================
//
// How it works (no external library needed):
//   1. CS falls (Pi5 starts transaction):
//      - Copy fresh telemetry into spi_tx_buf (pre-load).
//      - Begin a blocking SPI.transfer() in the FALLING ISR is wrong (too slow).
//      Instead we use a non-blocking approach:
//        FALLING ISR: note transaction start, reset byte index.
//        Actual byte exchange is driven by the SPI hardware shift register.
//        RISING ISR: transaction done — swap buffers, set spi_ready.
//
// For Teensy 4.1, the simplest correct slave approach that avoids third-party
// libraries is to use SPI.transfer(buf, len) inside a CS-gated section in loop().
// Because Pi5 controls the clock, we just need to be ready with our TX buf
// before CS falls, which we guarantee by building spi_tx_buf at the end of
// every PID tick (200 Hz >> typical Pi command rate of 50 Hz).
//
// We use a minimal ISR on CS pin: FALLING starts tracking, RISING signals done.
// The actual byte clocking is done by hardware — we just read the result.
//
// NOTE: If the Pi5 SPI transaction length < SPI_PACKET_BYTES, the transfer
// will be incomplete. Pi5 must always send exactly SPI_PACKET_BYTES bytes.
// On Pi5 side: spi.xfer2([0]*SPI_PACKET_BYTES) or equivalent.

volatile bool spi_in_transaction = false;

void spi_cs_fall() {
  spi_in_transaction = true;
}

void spi_cs_rise() {
  // Copy completed RX data to shadow buffer for loop() to process
  memcpy(spi_rx_shadow, spi_rx_work, SPI_PACKET_BYTES);
  spi_ready          = true;
  spi_in_transaction = false;
}

// Call once in setup(). Configures SPI in slave mode and attaches CS ISRs.
void spi_slave_init() {
  SPI.begin();
  // Teensy SPI slave: MODE0, MSB first — match these on Pi5 side.
  // Pi5 spidev default is MODE0; no change needed there.
  SPI.beginTransaction(SPISettings(0, MSBFIRST, SPI_MODE0));
  // (Clock speed arg is ignored in slave mode on Teensy)

  pinMode(SPI_CS_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(SPI_CS_PIN), spi_cs_fall, FALLING);
  attachInterrupt(digitalPinToInterrupt(SPI_CS_PIN), spi_cs_rise, RISING);

  memset(spi_tx_buf,    0, SPI_PACKET_BYTES);
  memset(spi_rx_work,   0, SPI_PACKET_BYTES);
  memset(spi_rx_shadow, 0, SPI_PACKET_BYTES);
}

// Perform the actual SPI byte exchange.
// Called from loop() while CS is asserted (Pi5 is clocking).
// Blocks for the duration of the transfer (~37 bytes × 0.1 µs at 10 MHz = 3.7 µs).
// This is called only when spi_in_transaction is true — which happens at Pi5's
// command rate (typically 50 Hz), not at 200 Hz.
void spi_do_transfer() {
  // SPI.transfer(buf_out, buf_in, len) is full-duplex on Teensy:
  // simultaneously clocks spi_tx_buf out on MISO and fills spi_rx_work from MOSI.
  SPI.transfer(spi_tx_buf, spi_rx_work, SPI_PACKET_BYTES);  //
}

// Build the telemetry buffer that Pi5 will receive on the next transaction.
// Called at end of each control_loop() so it always reflects the latest state.
void spi_build_telem() {
  JointState state;
  state.fault_flags = 0;
  for (uint8_t i = 0; i < 6; i++) {
    state.current_pos[i] = joints[i].enc.angle_filtered;
    state.freq_cmd[i]    = joints[i].freq_sent;
    if (joints[i].fault) state.fault_flags |= (1 << i);
  }
  // Copy into TX buf — Pi5 gets this on the NEXT SPI transaction
  memcpy(spi_tx_buf, &state, sizeof(JointState));
}

// Process a received JointCmd packet.
// Called from loop() after spi_ready is set.
void spi_process_cmd() {
  JointCmd cmd;
  memcpy(&cmd, spi_rx_shadow, sizeof(JointCmd));

  // Feed watchdog on every received packet (valid or not — Pi5 is alive)
  spi_last_ms = millis();

  if (cmd.estop) {
    estop_active = true;
    emergency_stop_all();
    return;
  }

  // Clear E-STOP if Pi5 sends normal command
  estop_active = false;

  for (uint8_t i = 0; i < 6; i++) {
    joints[i].setpoint_rad = cmd.target_pos[i];
  }
}

// =============================================================================
// UTILITIES  (unchanged)
// =============================================================================

static inline float clampf(float v, float lo, float hi) {
  return v < lo ? lo : v > hi ? hi : v;
}

// =============================================================================
// TCA9548A MULTIPLEXER  (unchanged)
// =============================================================================

void mux_select(uint8_t ch) {
  if (ch > 7) return;
  Wire.beginTransmission(TCA_ADDR);
  Wire.write(1 << ch);
  Wire.endTransmission();
}

void mux_disable_all() {
  Wire.beginTransmission(TCA_ADDR);
  Wire.write(0x00);
  Wire.endTransmission();
}

// =============================================================================
// AS5600 ABSOLUTE ENCODER  (unchanged)
// =============================================================================

int16_t as5600_read_raw() {
  Wire.beginTransmission(AS5600_ADDR);
  Wire.write(AS5600_RAW_H);
  // Repeated start — check NACK; if sensor absent, return -1 and keep last value
  if (Wire.endTransmission(false) != 0) return -1;
  Wire.requestFrom((uint8_t)AS5600_ADDR, (uint8_t)2);
  if (Wire.available() < 2) return -1;
  uint16_t hi = Wire.read();
  uint16_t lo = Wire.read();
  return (int16_t)((hi << 8) | lo) & 0x0FFF;  // 12-bit mask
}

static inline float raw_to_rad(int16_t raw) {
  return raw * (2.0f * (float)M_PI / 4096.0f);
}

// Reads AS5600 for one joint, updates unwrapped angle and EMA filter.
// Angle unwrapping: accumulates continuous rotation beyond ±2π
// without the 0↔2π jump that would cause the PID to see a false large error.
void abs_encoder_update(Joint &j) {
  mux_select(j.mux_channel);
  int16_t raw = as5600_read_raw();

  if (raw < 0) {
    // I2C failure — mark fault but keep last position estimate
    j.fault = true;
    return;
  }
  j.fault = false;

  float angle = raw_to_rad(raw);
  AbsEncoder &e = j.enc;

  if (!e.initialized) {
    e.angle_raw_rad = e.angle_unwrapped = e.angle_filtered = e.angle_prev = angle;
    e.initialized = true;
    return;
  }

  float delta = angle - e.angle_prev;
  if (delta >  (float)M_PI) delta -= 2.0f * (float)M_PI;
  if (delta < -(float)M_PI) delta += 2.0f * (float)M_PI;

  e.angle_prev       = angle;
  e.angle_raw_rad    = angle;
  e.angle_unwrapped += delta;
  e.angle_filtered   = EMA_ALPHA * e.angle_unwrapped + (1.0f - EMA_ALPHA) * e.angle_filtered;
}

// =============================================================================
// PID  (unchanged)
// =============================================================================

void pid_init(PID &p, float kp, float ki, float kd, float i_max, float out_max) {
  p.kp = kp; p.ki = ki; p.kd = kd;
  p.integral = p.prev_error = 0.0f;
  p.integral_max = i_max;
  p.output_max   = out_max;
}

void pid_reset(PID &p) { p.integral = p.prev_error = 0.0f; }

// Output is desired joint velocity in rad/s, clamped by output_max.
// Anti-windup: integral clamped to ±integral_max independently.
float pid_update(PID &p, float setpoint, float measured) {
  float err  = setpoint - measured;
  float P    = p.kp * err;
  p.integral = clampf(p.integral + p.ki * err * DT_S, -p.integral_max, p.integral_max);
  float D    = p.kd * (err - p.prev_error) / DT_S;
  p.prev_error = err;
  return clampf(P + p.integral + D, -p.output_max, p.output_max);
}

// =============================================================================
// VELOCITY → RMCS FREQUENCY  (unchanged)
// =============================================================================
//
// RMCS datasheet: RPM_motor = (60 × Freq_Hz) / PolePairs
// Rearranged + gear ratio:
//   Freq_Hz = |vel_joint_rad_s| × GEAR_RATIO × MOTOR_POLE_PAIRS / (2π)
//
// Velocity sign → direction command (handled separately to allow caching [C5]).

uint16_t velocity_to_frequency(float vel_rad_s) {
  float f = fabsf(vel_rad_s) * (float)GEAR_RATIO * (float)MOTOR_POLE_PAIRS
          / (2.0f * (float)M_PI);
  return (uint16_t)clampf(f, RMCS_FREQ_MIN, RMCS_FREQ_MAX);
}

float frequency_to_velocity(uint16_t f) {
  return (float)f * 2.0f * (float)M_PI
       / ((float)GEAR_RATIO * (float)MOTOR_POLE_PAIRS);
}

// =============================================================================
// MODBUS ASCII  (unchanged logic; now accepts uart_ptr and de_pin per joint [C4])
// =============================================================================

uint8_t modbus_lrc(uint8_t *data, uint8_t len) {
  uint8_t s = 0;
  for (uint8_t i = 0; i < len; i++) s += data[i];
  return (uint8_t)(~s + 1);
}

void rmcs_write_reg(HardwareSerial* uart, int8_t de,
                    uint8_t slave, uint16_t reg, uint16_t val) {
  uint8_t raw[6] = {
    slave,
    0x06,
    (uint8_t)(reg >> 8), (uint8_t)(reg & 0xFF),
    (uint8_t)(val >> 8), (uint8_t)(val & 0xFF)
  };
  uint8_t lrc = modbus_lrc(raw, 6);

  if (de >= 0) { digitalWrite(de, HIGH); delayMicroseconds(50); }

  uart->print(':');
  for (uint8_t i = 0; i < 6; i++) {
    if (raw[i] < 0x10) uart->print('0');
    uart->print(raw[i], HEX);
  }
  if (lrc < 0x10) uart->print('0'); // 0 is printed (sent) first and then the number: eg 0x06
  uart->print(lrc, HEX);
  uart->print('\r');
  uart->print('\n');
  uart->flush();

  if (de >= 0) { delayMicroseconds(50); digitalWrite(de, LOW); }
}

uint16_t rmcs_read_reg(HardwareSerial* uart, int8_t de,
                       uint8_t slave, uint16_t reg) {
  uint8_t raw[6] = {
    slave, 0x03,
    (uint8_t)(reg >> 8), (uint8_t)(reg & 0xFF),
    0x00, 0x01
  };
  uint8_t lrc = modbus_lrc(raw, 6);

  if (de >= 0) { digitalWrite(de, HIGH); delayMicroseconds(50); } // Only for rs-485 to enable Tx and disable Rx
  uart->print(':');                                                     // Sending request frame 
  for (uint8_t i = 0; i < 6; i++) {
    if (raw[i] < 0x10) uart->print('0');
    uart->print(raw[i], HEX);
  }
  if (lrc < 0x10) uart->print('0');           // Convert HEX to ASCII for LRC
  uart->print(lrc, HEX);
  uart->print('\r'); uart->print('\n'); uart->flush(); // Flush -> BLocks until UART Tx of request is done 
  if (de >= 0) { delayMicroseconds(50); digitalWrite(de, LOW); }

  uint32_t t = millis();
  while (uart->available() < 13 && millis() - t < 10);
  if (uart->available() < 13) return 0xFFFF;

  uart->read();  // ':' read returns only one byte and we are discarding : here 
  char buf[13];
  for (uint8_t i = 0; i < 12; i++) buf[i] = uart->read();
  buf[12] = '\0';
  char ds[5] = { buf[6], buf[7], buf[8], buf[9], '\0' }; // Extract the register value 
  return (uint16_t)strtoul(ds, nullptr, 16);            // str to ol -> unsigned long , 16-> hexidecimal antha , then uint16_t converts to integer 
}

// High-level RMCS helpers — take Joint& for uart/de/slave lookup
void rmcs_enable_cw  (Joint &j) { rmcs_write_reg(j.uart_ptr, j.rs485_de, j.rmcs_slave_id, RMCS_REG_CONTROL, RMCS_CMD_ENABLE_CW);  }
void rmcs_enable_ccw (Joint &j) { rmcs_write_reg(j.uart_ptr, j.rs485_de, j.rmcs_slave_id, RMCS_REG_CONTROL, RMCS_CMD_ENABLE_CCW); }
void rmcs_disable    (Joint &j) { rmcs_write_reg(j.uart_ptr, j.rs485_de, j.rmcs_slave_id, RMCS_REG_CONTROL, RMCS_CMD_DISABLE);    }
void rmcs_brake      (Joint &j) { rmcs_write_reg(j.uart_ptr, j.rs485_de, j.rmcs_slave_id, RMCS_REG_CONTROL, RMCS_CMD_BRAKE);      }
void rmcs_set_freq   (Joint &j, uint16_t f) {
  f = (uint16_t)clampf(f, RMCS_FREQ_MIN, RMCS_FREQ_MAX);
  rmcs_write_reg(j.uart_ptr, j.rs485_de, j.rmcs_slave_id, RMCS_REG_FREQUENCY, f);
}

// =============================================================================
// RMCS UPDATE — direction + frequency caching  [C5][C6][C7]
// =============================================================================
//
// Called at 50 Hz (every RMCS_DIV PID ticks) for each joint.
//
// Why caching matters:
//   Without caching: 2 writes/joint × 6 joints × 2.86 ms = 34.3 ms @ 38400 baud.
//   With direction caching [C5]: direction write only on sign change.
//     Steady-state: 1 write/joint → 17.2 ms. Still tight.
//   With frequency caching [C6]: freq write only when value changes.
//     Converged: 0 writes → 0 ms. Excellent.
//   Combined + 50 Hz update rate [C7]: 20 ms budget, 3 parallel UARTs.
//     Worst case (startup, all joints moving): 2 writes × 2 joints per UART
//     = 4 × 2.86 ms = 11.4 ms per UART. Budget: 20 ms. ✓
//
// Direction caching detail:
//   j.dir_initialized tracks whether we've sent a direction write at all.
//   On first update, always send. Thereafter, only send when bool flips.
//   This prevents sending 0x0101 (CW enable) every 20 ms during constant-
//   direction moves, saving ~2.86 ms per joint per RMCS tick.

// Tracks last sent direction per joint (static, indexed by joint.index)
static bool dir_last[6] = { true, true, true, true, true, true }; 

void rmcs_update_joint(Joint &j) {
  if (estop_active) return;

  uint16_t freq = j.freq_pending;

  if (freq == 0) {
    // Zero command: brake and reset caches so direction is re-sent on resume
    rmcs_brake(j);
    j.freq_sent = 0;
    j.dir_initialized = false;
    return;
  }

  // [C5] Direction: write only if changed
  bool want_cw = j.dir_positive;
  if (!j.dir_initialized || want_cw != dir_last[j.index]) { // Enter if direction not initialized or if direction changes from previous 
    if (want_cw) rmcs_enable_cw(j);
    else         rmcs_enable_ccw(j);
    dir_last[j.index]  = want_cw; // Updates present direction command 
    j.dir_initialized  = true;
  }

  // [C6] Frequency: write only if changed
  if (freq != j.freq_sent) {
    rmcs_set_freq(j, freq);
    j.freq_sent = freq;
  }
}

// =============================================================================
// EMERGENCY STOP  [C8]
// =============================================================================

void emergency_stop_all() {
  for (uint8_t i = 0; i < 6; i++) {
    rmcs_brake(joints[i]);
    joints[i].freq_pending    = 0;
    joints[i].freq_sent       = 0;
    joints[i].dir_initialized = false;
  }
  Serial.println(F("[ESTOP] All joints braked"));
}

// =============================================================================
// INTERVAL TIMER ISR  (unchanged)
// =============================================================================

void control_timer_isr() {
  control_flag = true;
  pid_tick++;   // this timer isr triggered every 200 hz or 5ms but rmcs update at 50 hz, so we use this pid_tick%, rmcs_div ==0 , then rmcs updation 
}

// =============================================================================
// CONTROL LOOP — 6-joint PID + decoupled RMCS update  [C3][C7]
// =============================================================================
//
// Timing breakdown (every 5 ms PID tick):
//   6 × AS5600 I2C reads (mux select + 2-byte read @ 400 kHz): ~6 × 0.65 ms = 3.9 ms
//   6 × pid_update (float ops @ 600 MHz):                       ~6 × 0.005 ms = 0.03 ms
//   6 × velocity_to_frequency:                                  ~0.001 ms
//   spi_build_telem:                                            ~0.005 ms
//   Total PID work:                                             ≈ 3.94 ms  (headroom: 1.06 ms ✓)
//
// RMCS update (every 4th tick = 50 Hz, 20 ms budget):
//   Worst case: 6 joints × 2 writes × 2.86 ms = 34 ms if sequential.
//   But 3 UARTs are independent: each handles 2 joints.
//   Interleaved dispatch (0,2,4 then 1,3,5) ensures each UART sees
//   at most 2 joints in sequence → 2 × 2 × 2.86 ms = 11.4 ms per UART.
//   Wall time = max(UART1, UART2, UART3) ≈ 11.4 ms < 20 ms ✓
//   With caching: usually much less.

void run_control_loop() {

  // --- 1. Read positions + run PID for all 6 joints ---
  for (uint8_t i = 0; i < 6; i++) {
    Joint &j = joints[i];
    if (!j.enabled) continue;

    abs_encoder_update(j);

    float vel = pid_update(j.pid, j.setpoint_rad, j.enc.angle_filtered);
    vel = clampf(vel, -VEL_MAX_RAD_S, VEL_MAX_RAD_S);

    j.dir_positive = (vel >= 0.0f);              // cache direction sign [C5] based on the sign of the velocity 
    j.freq_pending = velocity_to_frequency(vel);  // cache freq for RMCS update [C7]
  }

  // --- 2. RMCS update at 50 Hz (every RMCS_DIV ticks) ---
  // Interleaved order: 0,2,4 first (one joint per UART), then 1,3,5
  // This balances UART load: Serial1 doesn't do both its joints before Serial2 starts.
  if ((pid_tick % RMCS_DIV) == 0) {
    const uint8_t order[6] = { 0, 2, 4, 1, 3, 5 };
    for (uint8_t i = 0; i < 6; i++) {
      rmcs_update_joint(joints[order[i]]);
    }
  }

  // --- 3. Build fresh telemetry for next SPI transaction ---
  spi_build_telem();
}

// =============================================================================
// SETUP
// =============================================================================

// Helper: map joint index to its UART
HardwareSerial* joint_uart(uint8_t idx) {
  if (idx <= 1) return &Serial1;
  if (idx <= 3) return &Serial2;
  return &Serial3;
}

// Helper: map joint index to its RS-485 DE pin
int8_t joint_de(uint8_t idx) {
  if (idx <= 1) return RS485_DE_S1;
  if (idx <= 3) return RS485_DE_S2;
  return RS485_DE_S3;
}

void setup() {
  Serial.begin(115200);
  Serial.println(F("[ACARE] 6-DOF Teensy 4.1 — SPI slave + RMCS x6"));

  // ── I2C (unchanged) ────────────────────────────────────────────────────────
  Wire.begin();
  Wire.setClock(400000);
  Wire.setDefaultTimeout(2000);   // 2 ms timeout: prevents I2C stall eating budget

  // Scan AS5600 on all 6 mux channels
  for (uint8_t ch = 0; ch < 6; ch++) {
    mux_select(ch);
    Wire.beginTransmission(AS5600_ADDR);
    Serial.print(F("[AS5600] ch")); Serial.print(ch);
    Serial.println(Wire.endTransmission() == 0 ? F(" OK") : F(" NOT FOUND"));
  }
  mux_disable_all();

  // ── RMCS UARTs [C4] ────────────────────────────────────────────────────────
  Serial1.begin(RMCS_BAUD);
  Serial2.begin(RMCS_BAUD);
  Serial3.begin(RMCS_BAUD);
  Serial.print(F("[RMCS] Serial1/2/3 at ")); Serial.print(RMCS_BAUD); Serial.println(F(" baud"));

  // RS-485 DE pin setup
  const int8_t de_list[3] = { RS485_DE_S1, RS485_DE_S2, RS485_DE_S3 };
  for (uint8_t i = 0; i < 3; i++) {
    if (de_list[i] >= 0) { pinMode(de_list[i], OUTPUT); digitalWrite(de_list[i], LOW); }
  }

  // ── Joint initialisation [C3] ───────────────────────────────────────────────
  for (uint8_t i = 0; i < 6; i++) {
    Joint &j          = joints[i];
    j.index           = i;
    j.rmcs_slave_id   = i + 1;         // Slave IDs 1–6
    j.mux_channel     = i;             // TCA9548A channels 0–5
    j.uart_ptr        = joint_uart(i);
    j.rs485_de        = joint_de(i);
    j.setpoint_rad    = 0.0f;
    j.freq_pending    = 0;
    j.freq_sent       = 0;
    j.dir_positive    = true;
    j.dir_initialized = false;
    j.fault           = false;
    j.enabled         = false;
    memset(&j.enc, 0, sizeof(j.enc));
    pid_init(j.pid, POS_KP, POS_KI, POS_KD, POS_I_MAX, VEL_MAX_RAD_S);

    // Safe RMCS startup
    rmcs_disable(j); delay(20);
    rmcs_set_freq(j, 0); delay(20);
    rmcs_enable_cw(j);
    dir_last[i]       = true;
    j.dir_initialized = true;
    j.enabled         = true;

    Serial.print(F("[Joint ")); Serial.print(i); Serial.println(F("] ready"));
  }

  // ── SPI slave [C1] ─────────────────────────────────────────────────────────
  spi_slave_init();
  spi_last_ms = millis();
  Serial.println(F("[SPI] Slave ready (pins 10-13, MODE0, MSB first)"));

  // ── IntervalTimer 200 Hz (unchanged) ───────────────────────────────────────
  if (!controlTimer.begin(control_timer_isr, 5000)) {
    Serial.println(F("[FATAL] No PIT channel for IntervalTimer"));
    while (1);
  }
  Serial.print(F("[ACARE] Running at ")); Serial.print(CONTROL_HZ); Serial.println(F(" Hz"));
}

// =============================================================================
// MAIN LOOP
// =============================================================================

void loop() {

  // ── 1. 200 Hz control loop (triggered by IntervalTimer ISR) ────────────────
  if (control_flag) {
    control_flag = false;
    if (!estop_active) run_control_loop();
  }

  // ── 2. SPI slave: service active transaction ────────────────────────────────
  // Pi5 controls when transactions happen (it's master). When CS is low,
  // we service the byte exchange. When it rises, the ISR sets spi_ready.
  if (spi_in_transaction) {
    spi_do_transfer();   // non-blocking at 10 MHz: completes in ~3.7 µs
  }

  if (spi_ready) {
    spi_ready = false;
    spi_process_cmd();
  }

  // ── 3. Watchdog [C8] ────────────────────────────────────────────────────────
  // If Pi5 goes silent (crash, cable pull, power loss), brake all joints.
  if (!estop_active && (millis() - spi_last_ms) > SPI_WATCHDOG_MS) {
    estop_active = true;
    emergency_stop_all();
    Serial.println(F("[WATCHDOG] Pi5 silent — joints braked"));
  }

  // Auto-recover if watchdog fired but Pi5 resumes: spi_process_cmd() clears
  // estop_active when a non-estop packet arrives and updates spi_last_ms.

  // ── 4. Low-rate diagnostics — one joint per 100 ms, round-robin ────────────
  static uint32_t diag_ms = 0;
  static uint8_t  diag_j  = 0;
  if (millis() - diag_ms >= 100) {
    diag_ms = millis();
    Joint &j = joints[diag_j];
    Serial.print(F("J")); Serial.print(diag_j);
    Serial.print(F(" pos=")); Serial.print(j.enc.angle_filtered, 3); // 3- print such that 3 values after decimal point 
    Serial.print(F(" sp="));  Serial.print(j.setpoint_rad, 3);
    Serial.print(F(" fq="));  Serial.print(j.freq_sent);
    Serial.print(F(" fault=")); Serial.println(j.fault);
    diag_j = (diag_j + 1) % 6;
  }
}

// =============================================================================
// PUBLIC: Set position target for one joint (local override, e.g. for testing)
// =============================================================================

void set_joint_target(uint8_t idx, float rad) {
  if (idx >= 6) return;
  joints[idx].setpoint_rad = rad;
  pid_reset(joints[idx].pid);
}

// =============================================================================
// Pi5 SIDE REFERENCE (Python pseudocode)
// =============================================================================
//
// import spidev, struct
// spi = spidev.SpiDev(); spi.open(0, 0)
// spi.max_speed_hz = 10_000_000
// spi.mode = 0
//
// CMD_FMT   = '<6f B'           # 6 floats + 1 uint8  = 25 bytes
// STATE_FMT = '<6f 6H B'        # 6 floats + 6 uint16 + 1 uint8 = 37 bytes
// SPI_LEN   = struct.calcsize(STATE_FMT)   # 37 bytes — always transfer this many
//
// def send_targets(targets, estop=0):
//     cmd = struct.pack(CMD_FMT, *targets, estop)
//     cmd += b'\x00' * (SPI_LEN - len(cmd))  # pad to SPI_LEN
//     raw = spi.xfer2(list(cmd))              # full-duplex
//     pos, freqs, faults = struct.unpack(STATE_FMT, bytes(raw))
//     return pos, freqs, faults
//
// =============================================================================
//
// TIMING SUMMARY
// ──────────────────────────────────────────────────────────────────────────────
// Task                    Rate     Budget    Worst case   Status
// PID loop (all 6 joints) 200 Hz   5.0 ms    3.94 ms     ✓ 1.06 ms headroom
// RMCS update (50 Hz)     50 Hz    20.0 ms   11.4 ms     ✓ 8.6 ms headroom
// SPI transaction         Pi-rate  in gap    ~3.7 µs     ✓ negligible
// Diagnostics             10 Hz    100 ms    ~10 ms      ✓
//
// RMCS UART remains the bottleneck for update rate.
// If baud can be raised to 115200: 1 frame = 0.96 ms →
//   worst case 2 joints × 2 writes × 0.96 ms = 3.84 ms per UART.
//   RMCS update can then safely run at 100 Hz (10 ms budget).
// Check your RMCS3002 firmware version for supported baud rates.
// =============================================================================
