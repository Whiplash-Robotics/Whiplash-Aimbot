#define INPUT_PIN 7

void setup() {

  Serial.begin(9600);
  pinMode(INPUT_PIN, INPUT);
 
}

long lastTime = 0;
int state = 0;

void loop() {

  int currentState = digitalRead(INPUT_PIN);
  if (state == currentState) return;

  long currentTime = micros();

  Serial.println((currentTime - lastTime) / 1000.0f);

  lastTime = currentTime;
  state = currentState;
}
