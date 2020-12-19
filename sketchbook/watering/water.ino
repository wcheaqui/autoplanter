int IN1 = 2;
int IN2 = 3;
int IN3 = 4;
int IN4 = 5;

int Pin1 = A0; 
int Pin2 = A1;
int Pin3 = A2;
int Pin4 = A3;

float value1 = 0;
float value2 = 0;
float value3 = 0;
float value4 = 0;
void setup() {
	Serial.begin(9600);
	pinMode(IN1, OUTPUT);
	delay(500);
}
void loop() {

	Serial.print("MOISTURE LEVEL1:");
	value1 = ((analogRead(Pin1) * -1) + 382) / 3;
	Serial.println(value1);
	if(value1>750)
	{
		digitalWrite(IN1, LOW);
	}
	else
	{
		digitalWrite(IN1, HIGH);
	}
    
	delay(1000);
}
