// Pin connected to the LED
const int ledPin = 13;

// timing constants
const int dotDelay = 200;  // dot ms
const int dashDelay = 3 * dotDelay;  // dash ms aka 3x dot duration
const int interLetterDelay = dotDelay;  // space between letters (1 dot duration)
const int loopDelay = 7 * dotDelay;  // space between restart (7 times the dot duration)

// lookup table
const char morseCode[][6] = {
  {'.', '-', '-', '.', '.'},  // m
  {'-', '.', '.', '.', '-'},  // a
  {'-', '.', '-'},            // t
  {'.', '.', '.', '.', '.'},  // t
  {'-', '.', '.', '.'},       // h
  {'.', '.', '-', '.'},       // e
  {'.', '-', '-', '-', '.'}   // w
};

// DOT
void dot() {
  digitalWrite(ledPin, HIGH);
  delay(dotDelay);
  digitalWrite(ledPin, LOW);
  delay(dotDelay);
}

// DASH
void dash() {
  digitalWrite(ledPin, HIGH);
  delay(dashDelay);
  digitalWrite(ledPin, LOW);
  delay(dotDelay);
}

// blink a character in Morse code
void blinkCharacter(const char* character) {
  for (int i = 0; character[i] != '\0'; i++) {
    if (character[i] == '.')
      dot();
    else if (character[i] == '-')
      dash();
  }
}

void setup() {
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // initialize loop
  for (int i = 0; i < 7; i++) {
    blinkCharacter(morseCode[i]);
    delay(interLetterDelay);
  }

  delay(loopDelay);
}

