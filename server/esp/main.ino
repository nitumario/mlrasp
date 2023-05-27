#include "ESP8266WiFi.h"

const char* ssid = "miau miau";
const char* password = "parola12";
WiFiServer wifiServer1(9090);
WiFiServer wifiServer2(9091);

void setup() {
  Serial.begin(115200);

  delay(1000);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting..");
  }

  Serial.print("Connected to WiFi. IP:");
  Serial.println(WiFi.localIP());

  wifiServer1.begin();
  wifiServer2.begin();
}

void loop() {
  WiFiClient client1 = wifiServer1.available();
  WiFiClient client2 = wifiServer2.available();

  if (client1 && client2) {
    String data1 = "";
    String data2 = "";

    while (client1.connected()) {
      while (client1.available() > 0) {
        char c = client1.read();
        data1 += c;
      }
      delay(10);
    }

    while (client2.connected()) {
      while (client2.available() > 0) {
        char c = client2.read();
        data2 += c;
      }
      delay(10);
    }

    if (data1.equals(data2)) {
      Serial.println("Data is the same: OK = 1");
      transmitOK(client1);
      transmitOK(client2);
    } else {
      Serial.println("Data is different");
    }

    client1.stop();
    client2.stop();
    Serial.println("Clients disconnected");
  }
}

void transmitOK(WiFiClient& client) {
  client.println("OK");
}
