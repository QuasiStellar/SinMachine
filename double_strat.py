DEBUG = False
MAP = "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛" \
      "⬛⬛⬛⯆⯆⬛◐⯆▧⬛⬛" \
      "⬛⬛◐⬜⯈⬜⬜⬜▧⬛⬛" \
      "⬛⬜▧⬜⬜⬜⬜⬜▧⬜⬛" \
      "⬛⬜⬜⬜⬜⬜▧⬜▧⬜⬛" \
      "⬛⬛⬛⬜⬜⬜⬜⬜▧⬜⬛" \
      "⬛⬛⬛⬛⬛⬛⬛⬜⬜⬜⬛" \
      "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛"
END_MAP = "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛" \
          "⬛⬛⬛⯆⯆⬛◑⯆▧⬛⬛" \
          "⬛⬛◑▧⯈▧⬜▧▧⬛⬛" \
          "⬛⬜⬜⬜▧⬜⬜⬜⬜⬜⬛" \
          "⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜⬛" \
          "⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜⬛" \
          "⬛⬛⬛⬛⬛⬛⬛⬜▧⬜⬛" \
          "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛"
MAP = list(MAP)
END_MAP = list(END_MAP)
WIDTH = 11
HEIGHT = len(MAP) // WIDTH
POS_X = 8
POS_Y = 6
END_POS_X = 6
END_POS_Y = 2
TURN_LIMIT = 49
# MAP = "⬛⬛⬛⬛⬛⬛⬛" \
#       "⬛⬜⬜⬜⬜⬜⬛" \
#       "⬛⬜⬜▧⬜⬜⬛" \
#       "⬛⬜⬜⬜⬜⬜⬛" \
#       "⬛⯈⬜⬜⬜⬜⬛" \
#       "⬛◐⬜⬜⬜⬜⬛" \
#       "⬛⬛⬛⬛⬛⬛⬛"
# END_MAP = "⬛⬛⬛⬛⬛⬛⬛" \
#           "⬛⬜⬜⬜⬜⬜⬛" \
#           "⬛⬜⬜⬜⬜⬜⬛" \
#           "⬛⬜⬜⬜⬜⬜⬛" \
#           "⬛⯈⬜▧⬜⬜⬛" \
#           "⬛◑⬜⬜⬜⬜⬛" \
#           "⬛⬛⬛⬛⬛⬛⬛"
# MAP = list(MAP)
# END_MAP = list(END_MAP)
# WIDTH = 7
# HEIGHT = len(MAP) // WIDTH
# POS_X = 1
# POS_Y = 1
# END_POS_X = 2
# END_POS_Y = 5
# TURN_LIMIT = 12
FORWARD_TL = TURN_LIMIT // 2
BACKWARD_TL = TURN_LIMIT - FORWARD_TL


forward_conditions = []
forward_condition_set = {}
backward_conditions = []
backward_condition_set = {}


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


class FCondition:
    def __init__(self, scheme, lasers, pos_x, pos_y, turn, route):
        self.scheme = scheme
        self.lasers = lasers
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.turn = turn
        self.route = route
        if self.turn > FORWARD_TL:
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
                                                  (direction[0] + self.route[-1][0][0] == 0 and
                                                   direction[1] + self.route[-1][0][1] == 0))) and \
                    not self.lasers[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]]:
                neighbours.append((direction, 0))
            elif self.scheme[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]] == '▧' and \
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
            condition_hash = hash((tuple(new_scheme), new_pos_x, new_pos_y))
            if condition_hash in forward_condition_set and forward_condition_set[condition_hash][0] >= self.turn or \
                    condition_hash not in forward_condition_set:
                forward_condition_set[condition_hash] = (self.turn, self.route + [neighbour])
                forward_conditions.append(FCondition(new_scheme,
                                                     new_lasers,
                                                     new_pos_x,
                                                     new_pos_y,
                                                     self.turn + 1,
                                                     self.route + [neighbour]))


