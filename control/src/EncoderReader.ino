// on Mega, interrupt‐capable pins: 2,3,18,19,20,21
#define SENSOR_PIN 3

volatile unsigned long lastTime  = 0;
volatile unsigned long periodUs  = 0;
volatile bool          newData = false;

void onEdge() {
  unsigned long now = micros();
  periodUs = now - lastTime;
  lastTime = now;
  newData = true;
}

void setup() {
  Serial.begin(115200);
  pinMode(SENSOR_PIN, INPUT);
  lastTime = micros();
  attachInterrupt(digitalPinToInterrupt(SENSOR_PIN), onEdge, RISING);
}

void loop() {
  if (newData) {
    noInterrupts();
    unsigned long p = periodUs;
    newData = false;
    interrupts();

    Serial.println(p/1000.0f, 5);
  }
}
