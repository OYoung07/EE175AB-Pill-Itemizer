#include <Stepper.h>
// Number of steps per output rotation



// Create Instance of Stepper library
const int steps = 200;

Stepper myStepper(steps, 0, 2, 14, 12);

void setup() {
  // put your setup code here, to run once:
  myStepper.setSpeed(70);
  pinMode(0,OUTPUT);
  pinMode(2,OUTPUT);
  pinMode(14,OUTPUT);
  pinMode(12,OUTPUT);
  
  Serial.begin(9600);
}


void loop() {
  if(Serial.available() > 0){
    String msg = Serial.readString();
    if(msg == "CCW") {
        rotateCCW();
    }
    else if(msg == "CW") {
        rotateCW();
    }
    else if (msg == "CCW2") {
      rotateCCW2();
    }
    else if (msg == "CW2") {
      rotateCW2();
    }

    if(Serial.available() > 0){
      if(msg == "RESET") {
           ESP.reset();
           flush();
      }
    }
  }
}



void rotateCCW() {
      myStepper.step(45);
}
void rotateCW() {
      myStepper.step(-45);
}
void rotateCCW2() {
  myStepper.step(90);
}
void rotateCW2(){
  myStepper.step(-90);
}

void flush()
{
  digitalWrite(0, LOW);
  digitalWrite(2, LOW);
  digitalWrite(14, LOW);
  digitalWrite(12, LOW);
  //delay(5000);
}
