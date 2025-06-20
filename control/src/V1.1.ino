// Arduino Mega: Data Logging for ON/OFF durations controlled by Buttons
// - Button on pin 4 starts sending Hall effect sensor ON/OFF duration data via Serial.
// - Button on pin 7 stops sending Hall effect sensor ON/OFF duration data.
// - Hall effect sensor on interrupt-capable pin 3.
// - Measures and reports the duration of both ON and OFF states of the sensor.

// ----- Button Configuration -----
const uint8_t START_BUTTON_PIN = 4; // Button to start logging
const uint8_t STOP_BUTTON_PIN = 7;  // Button to stop logging
const unsigned long DEBOUNCE_DELAY = 50; // 50 ms debounce interval

// Variables for Start Button (pin 4)
int lastReadingStart = HIGH;
int buttonStateStart = HIGH;
unsigned long lastDebounceTimeStart = 0;

// Variables for Stop Button (pin 7)
int lastReadingStop = HIGH;
int buttonStateStop = HIGH;
unsigned long lastDebounceTimeStop = 0;

// ----- Hall Effect Sensor Configuration -----
// On Mega, interrupt-capable pins include: 2, 3, 18, 19, 20, 21
#define SENSOR_PIN 3 // Using pin 3 for the Hall effect sensor

// Volatile variables modified by ISR
volatile unsigned long newEdgeTimestamp_us = 0;
volatile bool newEdgeOccurred = false;
volatile int sensorPinStateAtNewEdge = LOW;

// Non-volatile variables for state and duration tracking in loop()
unsigned long previousEdgeTimestamp_us = 0;
int previousSensorPinState = LOW; // Assumed initial state, will be updated in setup

unsigned long onDuration_us = 0;
unsigned long offDuration_us = 0;
bool newOnDurationAvailable = false;
bool newOffDurationAvailable = false;

// ----- Logging State -----
bool isLogging = false; // Flag to control data transmission

// ----- Interrupt Service Routine for Hall Sensor -----
// This ISR is called on ANY change (RISING or FALLING) of the SENSOR_PIN
void onHallSensorChange() {
  newEdgeTimestamp_us = micros(); // Record the time of the edge
  sensorPinStateAtNewEdge = digitalRead(SENSOR_PIN); // Record the new state of the pin
  newEdgeOccurred = true;       // Set a flag for the main loop to process
}

// ----- Setup Function -----
void setup() {
  Serial.begin(115200); // Use a higher baud rate for faster data transfer

  // Initialize Button Pins
  pinMode(START_BUTTON_PIN, INPUT_PULLUP);
  pinMode(STOP_BUTTON_PIN, INPUT_PULLUP);

  // Initialize Hall Sensor Pin
  pinMode(SENSOR_PIN, INPUT_PULLUP); // Set sensor pin as input.
                              // Use INPUT_PULLUP if your sensor has an open-collector/drain output
                              // and no external pull-up resistor.

  Serial.println("System Initializing...");
  delay(100); // Short delay for sensor stabilization and accurate initial reading

  // Initialize sensor state and timestamp before attaching interrupt
  previousSensorPinState = digitalRead(SENSOR_PIN);
  previousEdgeTimestamp_us = micros();

  // Attach interrupt to SENSOR_PIN, trigger on CHANGE (both RISING and FALLING edges)
  attachInterrupt(digitalPinToInterrupt(SENSOR_PIN), onHallSensorChange, CHANGE);

  Serial.print("Initial sensor state: ");
  Serial.println(previousSensorPinState == HIGH ? "ON" : "OFF");
  Serial.println("Press button on Pin 4 to START logging, Pin 7 to STOP.");
}

