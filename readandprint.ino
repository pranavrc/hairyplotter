const int analogInPin1 = A0;
const int analogInPin2 = A1;
int sensorValue1 = 0;
int sensorValue2 = 0;
void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600); 
}

void loop() {
  // read the analog in value:
  sensorValue1 = analogRead(analogInPin1);
  sensorValue2 = analogRead(analogInPin2);
  
  // print the results to the serial monitor:
  Serial.print(sensorValue1);
  Serial.print(",");
  Serial.println(sensorValue2);
  
  // wait 2 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(2);                     
}
