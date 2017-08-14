#define M2IN1 8
#define M2IN2 7
#define M2D1 6
#define M2D2 9
#define FB A0
#define SF 4

int fb = 0;
int sf = LOW;

void setup() {
  Serial.begin(9600);
  pinMode(M2D2, OUTPUT);
  pinMode(M2IN1, OUTPUT);
  pinMode(M2IN2, OUTPUT);
  //pinMode(FB, INPUT);
  //pinMode(SF, INPUT);

  digitalWrite(M2IN1, HIGH);
  digitalWrite(M2IN2, LOW);
  analogWrite(M2D2, 150);
  digitalWrite(M2D1, LOW);
}

void loop() {
  /*
  delay(100);
  fb = analogRead(FB);
  Serial.println(fb);
  sf = digitalRead(SF);
  Serial.print("SF: ");
  Serial.println(sf);
  */
}
