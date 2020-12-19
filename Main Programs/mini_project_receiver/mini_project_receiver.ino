#include "BluetoothSerial.h" 
#include "String.h"
BluetoothSerial ESP_BT;

void setup() 
{
  Serial.begin(115200);
  ESP_BT.begin("ESP32 BT");
//  Serial.println("Bluetooth device is ready to pair!");
  pinMode(2, OUTPUT);
  digitalWrite(2, LOW);
}

void loop() 
{
  ESP_BT.println("NEXT");
  if(ESP_BT.available())
  {
    String val = ESP_BT.readStringUntil('\n');
    Serial.println(val);
    
  }
  delay(1000);  
}
