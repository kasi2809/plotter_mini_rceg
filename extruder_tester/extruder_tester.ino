const int motor_R = 23;
const int motor_L = 22;
const int extruder_speed = 16;
int pot_value=0;
int pot_pin=34;
void setup() {
  pinMode(motor_R,OUTPUT);
  pinMode(motor_L,OUTPUT);
  pinMode(extruder_speed,OUTPUT);
  pinMode(pot_pin,INPUT);
  Serial.begin(115200);

  
  ledcSetup(0, 1000, 10);
ledcAttachPin(extruder_speed, 0);

  // put your setup code here, to run once:

}

void loop() {
  pot_value=analogRead(pot_pin);
  pot_value=map(pot_value,0,4095,0,1024);
  Serial.println(pot_value);
  ledcWrite(0,715);
  digitalWrite(motor_R,HIGH);
  digitalWrite(motor_L,LOW);
  
  
  // put your main code here, to run repeatedly:

}
