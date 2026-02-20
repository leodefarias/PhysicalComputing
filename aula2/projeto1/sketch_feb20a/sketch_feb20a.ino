#define led 8

void setup() {
  Serial.begin(9600);
  pinMode(led, OUTPUT);

}

void loop() {
  if(Serial.available() > 0){
    char comando = Serial.read();

    if(comando == '1'){
      digitalWrite(led, HIGH);
    } else if(comando == '2'){
      digitalWrite(led, LOW);
    }
  }
}
 