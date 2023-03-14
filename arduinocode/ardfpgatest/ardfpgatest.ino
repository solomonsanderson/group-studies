void setup() {
  // put your setup code here, to run once:
  enableFpgaClock();
  pinMode(1, OUTPUT)
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(0, LOW);
  delayMicrosecond(1);
  digitalWrite(1, HIGH);
  delayMicrosecond(1);
}
