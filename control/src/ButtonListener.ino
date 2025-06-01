// Arduino Mega: Button Debounce Example for Pins 4 and 7
// Listens for buttons wired to ground (using INPUT_PULLUP) with debounce.
// Prints a message to Serial whenever a button is pressed.

const uint8_t BUTTON_PIN1 = 4;
const uint8_t BUTTON_PIN2 = 7;

const unsigned long DEBOUNCE_DELAY = 50;  // 50 ms debounce interval

// Variables for Button on pin 4
int lastReading1 = HIGH;              // Last raw reading from pin 4
int buttonState1  = HIGH;             // Debounced state
unsigned long lastDebounceTime1 = 0;  // Timestamp of last change

// Variables for Button on pin 7
int lastReading2 = HIGH;              // Last raw reading from pin 7
int buttonState2  = HIGH;             // Debounced state
unsigned long lastDebounceTime2 = 0;  // Timestamp of last change

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN1, INPUT_PULLUP);
  pinMode(BUTTON_PIN2, INPUT_PULLUP);
}

void loop() {
  unsigned long currentTime = millis();

  // ----- Handle Button on Pin 4 -----
  int reading1 = digitalRead(BUTTON_PIN1);

  if (reading1 != lastReading1) {
    lastDebounceTime1 = currentTime;
  }
  if ((currentTime - lastDebounceTime1) > DEBOUNCE_DELAY) {
    if (reading1 != buttonState1) {
      buttonState1 = reading1;
      if (buttonState1 == LOW) {
        Serial.println("Button on pin 4 pressed!");
      }
    }
  }
  lastReading1 = reading1;

  // ----- Handle Button on Pin 7 -----
  int reading2 = digitalRead(BUTTON_PIN2);

  if (reading2 != lastReading2) {
    lastDebounceTime2 = currentTime;
  }
  if ((currentTime - lastDebounceTime2) > DEBOUNCE_DELAY) {
    if (reading2 != buttonState2) {
      buttonState2 = reading2;
      if (buttonState2 == LOW) {
        Serial.println("Button on pin 7 pressed!");
      }
    }
  }
  lastReading2 = reading2;

  // Tiny delay to reduce loop churn (optional)
  delay(5);
}
