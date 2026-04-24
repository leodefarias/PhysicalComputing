#include<SPI.h>
#include<MFRC522.h>
#include<ArduinoJson.h>

#define PINO_SDA 10
#define PINO_RST 9

MFRC522 leitor(PINO_SDA, PINO_RST);



void setup() {
  Serial.begin(9600);
  SPI.begin();
  leitor.PCD_Init();
  Serial.println("Aproxime o cartão...");
}

void loop() {
  if(!leitor.PICC_IsNewCardPresent()) return;
  if(!leitor.PICC_ReadCardSerial()) return;

  String uid = "";

  for(byte i = 0; i < leitor.uid.size; i++){
    uid += String(leitor.uid.uidByte[i], HEX);
    if(i < leitor.uid.size - i) uid += " ";
  }

  uid.toUpperCase();

  //Criando JSON
  StaticJsonDocument<100>doc;
  
  //Atributo = valor
  doc["uid"] = uid;
  doc["status"] = "Lido";

  serializeJson(doc, Serial);
  Serial.println();
  delay(1000);



}
