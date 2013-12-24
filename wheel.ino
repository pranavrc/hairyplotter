// lw - Output pin of left wheel.
// rw - Output pin of right wheel.

const int lw=11;
const int rw=12;
int option = 52;

void setup() {
    pinMode(lw, OUTPUT);
    pinMode(rw, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        option = Serial.read();
        Serial.println(option);
    }

    switch (option) {
        // Write signals to output pins based on input
        // from the backend code.

        // A HIGH signal activates the wheel while
        // a LOW signal switches it off.
        case 49:
            digitalWrite(lw, HIGH);
            digitalWrite(rw, HIGH);
        break;
        case 50:
            digitalWrite(lw, HIGH);
            digitalWrite(rw, LOW);
        break;
        case 51:
            digitalWrite(lw, LOW);
            digitalWrite(rw, HIGH);
        break;
        default:
            digitalWrite(lw, LOW);
            digitalWrite(rw, LOW);
        break;
    }
}
