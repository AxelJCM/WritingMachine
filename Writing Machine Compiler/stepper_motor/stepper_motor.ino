  // Stepper Motor X
  #include <Servo.h>
  const int stepPinX = 2; //X.STEP
  const int dirPinX = 5; // X.DIR
  const int stepPinY = 3; //X.STEP
  const int dirPinY = 6; // X.DIR
  const int xDir = 1650;
  const int yDir = 1050;
 
 void setup() {
 // Sets the two pins as Outputs
 pinMode(stepPinX,OUTPUT); 
 pinMode(dirPinX,OUTPUT);
 pinMode(stepPinY,OUTPUT); 
 pinMode(dirPinY,OUTPUT);
 delay(5000);
 Servo servo;
 //servo.attach(11);
 //servo.write(0);
 }
 void loop() {
//X/ Derecha
 digitalWrite(dirPinX,HIGH);
 digitalWrite(dirPinY,HIGH);// Enables the motor to move in a particular direction
 // Makes 200 pulses for making one full cycle rotation
 for(int x = 0; x < xDir; x++) {
 digitalWrite(stepPinX,HIGH);
 digitalWrite(stepPinY,HIGH);
 delayMicroseconds(1000); 
 digitalWrite(stepPinX,LOW);
 digitalWrite(stepPinY,LOW); 
 delayMicroseconds(1000); 
 }
 // Y/ adelante
 delay(1000); // One second delay
 digitalWrite(dirPinY,LOW);// Enables the motor to move in a particular direction
 // Makes 200 pulses for making one full cycle rotation
 for(int x = 0; x < yDir; x++) {
 digitalWrite(stepPinX,HIGH);
 digitalWrite(stepPinY,HIGH);
 delayMicroseconds(1000); 
 digitalWrite(stepPinX,LOW);
 digitalWrite(stepPinY,LOW); 
 delayMicroseconds(1000); 
 }
 // X Izquierdo
 delay(1000); // One second delay
 digitalWrite(dirPinX,LOW);//Changes the rotations direction
 // Makes 400 pulses for making two full cycle rotation
 for(int x = 0; x < xDir; x++) {
 digitalWrite(stepPinX,HIGH);
 digitalWrite(stepPinY,HIGH);
 delayMicroseconds(1000);
 digitalWrite(stepPinX,LOW);
 digitalWrite(stepPinY,LOW);
 delayMicroseconds(1000);
 }
 delay(1000);
// Y Atras
 digitalWrite(dirPinY,HIGH);// Enables the motor to move in a particular direction
 // Makes 200 pulses for making one full cycle rotation
 for(int x = 0; x < yDir; x++) {
 digitalWrite(stepPinX,HIGH);
 digitalWrite(stepPinY,HIGH);
 delayMicroseconds(1000); 
 digitalWrite(stepPinX,LOW);
 digitalWrite(stepPinY,LOW); 
 delayMicroseconds(1000); 
 }
 
 delay(1000); // One second delay
 }
