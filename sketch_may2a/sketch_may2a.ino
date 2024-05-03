#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define MAX_UIDS 10 // Maximum number of RFID UIDs to store
char storedUIDs[MAX_UIDS][9] = { "0106E7F0", "0102E6F1", "3162DEDF", "E3D21811" };
int numStoredUIDs = sizeof(storedUIDs) / sizeof(storedUIDs[0]); // Calculate the number of stored UIDs

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop() {
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String uid = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      uid.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""));
      uid.concat(String(mfrc522.uid.uidByte[i], HEX));
    }
    //Serial.println("UID: " + uid);
    uid.toUpperCase();
    if(checkUID(uid.c_str())){
      Serial.println(uid); // Send UID over serial to computer
      //Serial.println("Welcome to the Class!");
    } else{
      Serial.println("Access Denied, You are not part of this Class!");
    }
    delay(1000);  // Delay for stability
  }
}

bool checkUID(char* uid) {
    for (int i = 0; i < numStoredUIDs; i++) {
        if (strcmp(storedUIDs[i], uid) == 0) {
            return true; // Match found
        }
    }
    return false; // No match found
}
