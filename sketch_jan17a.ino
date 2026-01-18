#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu.initialize();
}

void loop() {
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  float x = ax / 17000.0;
  float y = ay / 17000.0;

  Serial.print(x);
  Serial.print(",");
  Serial.println(y);

  delay(20);
}
