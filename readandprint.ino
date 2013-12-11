// LE - Left Electrode, RE - Right Electrode.

const int analogInPin_LE = A0;
const int analogInPin_RE = A1;

int sensorValue_LE = 0;
int sensorValue_RE = 0;

void setup() {
  // Initialize serial communication at 9600 bps.
  Serial.begin(9600);
}

void loop() {
  // Read the analog input value.
  sensorValue_LE = analogRead(analogInPin_LE);
  sensorValue_RE = analogRead(analogInPin_RE);

  // Print the results to the serial monitor,
  // delimiting the two values with a comma.
  Serial.print(sensorValue_LE);
  Serial.print(",");
  Serial.println(sensorValue_RE);

  // Wait for 2 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading.
  delay(2);
}
