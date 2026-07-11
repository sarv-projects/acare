// =============================================================================
// ACARE 6-DOF Robotic Arm Firmware
// Target:  Teensy 4.1 (NXP iMXRT1062, Cortex-M7, 600 MHz)
//
// ARCHITECTURE
//   Raspberry Pi 5 (ROS2 Jazzy)
//       │  SPI MASTER — fixed struct, Pi initiates every transfer
//       ▼
//   Teensy 4.1  (SPI SLAVE, pins 10-13)
//       │
//       ├── IntervalTimer 200 Hz ─► control_loop()
//       │        ├── Wire I2C 400 kHz ─► TCA9548A ─► 6 × AS5600
//       │        ├── Position PID × 6
//       │        └── velocity_to_frequency() × 6
//       │
//       ├── Serial1 38400 baud ─► RMCS3002 slave 1 (joint 0)  [dedicated]
//       ├── Serial2 38400 baud ─► RMCS3002 slave 2 (joint 1)  [dedicated]
//       ├── Serial3 38400 baud ─► RMCS3002 slave 3 (joint 2)  [dedicated]
//       ├── Serial4 38400 baud ─► RMCS3002 slave 4 (joint 3)  [dedicated]
//       ├── Serial5 38400 baud ─► RMCS3002 slave 5 (joint 4)  [dedicated]
//       ├── Serial6 38400 baud ─► RMCS3002 slave 6 (joint 5)  [dedicated]
//       ├── Serial7 — spare (future use)
//       └── Serial8 — spare (future use)
//
// With one dedicated UART per joint, all 6 RMCS frames fire in parallel.
// Worst-case wall time = 1 frame = 2.86 ms, so RMCS update runs at 100 Hz
// (every 2nd PID tick) with comfortable headroom. No interleaving needed.
// =============================================================================

#include <Wire.h>
#include <IntervalTimer.h>
#include <SPI.h>

// =============================================================================
// SPI PIN DEFINITIONS
// =============================================================================

#define SPI_CS_PIN    10   // CS   — Pi5 pulls LOW to start transaction
#define SPI_MOSI_PIN  11   // MOSI — Pi5 → Teensy
#define SPI_MISO_PIN  12   // MISO — Teensy → Pi5
#define SPI_SCK_PIN   13   // SCK  — Pi5 generates clock

// =============================================================================
// SPI PACKET STRUCTS
// =============================================================================
// Pi5 Python side: use struct.pack('<6f B', ...) for JointCmd (25 bytes)
// and struct.unpack('<6f 6H B', ...) for JointState (37 bytes).
// Always transfer SPI_PACKET_BYTES (37) bytes per transaction.

#pragma pack(push, 1)

struct JointCmd {
  float   target_pos[6];  // rad — desired angle per joint (Pi5 → Teensy)
  uint8_t estop;          // non-zero = emergency stop all joints
};
// sizeof(JointCmd) = 6×4 + 1 = 25 bytes

struct JointState {
  float    current_pos[6]; // rad — filtered AS5600 reading per joint (Teensy → Pi5)
  uint16_t freq_cmd[6];    // Hz  — last RMCS frequency command per joint
  uint8_t  fault_flags;    // bit N = joint N has a fault
};
// sizeof(JointState) = 6×4 + 6×2 + 1 = 37 bytes

#pragma pack(pop)

#define SPI_PACKET_BYTES  sizeof(JointState)   // 37 bytes

// =============================================================================
// RMCS UART CONFIGURATION
// =============================================================================
// One dedicated UART per joint (Serial1–Serial6). Serial7 and Serial8 spare.
// At 38400 baud: 1 Modbus ASCII frame (11 chars) ≈ 2.86 ms.
// All 6 UARTs are independent hardware FIFOs — frames fire in parallel.
//
// Teensy 4.1 UART pin map:
//   Serial1: TX=1,  RX=0   → Joint 0
//   Serial2: TX=8,  RX=7   → Joint 1
//   Serial3: TX=14, RX=15  → Joint 2
//   Serial4: TX=17, RX=16  → Joint 3
//   Serial5: TX=20, RX=21  → Joint 4
//   Serial6: TX=24, RX=25  → Joint 5
//   Serial7: TX=29, RX=28  → spare
//   Serial8: TX=35, RX=34  → spare

