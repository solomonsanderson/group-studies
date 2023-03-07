  int ci_pin = 1; // cooling intensity pin 
  int cf_pin = 2; // cooling frequency pin
  int repump_pin = 3;
  int mc_pin = 0; //mot coils pin 
  int output_max = 255; 

void setup() {
  // put your setup code here, to run once:
  // we already use pin 6 for controlling the rf for the laser.


  pinMode(ci_pin, OUTPUT);
  pinMode(cf_pin, OUTPUT);
  pinMode(repump_pin, OUTPUT);
  pinMode(mc_pin, OUTPUT);


  
}

void loop() {
  // put your main code here, to run repeatedly:
  // set all pins to start values
  analogWrite(ci_pin, output_max);
  analogWrite(cf_pin, 0.17 * output_max); // starts at around 17%
  analogWrite(repump_pin, output_max);
  digitalWrite(mc_pin, HIGH);
  
  delayMicroseconds(1750); // delay for 1.75ms

  analogWrite(ci_pin, 0);
  analogWrite(repump_pin, 0);
  digitalWrite(mc_pin, LOW);

  delayMicroseconds(3250);

  analogWrite(repump_pin, 0.45 * output_max);
  analogWrite(ci_pin, 0.45 * output_max);
  // need to add ramp for cooling frequency

  delayMicroseconds(1500);

  analogWrite(repump_pin, 0.3 * output_max);
  analogWrite(ci_pin, 0.3 * output_max);
  //need to add further ramp

  delayMicroseconds(7500);

  analogWrite(repump_pin, 0);

  delayMicroseconds(4000);

  analogWrite(ci_pin, 0);
}
