#include <Arduino.h>

#define SLAVE_ID1 0x01
#define SLAVE_ID2 0x02

#define motorSerial1 Serial1
#define motorSerial2 Serial2

// ---------- timing control ----------
#define MODE_SETTLE_US  30000UL   // 30 ms (controller requirement)
static uint32_t lastModeWriteUs = 0;

// --------------------------------------------------
// Modbus ASCII: Write Single Register
// --------------------------------------------------
void sendWriteSingleRegister(uint8_t slaveAddress,
                             uint16_t registerAddress,
                             uint16_t value)
{
  char frame[32];
  char data[20];

  sprintf(data, "%02X06%04X%04X", slaveAddress, registerAddress, value);

  uint8_t lrc = 0;
  for (size_t i = 0; i < strlen(data); i += 2) {
    char byteChars[3] = { data[i], data[i + 1], 0 };
    lrc += strtoul(byteChars, NULL, 16);
  }
  lrc = (uint8_t)(-((int8_t)lrc));

  sprintf(frame, ":%s%02X\r\n", data, lrc);
  motorSerial1.print(frame);
  motorSerial2.print(frame);
}

// --------------------------------------------------
// MOTOR COMMANDS
// --------------------------------------------------
void motorSetMode(uint8_t id, uint16_t mode)
{
  sendWriteSingleRegister(id, 2, mode);
  lastModeWriteUs = micros();
}

void motorSetPWM(uint8_t id, uint16_t pwm)
{
  while ((micros() - lastModeWriteUs) < MODE_SETTLE_US) {}

  pwm = constrain(pwm, 0, 4800);
  sendWriteSingleRegister(id, 4, pwm);
}

void motorBrake(uint8_t id)
{
  motorSetPWM(id, 0);
  motorSetMode(id, 0x0203);
}

// --------------------------------------------------
// SETUP
// --------------------------------------------------
void setup()
{
  Serial.begin(115200);
  motorSerial1.begin(38400);
  motorSerial2.begin(38400);
     // allow PSU + drives to stabilize

  Serial.println("System start");
  Serial.println("Applying initial brake (arming drives)");

  // 🔑 CRITICAL: arm controllers immediately
  motorBrake(SLAVE_ID1);
  motorBrake(SLAVE_ID2);

  Serial.println("Ready for commands");
  Serial.println("Commands:");
  Serial.println("  M1 CW <pwm>");
  Serial.println("  M1 CCW <pwm>");
  Serial.println("  M1 B");
  Serial.println("  M2 CW <pwm>");
  Serial.println("  M2 CCW <pwm>");
  Serial.println("  M2 B");
}

// --------------------------------------------------
// LOOP (SERIAL COMMAND PARSER)
// --------------------------------------------------
void loop()
{
  if (!Serial.available())
    return;

  String input = Serial.readStringUntil('\n');
  input.trim();
  if (input.length() == 0)
    return;

  int s1 = input.indexOf(' ');
  int s2 = input.indexOf(' ', s1 + 1);

  String motorStr = (s1 > 0) ? input.substring(0, s1) : input;
  String cmdStr   = (s1 > 0 && s2 > 0) ? input.substring(s1 + 1, s2)
                    : (s1 > 0) ? input.substring(s1 + 1) : "";
  int pwm         = (s2 > 0) ? input.substring(s2 + 1).toInt() : 0;

  uint8_t motorId =
    motorStr.equalsIgnoreCase("M1") ? SLAVE_ID1 :
    motorStr.equalsIgnoreCase("M2") ? SLAVE_ID2 : 0;

  if (!motorId) {
    Serial.println("Invalid motor ID");
    return;
  }

  // -------- BRAKE --------
  if (cmdStr.equalsIgnoreCase("B")) {
    motorBrake(motorId);
    Serial.println("Motor BRaked");
    return;
  }

  // -------- CW --------
  if (cmdStr.equalsIgnoreCase("CW")) {
    motorSetMode(motorId, 0x0201);
    motorSetPWM(motorId, pwm);
    Serial.println("Motor CW running");
    return;
  }

  // -------- CCW --------
  if (cmdStr.equalsIgnoreCase("CCW")) {
    motorSetMode(motorId, 0x0209);
    motorSetPWM(motorId, pwm);
    Serial.println("Motor CCW running");
    return;
  }

  Serial.println("Unknown command");
}
