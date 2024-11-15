// Définir les pins pour les boutons
const int bouton1Pin = 2;  // Pin numérique 2
const int bouton2Pin = 3;  // Pin numérique 3



void setup() {
  pinMode(bouton1Pin, INPUT);  // Pas de résistance pull-up ici
  pinMode(bouton2Pin, INPUT);  // Pas de résistance pull-up ici

  Serial.begin(9600);
}

void loop() {

  if (digitalRead(bouton1Pin) == HIGH) {
    Serial.println("R");
  }

  if (digitalRead(bouton2Pin) == HIGH) {
    Serial.println("L");
  }

  delay(10);
}
