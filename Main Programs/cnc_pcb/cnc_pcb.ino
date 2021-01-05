const int dir_x = 5;
const int dir_y = 2;
const int step_x = 18;
const int step_y = 4;
const int in3 =21;
const int in4 =19;
int data_x,data_y;
String Data_x,Data_y;
#include "BluetoothSerial.h" 
BluetoothSerial ESP_BT;
int speedm=1000;
int delayt=240;
int time_to_solder=2000;

void moveTo_x(int steps)
{
  if (steps<0)
  {steps=-steps;
  digitalWrite(dir_x,HIGH);}
  else
  digitalWrite(dir_x,LOW);
 
  
  
  for(int x = 0; x < steps; x++)
  {
    digitalWrite(step_x, HIGH);
    delayMicroseconds(speedm);
    digitalWrite(step_x, LOW);
    delayMicroseconds(speedm);
  }
}
void moveTo_y(int steps)
{
  if (steps<0)
  {steps=-steps;
  digitalWrite(dir_y,HIGH);}
  else
  digitalWrite(dir_y,LOW);
 
  
  
  for(int x = 0; x < steps; x++)
  {
    digitalWrite(step_y, HIGH);
    delayMicroseconds(speedm);
    digitalWrite(step_y,LOW);
    delayMicroseconds(speedm);
  }
}
void setup()
{
  // Declare pins as Outputs
  pinMode(step_x, OUTPUT);
  pinMode(dir_x, OUTPUT);
  pinMode(step_y, OUTPUT);
  pinMode(dir_y, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  delay(1000);

  
  moveTo_x(-300);
  moveTo_y(-300);
  Serial.begin(115200);
  ESP_BT.begin("CNC_PCB");

}
void loop()
{int index;
 ESP_BT.println("NEXT");
  if(ESP_BT.available())
  {
    String val = ESP_BT.readStringUntil('\n');
    Serial.println(val);
    index=0;
    while(val[index]!=',')
    { 
    Data_x+=val[index];
    index+=1;
    }
    index+=1;
    while(index<val.length())
    {Data_y+=val[index];
    index+=1;}
    data_x=Data_x.toInt();
    data_y=Data_y.toInt();
    Serial.print("Steps_x:");
    Serial.print(data_x);
    Serial.print("  Steps_y:");
    Serial.println(data_y);
    Data_x="";
    Data_y="";
    moveTo_x(data_x);
    moveTo_y(data_y);
    delay(500);


    //Z-axis move up and down

  digitalWrite(in3,HIGH);
  digitalWrite(in4,LOW);
  delay(delayt);
  digitalWrite(in3,LOW);
  digitalWrite(in4,LOW);
  delay(time_to_solder);
  digitalWrite(in3,LOW);
  digitalWrite(in4,HIGH);
   delay(500);
   digitalWrite(in3,LOW);
  digitalWrite(in4,LOW);
  }  
}

  
