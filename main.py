MAP = "█████" \
      "█ ■ █" \
      "█■  █" \
      "█████"
WIDTH = 5
HEIGHT = len(MAP) // WIDTH
POS_X = 1
POS_Y = 1
TURN_LIMIT = 4
V_CELL = True
V_CELL_X = 3
V_CELL_Y = 2


conditions = []


class Condition:
    def __init__(self, scheme, pos_x, pos_y, turn, route, done):
        self.scheme = scheme
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.turn = turn
        self.route = route
        self.done = done
        if V_CELL and self.pos_x == V_CELL_X and self.pos_y == V_CELL_Y:
            self.done = True
        elif self.turn > TURN_LIMIT:
            pass
        elif abs(self.pos_x - V_CELL_X) + abs(self.pos_y - V_CELL_Y) > TURN_LIMIT - self.turn:
            pass
        else:
            self.generate_new()

    def neighbours(self):
        """
        0 - move
        1 - push
        2 - act
        3 - hit
        """
        neighbours = []
        for direction in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            if self.scheme[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]] == ' ' and \
                    not (self.route[-1][1] == 0 and
                         (direction[0] + self.route[-1][0][0] == 0 and direction[1] + self.route[-1][0][1] == 0)):
                neighbours.append((direction, 0))
            elif self.scheme[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]] == '■' and \
                    self.scheme[(self.pos_y + 2 * direction[1]) * WIDTH + self.pos_x + 2 * direction[0]] == ' ':
                neighbours.append((direction, 1))
        return neighbours

    def generate_new(self):
        for neighbour in self.neighbours():
            if neighbour[1] == 1:
                self.scheme[(self.pos_y + neighbour[0][1]) * WIDTH + self.pos_x + neighbour[0][0]] = ' '
                self.scheme[(self.pos_y + 2 * neighbour[0][1]) * WIDTH + self.pos_x + 2 * neighbour[0][0]] = '■'
            conditions.append(Condition(self.scheme,
                                        self.pos_x + (neighbour[0][0] if not neighbour[1] else 0),
                                        self.pos_y + (neighbour[0][1] if not neighbour[1] else 0),
                                        self.turn + 1,
                                        self.route + [neighbour],
                                        False))


conditions.append(Condition(list(MAP), POS_X, POS_Y, 0, [], False))
fastest = TURN_LIMIT + 1
best_condition = None
solutions = 0
for condition in conditions:
    if condition.done and condition.turn < fastest:
        best_condition = condition
        fastest = condition.turn
        solutions = 1
    elif condition.done and condition.turn == fastest:
        solutions += 1
print("Checked", len(conditions), "possible condition..." if len(conditions) == 1 else "possible conditions....")
print("Found", solutions, "solution." if solutions == 1 else "solutions.")
print("Solution example:", best_condition.turn, best_condition.route)
