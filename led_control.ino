int redPin = 9;
int greenPin = 10;
int bluePin = 11;

bool randomMode = false;

void setup() {
  Serial.begin(9600);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  randomSeed(analogRead(0));  // 랜덤 초기값 설정
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();

    // 모든 LED 끄기
    digitalWrite(redPin, LOW);
    digitalWrite(greenPin, LOW);
    digitalWrite(bluePin, LOW);
    
    randomMode = false;  // 랜덤모드 기본 OFF

    if (cmd == '1') {
      digitalWrite(redPin, HIGH);  // 빨간색
    } else if (cmd == '2') {
      digitalWrite(greenPin, HIGH);  // 초록색
    } else if (cmd == '3') {
      digitalWrite(bluePin, HIGH);  // 파란색
    } else if (cmd == '4') {
      randomMode = true;  // 랜덤모드 ON
    }
  }

  if (randomMode) {
    digitalWrite(redPin, random(0, 2));
    digitalWrite(greenPin, random(0, 2));
    digitalWrite(bluePin, random(0, 2));
    delay(200);  // 깜빡이는 속도 조절
  }
}
