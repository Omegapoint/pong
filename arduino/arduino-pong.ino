static const int NR_POSITION_DIFFS = 4;
static const char SEPARATOR[] = "¤";
static const char FIRE_EVENT_NAME[] = "FIRE";
static const char *FIRE_EVENTS[] = {"UP", "DN"};
static const char POSITION_EVENT_NAME[] = "PADL";

struct Player {
  const int id;
  const int firePin;
  const int positionPin;

  bool firePressed;
  int position;
  int positionDiffs[NR_POSITION_DIFFS];
};

Player player1 = {
  .id = 0,
  .firePin = 2,
  .positionPin = A0,

  .firePressed = false,
  .position = 0,
  .positionDiffs = {0, 0, 0, 0}
};

Player player2 {
  .id = 1,
  .firePin = 4,
  .positionPin = A1,

  .firePressed = false,
  .position = 0,
  .positionDiffs = {0, 0, 0, 0}
};

void update(Player *const player);
void outputStr(int id, char *event, char *value);
void outputInt(int id, char *event, int value);
void outputFireEvent(Player *const player);
void outputPositionEvent(Player *const player);

bool updateFireState(Player *player);
void updatePosition(Player *const player, const int position);
bool positionOscillating(Player *const player);
bool updatePositionState(Player *const player);

void update(Player *const player) {
  if (updateFireState(player)) {
    outputFireEvent(player);
  }
  if (updatePositionState(player)) {
    outputPositionEvent(player);
  }
}

void outputInt(int id, char *event, int value) {
  Serial.print(id, HEX);
  Serial.print(SEPARATOR);
  Serial.print(event);
  Serial.print(SEPARATOR);
  Serial.println(value);
}

void outputStr(int id, char *event, char *value) {
  Serial.print(id, HEX);
  Serial.print(SEPARATOR);
  Serial.print(event);
  Serial.print(SEPARATOR);
  Serial.println(value);
}

void outputFireEvent(Player *const player) {
  outputStr(player->id, FIRE_EVENT_NAME, FIRE_EVENTS[player->firePressed]);
}

void outputPositionEvent(Player *const player) {
  outputInt(player->id, POSITION_EVENT_NAME, player->position);
}

bool updateFireState(Player *player) {
  bool firePressed = digitalRead(player->firePin);
  if (firePressed != player->firePressed) {
    player->firePressed = firePressed;
    return true;
  }
  return false;
}

void updatePosition(Player *const player, const int position) {
  int i = 0;
  // Rotate diffs left
  for (; i < NR_POSITION_DIFFS - 1; i++) {
    player->positionDiffs[i] = player->positionDiffs[i + 1];
  }
  // Add latest diff last in array
  player->positionDiffs[i] = position - player->position;
  player->position = position;
}

bool positionOscillating(Player *const player) {
  bool oscillating = true;
  for (int i = 0; i < NR_POSITION_DIFFS - 1; i++) {
    oscillating = oscillating && (player->positionDiffs[i] == -player->positionDiffs[i + 1]);
  }
  return oscillating;
}

bool updatePositionState(Player *const player) {
  int position = analogRead(player->positionPin) / 2;
  if (position != player->position) {
    updatePosition(player, position);
    if (!positionOscillating(player)) {
      return true;
    }
  }
  return false;
}

void setup() {
  Serial.begin(9600);
  pinMode(player1.firePin, INPUT);
  pinMode(player2.firePin, INPUT);
}

void loop() {
  update(&player1);
  update(&player2);
}


