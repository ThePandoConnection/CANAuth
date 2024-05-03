double value = 0;
double voltage;
double resolution = 1.6383;


void setup(){
  analogReadResolution(14);
  Serial.begin(9600);  
}


void loop(){
  value = analogRead(A0);
  voltage = (value * 5.00000/resolution);
  Serial.println(voltage);

}