class BCondition:
    def __init__(self, scheme, lasers, pos_x, pos_y, turn, route):
        self.scheme = scheme
        self.lasers = lasers
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.turn = turn
        self.route = route
        if self.turn > BACKWARD_TL:
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
            if self.scheme[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]] == '◑':
                return [(direction, 2)]
            elif self.scheme[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]] == '⬜' and \
                    self.scheme[(self.pos_y + 2 * direction[1]) * WIDTH + self.pos_x + 2 * direction[0]] == '▧':
                neighbours.append((direction, 1))
            elif self.scheme[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]] == '⬜' and \
                    (len(self.route) == 0 or not (self.route[-1][1] == 0 and
                                                  (direction[0] + self.route[-1][0][0] == 0 and
                                                   direction[1] + self.route[-1][0][1] == 0))) and \
                    not self.lasers[(self.pos_y + direction[1]) * WIDTH + self.pos_x + direction[0]]:
                neighbours.append((direction, 0))
        return neighbours

    def generate_new(self):
        for neighbour in self.neighbours():
            new_scheme = self.scheme.copy()
            new_lasers = self.lasers.copy()
            new_pos_x = self.pos_x + (neighbour[0][0] if not neighbour[1] else 0)
            new_pos_y = self.pos_y + (neighbour[0][1] if not neighbour[1] else 0)
            if neighbour[1] == 1:
                new_scheme[(self.pos_y + neighbour[0][1]) * WIDTH + self.pos_x + neighbour[0][0]] = '▧'
                new_scheme[(self.pos_y + 2 * neighbour[0][1]) * WIDTH + self.pos_x + 2 * neighbour[0][0]] = '⬜'
                neighbour = ((-neighbour[0][0], -neighbour[0][1]), neighbour[1])
                new_lasers = update_lasers(new_scheme)
            elif neighbour[1] == 2:
                new_scheme[(self.pos_y + neighbour[0][1]) * WIDTH + self.pos_x + neighbour[0][0]] = '◐'
                neighbour = ((-neighbour[0][0], -neighbour[0][1]), neighbour[1])
                new_lasers = update_lasers(new_scheme)
            condition_hash = hash((tuple(new_scheme), new_pos_x, new_pos_y))
            if condition_hash in backward_condition_set and backward_condition_set[condition_hash][0] >= self.turn or \
                    condition_hash not in backward_condition_set:
                backward_condition_set[condition_hash] = (self.turn, self.route + [neighbour])
                backward_conditions.append(BCondition(new_scheme,
                                                     new_lasers,
                                                     new_pos_x,
                                                     new_pos_y,
                                                     self.turn + 1,
                                                     self.route + [neighbour]))


forward_conditions.append(FCondition(MAP, update_lasers(MAP), POS_X, POS_Y, 0, []))
backward_conditions.append(BCondition(END_MAP, update_lasers(END_MAP), END_POS_X, END_POS_Y, 0, []))

directions = {(1, 0): '🠖', (-1, 0): '🠔', (0, 1): '🠗', (0, -1): '🠕'}
backward_directions = {(1, 0): '🠔', (-1, 0): '🠖', (0, 1): '🠕', (0, -1): '🠗'}

print("Checked", len(forward_conditions), "possible conditions while going forwards...")
print(len(forward_condition_set.keys()), "of them were distinct.")
print("Checked", len(backward_conditions), "possible conditions while going backwards...")
print(len(backward_condition_set.keys()), "of them were distinct.")
solutions = tuple(set(forward_condition_set.keys()).intersection(set(backward_condition_set.keys())))
if solutions:
    print("Possible solutions (not all of them):")
else:
    print("There are no solutions :(")
for i in range(len(solutions)):
    print(*[directions[move[0]] for move in forward_condition_set[solutions[i]][1]],
          *reversed([backward_directions[move[0]] for move in backward_condition_set[solutions[i]][1]]))