#define RMCS_BAUD     38400

// RS-485 DE pin per joint UART. Set -1 if using TTL-direct (no DE pin needed).
// If using RS-485 (e.g. MAX485): DE+RE tied together, HIGH=TX, LOW=RX.
#define RS485_DE_J0   -1
#define RS485_DE_J1   -1
#define RS485_DE_J2   -1
#define RS485_DE_J3   -1
#define RS485_DE_J4   -1
#define RS485_DE_J5   -1

// =============================================================================
// I2C / AS5600 / TCA9548A CONFIGURATION
// =============================================================================

#define TCA_ADDR      0x70
#define AS5600_ADDR   0x36
#define AS5600_RAW_H  0x0C
#define AS5600_RAW_L  0x0D

// =============================================================================
// RMCS3002 REGISTER MAP
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

#define MOTOR_POLE_PAIRS     4
#define GEAR_RATIO           20.0f

// =============================================================================
// PER-JOINT SOFT LIMITS (radians)
// =============================================================================
// These are safety limits enforced in firmware. Commands outside these ranges
// are clamped to prevent hardware damage. Values should match system.yaml
// arm.joint_limits_min/max but can be tightened for additional safety margin.

const float JOINT_LIMITS_MIN[6] = {
  -3.14159f,  // J0 base
  -2.35619f,  // J1 shoulder
  -2.09440f,  // J2 elbow
  -3.14159f,  // J3 wrist_1
  -3.14159f,  // J4 wrist_2
  -3.14159f   // J5 wrist_3
};

const float JOINT_LIMITS_MAX[6] = {
   3.14159f,  // J0 base
   2.35619f,  // J1 shoulder
   2.09440f,  // J2 elbow
   3.14159f,  // J3 wrist_1
   3.14159f,  // J4 wrist_2
   3.14159f   // J5 wrist_3
};

// =============================================================================
// CONTROL LOOP TIMING
// =============================================================================

#define CONTROL_HZ       200
#define DT_S             (1.0f / CONTROL_HZ)   // 0.005 s

// RMCS update every 2 PID ticks → 100 Hz, 10 ms budget per cycle.
// Worst case per UART: 1 joint × 2 writes × 2.86 ms = 5.72 ms < 10 ms ✓
#define RMCS_DIV         2

// Brake all joints if SPI packets stop for this long
#define SPI_WATCHDOG_MS  200

// =============================================================================
// POSITION PID GAINS
// =============================================================================

#define POS_KP            8.0f
#define POS_KI            0.5f
#define POS_KD            0.1f
#define VEL_MAX_RAD_S     15.0f
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

struct Joint {
  uint8_t          index;           // 0–5
  uint8_t          rmcs_slave_id;   // Modbus slave address (1–6)
  uint8_t          mux_channel;     // TCA9548A channel (0–5)
  HardwareSerial*  uart_ptr;        // Dedicated UART: Serial1–Serial6
  int8_t           rs485_de;        // RS-485 DE pin, or -1

  AbsEncoder       enc;
  PID              pid;

  float            setpoint_rad;    // Commanded position from Pi5

  // RMCS command caches — only write on change to minimise UART load
  uint16_t         freq_pending;    // Latest freq from PID (not yet sent)
  uint16_t         freq_sent;       // Last freq actually transmitted
  bool             dir_positive;    // true = CW, false = CCW
  bool             dir_initialized; // false until first direction write

  bool             fault;
  bool             enabled;
};

// =============================================================================
// GLOBALS
// =============================================================================

Joint         joints[6];
IntervalTimer controlTimer;

volatile bool     control_flag  = false;
volatile uint32_t pid_tick      = 0;

uint8_t       spi_tx_buf[SPI_PACKET_BYTES];
uint8_t       spi_rx_work[SPI_PACKET_BYTES];
uint8_t       spi_rx_shadow[SPI_PACKET_BYTES];
volatile bool spi_ready = false;

uint32_t      spi_last_ms  = 0;
bool          estop_active = false;

// =============================================================================
// SPI SLAVE
// =============================================================================
// CS-FALLING ISR: marks transaction active.
// CS-RISING ISR:  copies completed RX bytes to shadow buffer, signals loop().
// Actual byte exchange is driven by SPI hardware; loop() calls spi_do_transfer()
// while CS is held low. spi_tx_buf is rebuilt at the end of every PID tick
// (200 Hz) so Pi5 always reads fresh telemetry.

