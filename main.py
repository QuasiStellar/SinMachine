DEBUG = False
MAP = "⬛⬛⬛⬛⬛" \
      "⬛⬜⬜⬜⬛" \
      "⬛▧⬜◐⬛" \
      "⬛⬜⬜⬜⬛" \
      "⬛⬛⬛⬛⬛"
MAP = list(MAP)
WIDTH = 5
HEIGHT = len(MAP) // WIDTH
POS_X = 1
POS_Y = 1
TURN_LIMIT = 3
V_CELL = False
V_CELL_X = 3
V_CELL_Y = 2
GEN_COUNT = MAP.count('◐')


conditions = []


class Condition:
    def __init__(self, scheme, pos_x, pos_y, turn, route, gen_count, done):
        self.scheme = scheme
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.turn = turn
        self.route = route
        self.gen_count = gen_count
        self.done = done
        if V_CELL and self.pos_x == V_CELL_X and self.pos_y == V_CELL_Y:
            self.done = True
        if not V_CELL and gen_count == 0:
            self.done = True
        elif self.turn >= TURN_LIMIT:
            pass
        elif V_CELL and abs(self.pos_x - V_CELL_X) + abs(self.pos_y - V_CELL_Y) > TURN_LIMIT - self.turn:
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
            if self.scheme[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]] == '◐':
                return [(direction, 2)]
            elif self.scheme[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]] == '⬜' and \
                    (len(self.route) == 0 or not (self.route[-1][1] == 0 and
                         (direction[0] + self.route[-1][0][0] == 0 and direction[1] + self.route[-1][0][1] == 0))):
                neighbours.append((direction, 0))
            elif self.scheme[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]] == '▧' and \
                    self.scheme[(self.pos_y + 2 * direction[1]) * WIDTH + self.pos_x + 2 * direction[0]] == '⬜':
                neighbours.append((direction, 1))
        return neighbours

    def generate_new(self):
        for neighbour in self.neighbours():
            new_scheme = self.scheme.copy()
            if neighbour[1] == 1:
                new_scheme[(self.pos_y + neighbour[0][1]) * WIDTH + self.pos_x + neighbour[0][0]] = '⬜'
                new_scheme[(self.pos_y + 2 * neighbour[0][1]) * WIDTH + self.pos_x + 2 * neighbour[0][0]] = '▧'
            elif neighbour[1] == 2:
                new_scheme[(self.pos_y + neighbour[0][1]) * WIDTH + self.pos_x + neighbour[0][0]] = '◑'
                self.gen_count -= 1
            conditions.append(Condition(new_scheme,
                                        self.pos_x + (neighbour[0][0] if not neighbour[1] else 0),
                                        self.pos_y + (neighbour[0][1] if not neighbour[1] else 0),
                                        self.turn + 1,
                                        self.route + [neighbour],
                                        self.gen_count,
                                        False))


conditions.append(Condition(list(MAP), POS_X, POS_Y, 0, [], GEN_COUNT, False))
fastest = TURN_LIMIT + 1
solutions = []
for condition in conditions:
    if DEBUG:
        print(condition.turn, condition.route)
    if condition.done and condition.turn < fastest:
        fastest = condition.turn
        solutions = [condition]
    elif condition.done and condition.turn == fastest:
        solutions.append(condition)
print("Checked", len(conditions), "possible condition..." if len(conditions) == 1 else "possible conditions....")
print("Found", len(solutions), "solution." if len(solutions) == 1 else "solutions.")
for solution in solutions:
    print(solution.turn, solution.route)
