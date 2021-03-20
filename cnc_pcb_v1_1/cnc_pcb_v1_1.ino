
// Libraries
#include "BluetoothSerial.h" 

//Variables
const int dir_x = 5;
const int dir_y = 2;
const int step_x = 18;
const int step_y = 4;
const int in3 =21;
const int in4 =19;
const int motor_R = 22;
const int motor_L = 23;
const int buzz_pin = 15;
int brd_ct =0,B_count=0 ;
int pt_cnt = 0,Pt_count=0;


int data_x,data_y,rad;
String Data_x,Data_y,Rad,b_count,pt_count;


int speedm=1000;
int time_to_solder=2000;

// Object declaration
BluetoothSerial ESP_BT;

void buzz(int t)
{
  for(int i=0;i<t;i++)
  {
    digitalWrite(buzz_pin,HIGH);
    delay(500);
    digitalWrite(buzz_pin,LOW);
    delay(500);
  }
}

void extrude(int t)
{
  digitalWrite(motor_R,HIGH);
  digitalWrite(motor_L,LOW);
  delay(t);
  digitalWrite(motor_L,LOW);
  digitalWrite(motor_R,LOW);
}

// Utility functions
void moveTo_x(int steps)
{
  if (steps<0)
  {
    steps=-steps;
    digitalWrite(dir_x,HIGH);
  }
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
  {
    steps=-steps;
    digitalWrite(dir_y,HIGH);
  }
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

void move_down(int t)
{
  digitalWrite(in3,HIGH);
  digitalWrite(in4,LOW);
  delay(t);
  digitalWrite(in3,LOW);
  digitalWrite(in4,LOW);
}

void move_up(int t)
{
  digitalWrite(in3,LOW);
  digitalWrite(in4,HIGH);
  delay(t);
  digitalWrite(in3,LOW);
  digitalWrite(in4,LOW);
}
// setup function
void setup()
{
  // Declare pins as Outputs
  pinMode(step_x, OUTPUT);
  pinMode(dir_x, OUTPUT);
  pinMode(step_y, OUTPUT);
  pinMode(dir_y, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(motor_R, OUTPUT);
  pinMode(motor_L, OUTPUT);
  pinMode(buzz_pin,OUTPUT);
  delay(1000);
  moveTo_x(-300);
  moveTo_y(-300);
  Serial.begin(115200);
  ESP_BT.begin("CNC_PCB");
  while(1)
  {
    if(ESP_BT.available()>0)
    {
        String val = ESP_BT.readStringUntil('\n');
        if(val=="1")
        {
            buzz(1);
            move_up(50);
        }
        else if(val=="2")
        {
            buzz(1);
            move_down(50);
        }
        else if(val=="3")
        {
            buzz(1);
            extrude(5000);
        }
        else if(val=="5")
        {
            buzz(1);
            moveTo_x(5);
        }
        else if(val=="6")
        {
            buzz(1);
            moveTo_x(-5);
        }

        else if(val=="7")
        {
            buzz(1);
            moveTo_y(5);
        }

        else if(val=="8")
        {
            buzz(1);
            moveTo_y(-5);
        }
        else
        {
          buzz(1);
          if(val.length()!=1)
          {
            int index=2;
            while(val[index]!=',')
            {
              b_count+=val[index];
              index+=1;
            }
            index+=1;
            while(index<val.length())
            {
              pt_count+=val[index];
              index+=1;
            }
          }
          Pt_count = pt_count.toInt();
          B_count = b_count.toInt();
          break;
        }
    }
  }
}

// Loop function
void loop()
{
  int index;
  ESP_BT.println("NEXT");

  if(ESP_BT.available())
  {
    String val = ESP_BT.readStringUntil('\n');
    Serial.println(val);
    if(val.length()!=1)
    {
      index=0;
      while(val[index]!=',')
      {
        Data_x+=val[index];
        index+=1;
      }
      index+=1;
      while(val[index]!=',')
      {
        Data_y+=val[index];
        index+=1;
      }
      index+=1;
      while(index<val.length())
      {
        Rad+=val[index];
        index+=1;
      }
      data_x=Data_x.toInt();
      data_y=Data_y.toInt();
      rad=Rad.toInt();
      Serial.print("Steps_x:");
      Serial.print(data_x);
      Serial.print("Steps_y:");
      Serial.println(data_y);
      Data_x="";
      Data_y="";
      Rad="";
      moveTo_x(data_x);
      moveTo_y(data_y);
      delay(500);
      time_to_solder=rad*1000;
      //Z-axis move up and down
  
      move_down(140);
      extrude(time_to_solder);
      move_up(500);
      pt_cnt+=1;
      if(pt_cnt==(Pt_count-1))
      {
        pt_cnt=0;
        brd_ct+=1;
        Serial.println("1 board completed.");
        buzz(2);
        while(brd_ct>=B_count)
        {
            //brd_ct=0;
            Serial.println("All boards completed.");
            buzz(10);
            ESP.restart();
        }
      }
    }
  }
}
