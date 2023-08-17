import sys
from enum import Enum
import copy

class Sokoban:
    class Icons(Enum):
        WALL = '#'
        FLOOR = ' '
        GOAL = '.'
        BOX = '$'
        BOX_ON_GOAL = '*'
        PLAYER = '@'
        PLAYER_ON_GOAL = '+'

    class Direction(Enum):
        LEFT = (-1, 0)
        RIGHT = (1, 0)
        UP = (0, -1)
        DOWN = (0, 1)
        NONE = (0, 0)


    def is_valid_value(self, c) -> bool:
        valid_values = {
            self.Icons.FLOOR.value,
            self.Icons.WALL.value,
            self.Icons.GOAL.value,
            self.Icons.BOX.value,
            self.Icons.BOX_ON_GOAL.value,
            self.Icons.PLAYER.value,
            self.Icons.PLAYER_ON_GOAL.value,
        }
        return c in valid_values

    def get_valid_directions(self):
        valid_moves = []
        for direction in Sokoban.Direction:
            if (self.can_move(direction) or self.can_push(direction)) and direction != self.Direction.NONE:
                valid_moves.append(direction)
        return valid_moves

    def __init__(self, level: int, levels_file: str):
        self.level_state = []
        self.boxes = set()
        self.goals = set()
        self.player=(0,0)

        x=0
        y=0
        # levels_file will have all the sokoban levels inside them
        # level lets you choose which one to play

        if level < 1:
            print("ERROR: Level " + str(level) + " does not exist")
            sys.exit(1)

        # I have to load the level to the level_state matrix
        file = open(levels_file, "r")
        level_found = False
        for line in file:
            if not level_found:
                if "Level " + str(level) == line.strip():
                    level_found = True
            else:
                # si se termino el nivel -> salgo del loop
                if line.strip() == "":
                    break

                row = []
                for c in line:
                    if c == "\n":
                        y+=1
                        x=0
                        continue

                    if not self.is_valid_value(c):
                        print(
                            "ERROR: Level " + str(level) + " has invalid value " + c
                        )
                        sys.exit(1)

                    row.append(self.Icons(c))
                    point= (x,y)
                    match c:
                        case '$':
                            self.boxes.add(point)
                        case '.':
                            self.goals.add(point)
                        case '*':
                            self.boxes.add(point)
                            self.goals.add(point)
                        case '+':
                            self.player=(x,y)
                            self.goals.add(point)
                        case '@':
                            self.player=(x,y)
                    x+=1
                self.level_state.append(row)

    def get_level_state(self):
        return self.level_state

    def get_player(self):
        return self.player

    def get_boxes(self):
        return self.boxes

    def get_goals(self):
        return self.goals

    def set_level_state(self, new_level_state):
        self.level_state = copy.deepcopy(new_level_state)

    def set_player(self, player):
        self.player = player

    def set_boxes(self, boxes):
        self.boxes = copy.deepcopy(boxes)

    def set_goals(self, goals):
        self.goals = copy.deepcopy(goals)

    def set_status(self,new_level_state,play,boxes,goals):
        self.level_state=copy.deepcopy(new_level_state)
        self.player=play
        self.boxes=copy.deepcopy(boxes)
        self.goals=copy.deepcopy(goals)

    def print_level_state(self):
        for row in self.level_state:
            row_str = "".join([char.value for char in row])
            print(row_str, end="\n")

    def get_cell_content(self, x: int, y: int) -> Icons:
        if (
            x < 0
            or y < 0
            or y >= len(self.level_state)
            or x >= len(self.level_state[y])
        ):
            return self.Icons.WALL

        return self.level_state[y][x]

    def set_cell_content(self, x: int, y: int, content: Icons):
        if (
            x < 0
            or y < 0
            or y >= len(self.level_state)
            or x >= len(self.level_state[y])
        ):
            raise RuntimeError("Cell is out of bounds")

        self.level_state[y][x] = content

    def level_complete(self) -> bool:
        for box in self.boxes:
            if box not in self.goals:
                return False
        return True

    # private
    def _move_box(self, x: int, y: int, x_diff: int, y_diff: int):
        box_cell = self.get_cell_content(x, y)
        valid_box_cells = [self.Icons.BOX, self.Icons.BOX_ON_GOAL]

        if box_cell not in valid_box_cells:
            raise RuntimeError("Cell is not a box")

        target_cell = self.get_cell_content(x + x_diff, y + y_diff)
        valid_target_cells = [self.Icons.FLOOR, self.Icons.GOAL]

        if target_cell not in valid_target_cells:
            raise RuntimeError("Cell is not a valid box target")

        new_box_cell = (
            self.Icons.FLOOR if box_cell == self.Icons.BOX else self.Icons.GOAL
        )
        new_target_cell = (
            self.Icons.BOX
            if target_cell == self.Icons.FLOOR
            else self.Icons.BOX_ON_GOAL
        )

        point= (x,y)
        new_point=(x+x_diff,y+y_diff)
        self.boxes.remove(point)
        self.boxes.add(new_point)

        self.set_cell_content(x, y, new_box_cell)
        self.set_cell_content(x + x_diff, y + y_diff, new_target_cell)

    def can_move(self, direction: Direction) -> bool:
        player_x, player_y = self.player
        x_diff, y_diff = direction.value

        target_cell = self.get_cell_content(player_x + x_diff, player_y + y_diff)
        invalid_cells = [self.Icons.WALL, self.Icons.BOX, self.Icons.BOX_ON_GOAL]

        return target_cell not in invalid_cells

    # private
    def _next(self, x: int, y: int) -> Icons:
        player_x, player_y = self.player

        return self.get_cell_content(player_x + x, player_y + y)

    def can_push(self, dir: Direction) -> bool:
        (x, y) = dir.value

        player_is_adjacent_to_box = self._next(x, y) in [
            self.Icons.BOX,
            self.Icons.BOX_ON_GOAL,
        ]
        box_can_be_pushed = self._next(x + x, y + y) in [
            self.Icons.FLOOR,
            self.Icons.GOAL,
        ]

        return player_is_adjacent_to_box and box_can_be_pushed

    def move_player(self, dir: Direction):
        (x, y) = dir.value
        if self.can_move(dir):
            player_x, player_y = self.player
            target_cell = self._next(x, y)

            new_player_cell = (
                self.Icons.FLOOR
                if (player_x, player_y) not in self.goals
                else self.Icons.GOAL
            )

            new_target_cell = (
                self.Icons.PLAYER
                if target_cell == self.Icons.FLOOR
                else self.Icons.PLAYER_ON_GOAL
            )
            self.player=(player_x+x,player_y+y)
            self.set_cell_content(player_x, player_y, new_player_cell)
            self.set_cell_content(player_x + x, player_y + y, new_target_cell)

        elif self.can_push(dir):
            player_x, player_y = self.player
            target_cell = self._next(x, y)

            new_player_cell = (
                self.Icons.FLOOR
                if (player_x, player_y) not in self.goals
                else self.Icons.GOAL
            )

            new_target_cell = (
                self.Icons.PLAYER
                if target_cell == self.Icons.BOX
                else self.Icons.PLAYER_ON_GOAL
            )

            self._move_box(player_x + x, player_y + y, x, y)
            self.player=(player_x+x,player_y+y)
            self.set_cell_content(player_x, player_y, new_player_cell)
            self.set_cell_content(player_x + x, player_y + y, new_target_cell)

class NodeSokoban:
    def __init__(self, level_state, player, boxes, goals):
        self.level_state = level_state
        self.player = player
        self.boxes = boxes
        self.goals = goals

    def __key(self):
        hashable_matrix = tuple(tuple(row) for row in self.level_state)
        return hash(hashable_matrix)

    def __hash__(self):
        return hash(self.__key())

    def get_level_state(self):
        return self.level_state

    def get_player(self):
        return self.player

    def get_boxes(self):
        return self.boxes

    def get_goals(self):
        return self.goals

    def __str__(self):
        string = ""
        for row in self.level_state:
            for char in row:
                string += char.value
            string += '\n'
        return string

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.level_state == other.level_state

    def manhattan(self):
        x, y = self.player

        playerToBoxes = 0;

        for  e in self.boxes:
            bx, by = e
            playerToBoxes += abs(x - bx) + abs(y - by)

        boxesToStorages = 0

        for e in self.goals:
            ex, ey = e

            minDistance = 0

            for m in self.boxes:
                mx, my = m
                distance = abs(ex - mx) + abs(ey - my)
                minDistance = min(minDistance, distance)

            boxesToStorages += minDistance

        return playerToBoxes+boxesToStorages
