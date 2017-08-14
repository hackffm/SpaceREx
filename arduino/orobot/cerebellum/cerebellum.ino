#define M1IN1 32
#define M1IN2 33
#define M1D2 3
#define M2IN1 30
#define M2IN2 31
#define M2D2 2


void setup() {
  Serial.begin(9600);
  
  pinMode(M1D2, OUTPUT);
  pinMode(M1IN1, OUTPUT);
  pinMode(M1IN2, OUTPUT);
  
  pinMode(M2D2, OUTPUT);
  pinMode(M2IN1, OUTPUT);
  pinMode(M2IN2, OUTPUT);


  digitalWrite(M1IN1, HIGH);
  digitalWrite(M1IN2, LOW);
  analogWrite(M1D2, 90);
  
  digitalWrite(M2IN1, HIGH);
  digitalWrite(M2IN2, LOW);
  analogWrite(M2D2, 150);
  
}

void loop() {

}
