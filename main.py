MAP = "█████" \
      "█   █" \
      "█  ■█" \
      "█████"
WIDTH = 5
HEIGHT = len(MAP) // WIDTH
POS_X = 1
POS_Y = 1
TURN_LIMIT = 3


conditions = []


class Condition:
    def __init__(self, scheme, pos_x, pos_y, turn, route, done):
        self.scheme = scheme
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.turn = turn
        self.route = route
        self.done = done
        if self.scheme[self.pos_y * WIDTH + self.pos_x] == '■':
            self.done = True
        elif self.turn > TURN_LIMIT:
            pass
        else:
            self.generate_new()

    def neighbours(self):
        neighbours = []
        for direction in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            if self.scheme[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]] in (' ', '■'):
                neighbours.append(direction)
        return neighbours

    def generate_new(self):
        for neighbour in self.neighbours():
            conditions.append(Condition(self.scheme,
                                        self.pos_x + neighbour[0],
                                        self.pos_y + neighbour[1],
                                        self.turn + 1,
                                        self.route + [neighbour],
                                        False))


conditions.append(Condition(MAP, POS_X, POS_Y, 0, [], False))
fastest = TURN_LIMIT + 1
best_condition = None
for condition in conditions:
    if condition.done and condition.turn < fastest:
        best_condition = condition
        fastest = condition.turn
print(best_condition.turn, best_condition.route)
