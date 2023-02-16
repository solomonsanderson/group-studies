void setup() {
  pinMode(5, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}
void loop() {
  digitalWrite(5, HIGH);  
  digitalWrite(LED_BUILTIN, HIGH);
  delayMicroseconds(1); 
  // delay(1);
               
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(5, LOW);  
  delayMicroseconds(1);             
  // delay(1);
}
