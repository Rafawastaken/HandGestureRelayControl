#include "ESP8266WiFi.h"

const char* ssid = "MEO-8974B0";
const char* password =  "588d1b30e7";

WiFiServer wifiServer(9999);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);

  delay(1000);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting..");
  }

  Serial.print("Connected to WiFi. IP:");
  Serial.println(WiFi.localIP());

  wifiServer.begin();
}

void loop() {
  WiFiClient client = wifiServer.available();

  if (client) {
    while (client.connected()) {
      while (client.available() > 0) {
        char c = client.read();
        processReceivedValue(c);
        Serial.write(c);
      }

      delay(10);
    }

    client.stop();
    Serial.println("Client disconnected");
  }
}

//Descodifica array para string
void processReceivedValue(char command) {
  if (command == '1') {
    digitalWrite(LED_BUILTIN, HIGH);
  }
  else if (command == '0') {
    digitalWrite(LED_BUILTIN, LOW);
  }
  return;
}
