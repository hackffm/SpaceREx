#define M1IN1 32
#define M1IN2 33
#define M1D2 3
#define M2IN1 30
#define M2IN2 31
#define M2D2 2


void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  
  pinMode(M1D2, OUTPUT);
  pinMode(M1IN1, OUTPUT);
  pinMode(M1IN2, OUTPUT);
  
  pinMode(M2D2, OUTPUT);
  pinMode(M2IN1, OUTPUT);
  pinMode(M2IN2, OUTPUT);


  digitalWrite(M1IN1, HIGH);
  digitalWrite(M1IN2, LOW);
  analogWrite(M1D2, 0);
  
  digitalWrite(M2IN1, HIGH);
  digitalWrite(M2IN2, LOW);
  analogWrite(M2D2, 0);
  
}

void loop() {
  receive_serial_cmd();
}

void receive_serial_cmd(void) {
  static uint8_t cmd[18];         // command buffer
  static uint8_t cmdcount = 0;    // position in the buffer of the received byte
  uint8_t c;                      // received byte
  while(Serial1.available()) {
    c = Serial1.read();
    if(c > ' ') cmd[cmdcount++] = c;
    if((c == 8) && (cmdcount > 0)) cmdcount--;                // deals with backspaces, if a person on the other side types 
    if((c == 0x0d) || (c == 0x0a) || (cmdcount > 16)) {       // end of command, gets interpreted now
      cmd[cmdcount] = 0;    // clear the last byte in cmd buffer
      if(cmdcount > 0) {    // prevent empty cmd buffer parsing
       switch(cmd[0]) {
        case 'l': 
          if((cmdcount > 2) && (cmdcount < 7)) {
            int temp = atoi((const char *)&cmd[1]);           
            Serial.print("l:");
            Serial.println(temp);  
            if(temp > 0) {
              if(temp > 255) temp = 255;
              digitalWrite(M1IN1, HIGH);
              digitalWrite(M1IN2, LOW);
              analogWrite(M1D2, temp);                    
            } else {
              temp = -temp;
              if(temp > 255) temp = 255;
              digitalWrite(M1IN1, LOW);
              digitalWrite(M1IN2, HIGH);
              analogWrite(M1D2, temp); 
            }
          }                    
          break; 
          case 'r':
           if((cmdcount > 2) && (cmdcount < 7)) {
            int temp = atoi((const char *)&cmd[1]);           
            Serial.print("r:");
            Serial.println(temp);
            
            if(temp > 0) {
              if(temp > 255) temp = 255;
              digitalWrite(M2IN1, HIGH);
              digitalWrite(M2IN2, LOW);
              analogWrite(M2D2, temp);                    
            } else {
              temp = -temp;
              if(temp > 255) temp = 255;
              digitalWrite(M2IN1, LOW);
              digitalWrite(M2IN2, HIGH);
              analogWrite(M2D2, temp); 
            }                        
          }  
          break;                 
       }    
      }
      cmdcount = 0;
    } 
  }
}