volatile bool spi_in_transaction = false;

void spi_cs_fall() {
  spi_in_transaction = true;
}

void spi_cs_rise() {
  memcpy(spi_rx_shadow, spi_rx_work, SPI_PACKET_BYTES);
  spi_ready          = true;
  spi_in_transaction = false;
}

void spi_slave_init() {
  // Configure LPSPI4 as SPI SLAVE (not master).
  // SPI.begin() defaults to master mode; we need to set the LPSPI control
  // register directly to enable slave mode.

  // 1. Enable module clock and configure pins via the standard SPI.begin
  SPI.begin();
  SPI.endTransaction();  // Release the bus config so we can reconfigure

  // 2. LPSPI4 direct register config for SLAVE mode
  LPSPI4_CR  = 0;                       // Disable module while configuring
  LPSPI4_CFGR1 = LPSPI_CFGR1_MASTER(0); // Clear MSTR bit → SLAVE mode
  LPSPI4_CCR = 0;                       // No clock config needed (Pi provides clock)
  LPSPI4_FCR = 0;                       // No FIFO watermark (single-word transfers)
  LPSPI4_CR  = LPSPI_CR_MEN | LPSPI_CR_RRF | LPSPI_CR_GRF
             | LPSPI_CR_DBGEN | LPSPI_CR_DOZEN;  // Enable + reset FIFOs

  pinMode(SPI_CS_PIN, INPUT);  // CS is input in slave mode — Pi drives it
  attachInterrupt(digitalPinToInterrupt(SPI_CS_PIN), spi_cs_fall, FALLING);
  attachInterrupt(digitalPinToInterrupt(SPI_CS_PIN), spi_cs_rise, RISING);

  memset(spi_tx_buf,    0, SPI_PACKET_BYTES);
  memset(spi_rx_work,   0, SPI_PACKET_BYTES);
  memset(spi_rx_shadow, 0, SPI_PACKET_BYTES);
}

void spi_do_transfer() {
  // Full-duplex: clocks spi_tx_buf out on MISO, fills spi_rx_work from MOSI.
  // ~3.7 µs at 10 MHz for 37 bytes.
  SPI.transfer(spi_tx_buf, spi_rx_work, SPI_PACKET_BYTES);
}

void spi_build_telem() {
  JointState state;
  state.fault_flags = 0;
  for (uint8_t i = 0; i < 6; i++) {
    state.current_pos[i] = joints[i].enc.angle_filtered;
    state.freq_cmd[i]    = joints[i].freq_sent;
    if (joints[i].fault) state.fault_flags |= (1 << i);
  }
  memcpy(spi_tx_buf, &state, sizeof(JointState));
}

void spi_process_cmd() {
  JointCmd cmd;
  memcpy(&cmd, spi_rx_shadow, sizeof(JointCmd));

  spi_last_ms = millis();  // feed watchdog

  if (cmd.estop) {
    estop_active = true;
    emergency_stop_all();
    return;
  }

  estop_active = false;
  for (uint8_t i = 0; i < 6; i++) {
    // Clamp setpoint to per-joint soft limits for safety
    joints[i].setpoint_rad = clampf(cmd.target_pos[i], JOINT_LIMITS_MIN[i], JOINT_LIMITS_MAX[i]);
  }
}

// =============================================================================
// UTILITIES
// =============================================================================

static inline float clampf(float v, float lo, float hi) {
  return v < lo ? lo : v > hi ? hi : v;
}

// =============================================================================
// TCA9548A MULTIPLEXER
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
// AS5600 ABSOLUTE ENCODER
// =============================================================================

int16_t as5600_read_raw() {
  Wire.beginTransmission(AS5600_ADDR);
  Wire.write(AS5600_RAW_H);
  if (Wire.endTransmission(false) != 0) return -1;
  Wire.requestFrom((uint8_t)AS5600_ADDR, (uint8_t)2);
  if (Wire.available() < 2) return -1;
  uint16_t hi = Wire.read();
  uint16_t lo = Wire.read();
  return (int16_t)((hi << 8) | lo) & 0x0FFF;  // 12-bit
}

