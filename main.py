DEBUG = False
# MAP = "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛" \
#       "⬛⬛⬛⯆⯆⬛◐⯆▧⬛⬛" \
#       "⬛⬛◐⬜⯈⬜⬜⬜▧⬛⬛" \
#       "⬛⬜▧⬜⬜⬜⬜⬜▧⬜⬛" \
#       "⬛⬜⬜⬜⬜⬜▧⬜▧⬜⬛" \
#       "⬛⬛⬛⬜⬜⬜⬜⬜▧⬜⬛" \
#       "⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬛" \
#       "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛"
MAP = "⬛⬛⬛⬛⬛⬛⬛" \
      "⬛⬜⬜⬜⬜⬜⬛" \
      "⬛⬜⬜▧⬜⬜⬛" \
      "⬛⬜⬜⬜⬜⬜⬛" \
      "⬛⯈⬜⬜⬜⬜⬛" \
      "⬛◐⬜⬜⬜⬜⬛" \
      "⬛⬛⬛⬛⬛⬛⬛"
MAP = list(MAP)
WIDTH = 7
HEIGHT = len(MAP) // WIDTH
POS_X = 1
POS_Y = 1
TURN_LIMIT = 12
V_CELL = False
V_CELL_X = 3
V_CELL_Y = 2
GEN_COUNT = MAP.count('◐')
TURN_LIMIT -= GEN_COUNT


def update_lasers(scheme):
    lasers = [0 for _ in range(len(MAP))]
    for i in range(len(MAP)):
        if scheme[i] == '⯈':
            for j in range(1, WIDTH):
                if scheme[i + j] in ['⬜', '⯈', '⯇', '⯆', '⯅']:
                    lasers[i + j] = 1
                else:
                    break
        elif scheme[i] == '⯇':
            for j in range(1, WIDTH):
                if scheme[i - j] in ['⬜', '⯈', '⯇', '⯆', '⯅']:
                    lasers[i - j] = 1
                else:
                    break
        elif scheme[i] == '⯆':
            for j in range(1, HEIGHT):
                if scheme[i + j * WIDTH] in ['⬜', '⯈', '⯇', '⯆', '⯅']:
                    lasers[i + j * WIDTH] = 1
                else:
                    break
        elif scheme[i] == '⯅':
            for j in range(1, HEIGHT):
                if scheme[i - j * WIDTH] in ['⬜', '⯈', '⯇', '⯆', '⯅']:
                    lasers[i - j * WIDTH] = 1
                else:
                    break
    return lasers


conditions = []
condition_set = {}


class Condition:
    def __init__(self, scheme, lasers, pos_x, pos_y, turn, route, gen_count, done):
        self.scheme = scheme
        self.lasers = lasers
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
        elif self.turn > TURN_LIMIT:
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
            next_cell = self.scheme[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]]
            if next_cell == '◐':
                return [(direction, 2)]
            elif next_cell == '⬜' and (len(self.route) == 0 or not (self.route[-1][1] == 0 and
                                                                    (direction[0] + self.route[-1][0][0] == 0 and
                                                                     direction[1] + self.route[-1][0][1] == 0))) and \
                    not self.lasers[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]]:
                neighbours.append((direction, 0))
            elif next_cell == '▧' and \
                    self.scheme[(self.pos_y + 2 * direction[1]) * WIDTH + self.pos_x + 2 * direction[0]] == '⬜':
                neighbours.append((direction, 1))
        return neighbours

    def generate_new(self):
        for neighbour in self.neighbours():
            new_scheme = self.scheme.copy()
            new_lasers = self.lasers.copy()
            new_pos_x = self.pos_x + (neighbour[0][0] if not neighbour[1] else 0)
            new_pos_y = self.pos_y + (neighbour[0][1] if not neighbour[1] else 0)
            if neighbour[1] == 1:
                new_scheme[(self.pos_y + neighbour[0][1]) * WIDTH + self.pos_x + neighbour[0][0]] = '⬜'
                new_scheme[(self.pos_y + 2 * neighbour[0][1]) * WIDTH + self.pos_x + 2 * neighbour[0][0]] = '▧'
                new_lasers = update_lasers(new_scheme)
            elif neighbour[1] == 2:
                new_scheme[(self.pos_y + neighbour[0][1]) * WIDTH + self.pos_x + neighbour[0][0]] = '◑'
                new_lasers = update_lasers(new_scheme)
                self.gen_count -= 1
                self.turn -= 1
            condition_hash = hash((tuple(new_scheme), new_pos_x, new_pos_y))
            if condition_hash in condition_set and condition_set[condition_hash] >= self.turn or \
                    condition_hash not in condition_set:
                condition_set[condition_hash] = self.turn
                conditions.append(Condition(new_scheme,
                                            new_lasers,
                                            new_pos_x,
                                            new_pos_y,
                                            self.turn + 1,
                                            self.route + [neighbour],
                                            self.gen_count,
                                            False))


conditions.append(Condition(MAP, update_lasers(MAP), POS_X, POS_Y, 0, [], GEN_COUNT, False))
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
print("Checked", len(conditions), "possible condition..." if len(conditions) == 1 else "possible conditions...")
print("Found", len(solutions), "solution." if len(solutions) == 1 else "solutions.")
directions = {(1, 0): '🠖', (-1, 0): '🠔', (0, 1): '🠗', (0, -1): '🠕'}
for solution in solutions:
    print(*[directions[move[0]] for move in solution.route])
