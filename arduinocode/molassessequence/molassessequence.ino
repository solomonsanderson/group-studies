
int time_counter = 0; 
int ci_pin = DAC0; // analogue
int cf_pin = A1; // cooling frequency pin , analogue
int repump_pin = A2; // analogue
int mc_pin = 7; //mot coils pin, digital 
int output_max = 255; 
int output_max_12 = 4095;

int dt = 10; // time interval per cycle
int f_ramp = 0; // fast ramp counter
int f_ramp_time = 1500; // total fast ramp time 
int f_delta = (dt/f_ramp_time) * 2000;   

int s_ramp = 2000; // slow ramp counter
int s_ramp_time = 11500;
int s_delta = (dt/s_ramp_time) * 3880;

void setup() {
  // put your setup code here, to run once:

  //we use pin 1 and 2 for triggering MZ so cannot use them 
  // we already use pin 6 for controlling the rf for the laser.



  pinMode(ci_pin, OUTPUT);
  pinMode(cf_pin, OUTPUT);
  pinMode(repump_pin, OUTPUT);
  pinMode(mc_pin, OUTPUT);


  
}

void loop() {
  // put your main code here, to run repeatedly:
  // set all pins to start values
  analogWriteResolution(12);
  if (time_counter < 1750){ // delay for 1.75micros
    analogWrite(ci_pin, output_max_12);
    analogWrite(cf_pin, 0.17 * output_max_12); // starts at around 17%
    analogWrite(repump_pin, output_max_12);
    digitalWrite(mc_pin, HIGH);
  }
  
  else if ((1750 <= time_counter) && (time_counter < 5000)){ // delay for 3250 micros (5ms total)
    analogWrite(ci_pin, 0);
    analogWrite(repump_pin, 0);
    digitalWrite(mc_pin, LOW);
  }

  else if (5000 <= time_counter < 6500){ //delay for 1500 micros (6.5ms total)
    analogWrite(repump_pin, 0.45 * output_max_12);
    analogWrite(ci_pin, 0.45 * output_max_12);

    // ramp cf

    f_ramp += f_delta;
    analogWrite(cf_pin, f_ramp);
  }
  // need to add ramp for cooling frequency

  else if (6500 <= time_counter < 18000){ //delat for 7500 micros (14ms total)
    analogWrite(ci_pin, 0.3 * output_max);
    if (time_counter >= 14000){
      analogWrite(repump_pin, 0);
    }
    else {
      analogWrite(repump_pin, 0.3 * output_max);
    }

    s_ramp += s_delta;
    analogWrite(cf_pin, s_ramp);
  }

  else if (18000 < time_counter < 18250){
    analogWrite(ci_pin, 0);
    analogWrite(cf_pin, 4095);

  }


  time_counter += dt; 
  delayMicroseconds(dt);
}
