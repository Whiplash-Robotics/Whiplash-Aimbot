/* ────────────────────────────────────────────────────────────────
   Single quadrature encoder  →  Arduino Mega 2560
   Instantaneous signed RPM   (A=2, B=3, Z=18), 100 PPR
   ──────────────────────────────────────────────────────────────── */

const uint8_t PIN_A = 2;          // INT0  – rising edges here
const uint8_t PIN_B = 3;          // digital read for direction
const uint8_t PIN_Z = 18;         // INT5  – index pulse (1 per rev)

const uint16_t PPR = 100;         // pulses per revolution

/* ── shared between ISR and loop ─────────────────────────────── */
volatile uint32_t lastA_us     = 0;   // μs timestamp of previous A edge
volatile uint32_t periodA_us   = 0;   // time between last two A pulses
volatile int8_t   dirSign      = 0;   // +1 fwd, −1 rev
volatile bool     newPeriodA   = false;

volatile uint32_t lastZ_us     = 0;   // timestamp of last index pulse (optional)
volatile bool     newZ         = false;

/* ── A-channel ISR (direction + timing) ──────────────────────── */
void ISR_A()
{
  uint32_t now = micros();
  uint32_t last = lastA_us;

  // Read B immediately → determines which channel leads
  bool bLevel = digitalRead(PIN_B);

  dirSign = bLevel ? -1 : +1;          // LOW => A leads B => forward

  if (last != 0) {                     // skip very first edge
    periodA_us = now - last;
    newPeriodA = true;
  }
  lastA_us = now;
}

/* ── Z (index) ISR – time-stamps revolution marker ───────────── */
void ISR_Z()
{
  lastZ_us = micros();
  newZ = true;
}

/* ── SETUP ───────────────────────────────────────────────────── */
void setup()
{
  Serial.begin(115200);

  pinMode(PIN_A, INPUT_PULLUP);
  pinMode(PIN_B, INPUT_PULLUP);
  pinMode(PIN_Z, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(PIN_A), ISR_A, RISING); // fast ISR
  attachInterrupt(digitalPinToInterrupt(PIN_Z), ISR_Z, RISING); // optional

  Serial.println(F("Instantaneous RPM with direction (100 PPR) ready"));
}

/* ── MAIN LOOP ───────────────────────────────────────────────── */
void loop()
{
  /* ---- Handle A-edge timing → RPM ---- */
  if (newPeriodA) {
    uint32_t delta_t;
    int8_t   s;

    noInterrupts();
    delta_t         = periodA_us;
    s          = dirSign;
    newPeriodA = false;
    interrupts();

    // RPM = 60 000 000 µs / (delta_t * PPR)  ; sign gives direction
    float rpm = s * (60.0f * 1e6) / (delta_t * PPR);

    Serial.print(F("RPM = "));
    Serial.println(rpm, 2);
  }

  /* ---- Optional: react to index pulse ---- */
  if (newZ) {
    uint32_t t;
    noInterrupts();
    t     = lastZ_us;
    newZ  = false;
    interrupts();

    // Serial.print(F("Index pulse at "));
    // Serial.print(t);
    // Serial.println(F(" µs"));
  }
}