static inline float raw_to_rad(int16_t raw) {
  return raw * (2.0f * (float)M_PI / 4096.0f);
}

void abs_encoder_update(Joint &j) {
  mux_select(j.mux_channel);
  int16_t raw = as5600_read_raw();

  if (raw < 0) {
    j.fault = true;
    return;  // keep last position estimate
  }
  j.fault = false;

  float angle = raw_to_rad(raw);
  AbsEncoder &e = j.enc;

  if (!e.initialized) {
    e.angle_raw_rad = e.angle_unwrapped = e.angle_filtered = e.angle_prev = angle;
    e.initialized = true;
    return;
  }

  // Unwrap: accumulate continuous rotation without 0↔2π jump
  float delta = angle - e.angle_prev;
  if (delta >  (float)M_PI) delta -= 2.0f * (float)M_PI;
  if (delta < -(float)M_PI) delta += 2.0f * (float)M_PI;

  e.angle_prev       = angle;
  e.angle_raw_rad    = angle;
  e.angle_unwrapped += delta;
  e.angle_filtered   = EMA_ALPHA * e.angle_unwrapped + (1.0f - EMA_ALPHA) * e.angle_filtered;
}

// =============================================================================
// PID
// =============================================================================

void pid_init(PID &p, float kp, float ki, float kd, float i_max, float out_max) {
  p.kp = kp; p.ki = ki; p.kd = kd;
  p.integral = p.prev_error = 0.0f;
  p.integral_max = i_max;
  p.output_max   = out_max;
}

void pid_reset(PID &p) { p.integral = p.prev_error = 0.0f; }

float pid_update(PID &p, float setpoint, float measured) {
  float err  = setpoint - measured;
  float P    = p.kp * err;
  p.integral = clampf(p.integral + p.ki * err * DT_S, -p.integral_max, p.integral_max);
  float D    = p.kd * (err - p.prev_error) / DT_S;
  p.prev_error = err;
  return clampf(P + p.integral + D, -p.output_max, p.output_max);
}

// =============================================================================
// VELOCITY → RMCS FREQUENCY
// =============================================================================
// RMCS datasheet: RPM_motor = (60 × Freq_Hz) / PolePairs
// Rearranged + gear ratio: Freq_Hz = |vel_rad_s| × GEAR_RATIO × POLE_PAIRS / (2π)
// Velocity sign → direction command (handled separately to allow caching).

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
// MODBUS ASCII
// =============================================================================

uint8_t modbus_lrc(uint8_t *data, uint8_t len) {
  uint8_t s = 0;
  for (uint8_t i = 0; i < len; i++) s += data[i];
  return (uint8_t)(~s + 1);
}