// ----- Main Loop -----
void loop() {
  unsigned long currentTime_ms = millis(); // For button debouncing

  // ----- Handle Start Button (Pin 4) -----
  int readingStart = digitalRead(START_BUTTON_PIN);
  if (readingStart != lastReadingStart) {
    lastDebounceTimeStart = currentTime_ms;
  }
  if ((currentTime_ms - lastDebounceTimeStart) > DEBOUNCE_DELAY) {
    if (readingStart != buttonStateStart) {
      buttonStateStart = readingStart;
      if (buttonStateStart == LOW) { // Button is pressed
        if (!isLogging) {
          isLogging = true;
          Serial.println("LOGGING_START");
          // Re-initialize sensor state tracking upon starting logging
          // to ensure the first reported duration is correct after a pause.
          noInterrupts(); // Temporarily disable interrupts
          previousSensorPinState = digitalRead(SENSOR_PIN);
          previousEdgeTimestamp_us = newEdgeTimestamp_us; // Use the latest edge time if available, or current time
          if (!newEdgeOccurred) previousEdgeTimestamp_us = micros(); // If no edge happened recently, use current time
          newEdgeOccurred = false; // Reset flag as we are consuming/resetting state
          interrupts(); // Re-enable interrupts
          newOnDurationAvailable = false; // Clear old data flags
          newOffDurationAvailable = false;
        }
      }
    }
  }
  lastReadingStart = readingStart;

  // ----- Handle Stop Button (Pin 7) -----
  int readingStop = digitalRead(STOP_BUTTON_PIN);
  if (readingStop != lastReadingStop) {
    lastDebounceTimeStop = currentTime_ms;
  }
  if ((currentTime_ms - lastDebounceTimeStop) > DEBOUNCE_DELAY) {
    if (readingStop != buttonStateStop) {
      buttonStateStop = readingStop;
      if (buttonStateStop == LOW) { // Button is pressed
        if (isLogging) {
          isLogging = false;
          Serial.println("LOGGING_STOP");
        }
      }
    }
  }
  lastReadingStop = readingStop;

  // ----- Process Hall Effect Sensor Edge Data -----
  if (newEdgeOccurred) {
    unsigned long currentEdgeTime_us_local;
    int currentSensorState_local;

    // Safely copy volatile data modified by ISR
    noInterrupts();
    currentEdgeTime_us_local = newEdgeTimestamp_us;
    currentSensorState_local = sensorPinStateAtNewEdge;
    newEdgeOccurred = false; // Reset the flag, we are processing this edge
    interrupts();

    // Calculate duration of the previous state
    unsigned long duration_us = currentEdgeTime_us_local - previousEdgeTimestamp_us;

    if (previousSensorPinState == HIGH && currentSensorState_local == LOW) {
      // Sensor was ON, now it's OFF. 'duration_us' is the ON_DURATION.
      onDuration_us = duration_us;
      newOnDurationAvailable = true;
    } else if (previousSensorPinState == LOW && currentSensorState_local == HIGH) {
      // Sensor was OFF, now it's ON. 'duration_us' is the OFF_DURATION.
      offDuration_us = duration_us;
      newOffDurationAvailable = true;
    }
    // Else: a glitch or multiple interrupts for the same logical state change (unlikely with clean signal)

    // Update state for the next calculation
    previousEdgeTimestamp_us = currentEdgeTime_us_local;
    previousSensorPinState = currentSensorState_local;
  }

  // ----- Log Data if Enabled -----
  if (isLogging) {
    if (newOnDurationAvailable) {
      Serial.print("ON_ms:");
      Serial.println(onDuration_us / 1000.0f, 3); // Duration in milliseconds with 3 decimal places
      newOnDurationAvailable = false; // Reset flag after logging
    }
    if (newOffDurationAvailable) {
      Serial.print("OFF_ms:");
      Serial.println(offDuration_us / 1000.0f, 3); // Duration in milliseconds with 3 decimal places
      newOffDurationAvailable = false; // Reset flag after logging
    }
  }
  // delay(1); // Optional very short delay if loop is too fast causing issues, but generally not needed.
}