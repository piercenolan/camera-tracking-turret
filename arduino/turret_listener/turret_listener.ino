// Reads "pan,tilt\n" over serial, clamps both to 0-180, drives two servos.
// pan -> pin 9, tilt -> pin 10. Must match src/config.py's SERIAL_PORT/BAUD_RATE
// and PAN_MIN_DEG/PAN_MAX_DEG/TILT_MIN_DEG/TILT_MAX_DEG if those ever change.

#include <Servo.h>

const int PAN_PIN = 9;
const int TILT_PIN = 10;

const int PAN_MIN_DEG = 15;
const int PAN_MAX_DEG = 180;
const int TILT_MIN_DEG = 125;
const int TILT_MAX_DEG =360;

const long BAUD_RATE = 9600;


Servo panServo;
Servo tiltServo;

void setup() {
  Serial.begin(BAUD_RATE);
  panServo.attach(PAN_PIN);
  tiltServo.attach(TILT_PIN);

  // Known position on power-up, rather than wherever the servo happened to sit.
  panServo.write(15);
  tiltServo.write(220);
}

void loop() {
  
  // if (Serial.available() > 0) {
  //   String line = Serial.readStringUntil('\n');
  //   line.trim();

  //   int commaIndex = line.indexOf(',');
  //   bool hasBothHalves = commaIndex > 0 && commaIndex < (int)line.length() - 1;
  //   if (!hasBothHalves) {
  //     return; // malformed line ("pan,tilt" expected) -- ignore, don't move
  //   }

  //   int pan = line.substring(0, commaIndex).toInt();
  //   int tilt = line.substring(commaIndex + 1).toInt();

  //   pan = constrain(pan, PAN_MIN_DEG, PAN_MAX_DEG);
  //   tilt = constrain(tilt, TILT_MIN_DEG, TILT_MAX_DEG);

  //   panServo.write(pan);
  //   tiltServo.write(tilt);

  //   Serial.print("OK ");
  //   Serial.print(pan);
  //   Serial.print(",");
  //   Serial.println(tilt);
    
    static int pan = 0;
    static int negFlag = 1;
    pan += negFlag;
    panServo.write(pan);
    if (pan >= PAN_MAX_DEG || pan <= 0) {
      negFlag *= -1;
    }
    delay(15);    
  }

