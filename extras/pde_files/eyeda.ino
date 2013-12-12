const int analogInPin = A5;  // Analog input pin that the potentiometer is attached to
const int analogOutPin = 11; // Analog output pin that the LED is attached to

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600); 
}

void sendPlotData(String seriesName, float data)
{
  Serial.print("{");
  Serial.print(seriesName);
  Serial.print(",T,");
  Serial.print(data);
  Serial.println("}");
}

void loop() {
  // read the analog in value:
  sensorValue = analogRead(analogInPin);            
  // map it to the range of the analog out:
  outputValue = map(sensorValue, 0, 1023, 0, 5);  
  // change the analog out value:
  analogWrite(analogOutPin, sensorValue);           

  // print the results to the serial monitor:
  Serial.println(outputValue);                 
      
  
  // wait 2 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(2);                     
}

float scaleDown(float newVal, float origMin, float origMax, float modMin, float modMax) {
  return newVal * (modMax - modMin) / (origMax - origMin);
}
