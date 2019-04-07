/*
  Analog Input

  Demonstrates analog input by reading an analog sensor on analog pin 0 and
  turning on and off a light emitting diode(LED) connected to digital pin 13.
  The amount of time the LED will be on and off depends on the value obtained
  by analogRead().

  The circuit:
  - potentiometer
    center pin of the potentiometer to the analog input 0
    one side pin (either one) to ground
    the other side pin to +5V
  - LED
    anode (long leg) attached to digital output 13
    cathode (short leg) attached to ground

  - Note: because most Arduinos have a built-in LED attached to pin 13 on the
    board, the LED is optional.

  created by David Cuartielles
  modified 30 Aug 2011
  By Tom Igoe

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogInput
*/

int sensorPin = A0;    // select the input pin for the potentiometer
int ledPin = 13;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor
int sensorValue2=0;

void setup() {
  // declare the ledPin as an OUTPUT:
  pinMode(ledPin, OUTPUT);
  pinMode(sensorPin, INPUT);
 pinMode(3, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
   pinMode(5, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  // read the value from the sensor:
  int SenVal1=!digitalRead(3);
  int SenVal2=!digitalRead(4);
  int SenVal3=!digitalRead(5);
  
  // turn the ledPin on
  //Serial.println(map(sensorValue,48,68,0,4));
  if(SenVal1 && SenVal2){
     Serial.println("jump ="+String(1.5));
  }
    else if(SenVal2 && SenVal3){
     Serial.println("jump ="+String(2.5));
  }
     else if(SenVal1){
     Serial.println("jump ="+String(1));
  }
     else if(SenVal2){
     Serial.println("jump ="+String(2));
  }
       else if(SenVal3){
     Serial.println("jump ="+String(3));
  }
       else {
     Serial.println("jump ="+String(0));
  }
  //Serial.println("jump ="+String(sensorValue));
  //Serial.println("attack ="+String(sensorValue2));
  delay(10);
}