void rmcs_write_reg(HardwareSerial* uart, int8_t de,
                    uint8_t slave, uint16_t reg, uint16_t val) {
  uint8_t raw[6] = {
    slave, 0x06,
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
  if (lrc < 0x10) uart->print('0');
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

  if (de >= 0) { digitalWrite(de, HIGH); delayMicroseconds(50); }
  uart->print(':');
  for (uint8_t i = 0; i < 6; i++) {
    if (raw[i] < 0x10) uart->print('0');
    uart->print(raw[i], HEX);
  }
  if (lrc < 0x10) uart->print('0');
  uart->print(lrc, HEX);
  uart->print('\r'); uart->print('\n'); uart->flush();
  if (de >= 0) { delayMicroseconds(50); digitalWrite(de, LOW); }

  uint32_t t = millis();
  while (uart->available() < 13 && millis() - t < 10);
  if (uart->available() < 13) return 0xFFFF;

  uart->read();  // discard leading ':'
  char buf[13];
  for (uint8_t i = 0; i < 12; i++) buf[i] = uart->read();
  buf[12] = '\0';
  char ds[5] = { buf[6], buf[7], buf[8], buf[9], '\0' };
  return (uint16_t)strtoul(ds, nullptr, 16);
}

// High-level RMCS helpers
void rmcs_enable_cw  (Joint &j) { rmcs_write_reg(j.uart_ptr, j.rs485_de, j.rmcs_slave_id, RMCS_REG_CONTROL, RMCS_CMD_ENABLE_CW);  }
void rmcs_enable_ccw (Joint &j) { rmcs_write_reg(j.uart_ptr, j.rs485_de, j.rmcs_slave_id, RMCS_REG_CONTROL, RMCS_CMD_ENABLE_CCW); }
void rmcs_disable    (Joint &j) { rmcs_write_reg(j.uart_ptr, j.rs485_de, j.rmcs_slave_id, RMCS_REG_CONTROL, RMCS_CMD_DISABLE);    }
void rmcs_brake      (Joint &j) { rmcs_write_reg(j.uart_ptr, j.rs485_de, j.rmcs_slave_id, RMCS_REG_CONTROL, RMCS_CMD_BRAKE);      }
void rmcs_set_freq   (Joint &j, uint16_t f) {
  f = (uint16_t)clampf(f, RMCS_FREQ_MIN, RMCS_FREQ_MAX);
  rmcs_write_reg(j.uart_ptr, j.rs485_de, j.rmcs_slave_id, RMCS_REG_FREQUENCY, f);
}

// =============================================================================
// RMCS UPDATE — direction + frequency caching
// =============================================================================
// Direction write: only when sign changes (saves ~2.86 ms per joint per tick).
// Frequency write: only when value changes (zero at convergence → UART silent).

static bool dir_last[6] = { true, true, true, true, true, true };

void rmcs_update_joint(Joint &j) {
  if (estop_active) return;

  uint16_t freq = j.freq_pending;

  if (freq == 0) {
    rmcs_brake(j);
    j.freq_sent       = 0;
    j.dir_initialized = false;
    return;
  }

  bool want_cw = j.dir_positive;
  if (!j.dir_initialized || want_cw != dir_last[j.index]) {
    if (want_cw) rmcs_enable_cw(j);
    else         rmcs_enable_ccw(j);
    dir_last[j.index] = want_cw;
    j.dir_initialized = true;
  }

  if (freq != j.freq_sent) {
    rmcs_set_freq(j, freq);
    j.freq_sent = freq;
  }
}

// =============================================================================
// EMERGENCY STOP
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
// INTERVAL TIMER ISR
// =============================================================================

void control_timer_isr() {
  control_flag = true;
  pid_tick++;
}

// =============================================================================
// CONTROL LOOP — 200 Hz PID + 100 Hz RMCS update
// =============================================================================
// Timing per 5 ms PID tick:
//   6 × AS5600 I2C reads @ 400 kHz:  ~6 × 0.65 ms = 3.90 ms
//   6 × pid_update + freq compute:   ~0.03 ms
//   spi_build_telem:                 ~0.005 ms
//   Total PID work:                  ≈ 3.94 ms  (1.06 ms headroom ✓)
//
// RMCS update (every 2nd tick = 100 Hz, 10 ms budget):
//   Each joint has its own UART — all 6 frames fire in parallel.
//   Worst case per UART: 1 joint × 2 writes × 2.86 ms = 5.72 ms < 10 ms ✓

void run_control_loop() {

  // 1. Read encoders + run PID for all 6 joints
  for (uint8_t i = 0; i < 6; i++) {
    Joint &j = joints[i];
    if (!j.enabled) continue;

    abs_encoder_update(j);

    float vel = pid_update(j.pid, j.setpoint_rad, j.enc.angle_filtered);
    vel = clampf(vel, -VEL_MAX_RAD_S, VEL_MAX_RAD_S);

    j.dir_positive = (vel >= 0.0f);
    j.freq_pending = velocity_to_frequency(vel);
  }

  // 2. RMCS update at 100 Hz — sequential dispatch is fine since each
  //    joint owns its UART; there is no bus contention between joints.
  if ((pid_tick % RMCS_DIV) == 0) {
    for (uint8_t i = 0; i < 6; i++) {
      rmcs_update_joint(joints[i]);
    }
  }

  // 3. Build fresh telemetry for next SPI transaction
  spi_build_telem();
}

// =============================================================================
// SETUP
// =============================================================================

// Map joint index to its dedicated UART
HardwareSerial* joint_uart(uint8_t idx) {
  switch (idx) {
    case 0: return &Serial1;
    case 1: return &Serial2;
    case 2: return &Serial3;
    case 3: return &Serial4;
    case 4: return &Serial5;
    default: return &Serial6;
  }
}

// Map joint index to its RS-485 DE pin
int8_t joint_de(uint8_t idx) {
  const int8_t de_list[6] = {
    RS485_DE_J0, RS485_DE_J1, RS485_DE_J2,
    RS485_DE_J3, RS485_DE_J4, RS485_DE_J5
  };
  return de_list[idx];
}

void setup() {
  Serial.begin(115200);
  Serial.println(F("[ACARE] 6-DOF Teensy 4.1 — SPI slave + 6x dedicated UART RMCS"));

  // I2C
  Wire.begin();
  Wire.setClock(400000);
  Wire.setDefaultTimeout(2000);

  for (uint8_t ch = 0; ch < 6; ch++) {
    mux_select(ch);
    Wire.beginTransmission(AS5600_ADDR);
    Serial.print(F("[AS5600] ch")); Serial.print(ch);
    Serial.println(Wire.endTransmission() == 0 ? F(" OK") : F(" NOT FOUND"));
  }
  mux_disable_all();

  // RMCS UARTs — one per joint
  Serial1.begin(RMCS_BAUD);
  Serial2.begin(RMCS_BAUD);
  Serial3.begin(RMCS_BAUD);
  Serial4.begin(RMCS_BAUD);
  Serial5.begin(RMCS_BAUD);
  Serial6.begin(RMCS_BAUD);
  Serial.print(F("[RMCS] Serial1–6 at ")); Serial.print(RMCS_BAUD); Serial.println(F(" baud"));

  // RS-485 DE pin setup
  const int8_t de_list[6] = {
    RS485_DE_J0, RS485_DE_J1, RS485_DE_J2,
    RS485_DE_J3, RS485_DE_J4, RS485_DE_J5
  };
  for (uint8_t i = 0; i < 6; i++) {
    if (de_list[i] >= 0) { pinMode(de_list[i], OUTPUT); digitalWrite(de_list[i], LOW); }
  }

  // Joint initialisation
  for (uint8_t i = 0; i < 6; i++) {
    Joint &j          = joints[i];
    j.index           = i;
    j.rmcs_slave_id   = i + 1;
    j.mux_channel     = i;
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

    rmcs_disable(j); delay(20);
    rmcs_set_freq(j, 0); delay(20);
    rmcs_enable_cw(j);
    dir_last[i]       = true;
    j.dir_initialized = true;
    j.enabled         = true;

    Serial.print(F("[Joint ")); Serial.print(i); Serial.println(F("] ready"));
  }

  // SPI slave
  spi_slave_init();
  spi_last_ms = millis();
  Serial.println(F("[SPI] Slave ready (pins 10-13, MODE0, MSB first)"));

  // 200 Hz IntervalTimer
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

  // 1. 200 Hz control loop (triggered by IntervalTimer ISR)
  if (control_flag) {
    control_flag = false;
    if (!estop_active) run_control_loop();
  }

  // 2. SPI slave: service active transaction
  if (spi_in_transaction) {
    spi_do_transfer();
  }

  if (spi_ready) {
    spi_ready = false;
    spi_process_cmd();
  }

  // 3. Watchdog — brake all joints if Pi5 goes silent
  if (!estop_active && (millis() - spi_last_ms) > SPI_WATCHDOG_MS) {
    estop_active = true;
    emergency_stop_all();
    Serial.println(F("[WATCHDOG] Pi5 silent — joints braked"));
  }

  // 4. Diagnostics — one joint per 100 ms, round-robin
  static uint32_t diag_ms = 0;
  static uint8_t  diag_j  = 0;
  if (millis() - diag_ms >= 100) {
    diag_ms = millis();
    Joint &j = joints[diag_j];
    Serial.print(F("J")); Serial.print(diag_j);
    Serial.print(F(" pos=")); Serial.print(j.enc.angle_filtered, 3);
    Serial.print(F(" sp="));  Serial.print(j.setpoint_rad, 3);
    Serial.print(F(" fq="));  Serial.print(j.freq_sent);
    Serial.print(F(" fault=")); Serial.println(j.fault);
    diag_j = (diag_j + 1) % 6;
  }
}

// =============================================================================
// PUBLIC: Set position target for one joint (local override / testing)
// =============================================================================

void set_joint_target(uint8_t idx, float rad) {
  if (idx >= 6) return;
  joints[idx].setpoint_rad = rad;
  pid_reset(joints[idx].pid);
}