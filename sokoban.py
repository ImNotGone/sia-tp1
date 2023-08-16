import sys
from typing import Tuple
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
                if line.strip() != "":
                    row = []
                    for c in line:
                        if c == "\n":
                            continue

                        if not self.is_valid_value(c):
                            print(
                                "ERROR: Level " + str(level) + " has invalid value " + c
                            )
                            sys.exit(1)

                        row.append(self.Icons(c))

                    self.level_state.append(row)
                else:
                    break

    def get_level_state(self):
        return self.level_state

    def set_level_state(self, new_level_state):
        self.level_state = copy.deepcopy(new_level_state)

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

    def player(
        self,
    ) -> Tuple[
        int, int, Icons
    ]:  # sets player to his acording starting cell depending on the level
        for y, row in enumerate(self.level_state):
            for x, cell in enumerate(row):
                if cell == self.Icons.PLAYER or cell == self.Icons.PLAYER_ON_GOAL:
                    return (x, y, cell)

        raise RuntimeError("Player not found")

    def level_complete(self) -> bool:
        for row in self.level_state:
            for cell in row:
                if cell == self.Icons.BOX:
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

        self.set_cell_content(x, y, new_box_cell)
        self.set_cell_content(x + x_diff, y + y_diff, new_target_cell)

    def can_move(self, direction: Direction) -> bool:
        player_x, player_y, _ = self.player()
        x_diff, y_diff = direction.value

        target_cell = self.get_cell_content(player_x + x_diff, player_y + y_diff)
        invalid_cells = [self.Icons.WALL, self.Icons.BOX, self.Icons.BOX_ON_GOAL]

        return target_cell not in invalid_cells

    def next(self, x: int, y: int) -> Icons:
        player_x, player_y, _ = self.player()

        return self.get_cell_content(player_x + x, player_y + y)

    def can_push(self, dir: Direction) -> bool:
        (x, y) = dir.value

        player_is_adjacent_to_box = self.next(x, y) in [
            self.Icons.BOX,
            self.Icons.BOX_ON_GOAL,
        ]
        box_can_be_pushed = self.next(x + x, y + y) in [
            self.Icons.FLOOR,
            self.Icons.GOAL,
        ]

        return player_is_adjacent_to_box and box_can_be_pushed

    def move_player(self, dir: Direction):
        (x, y) = dir.value
        if self.can_move(dir):
            player_x, player_y, player_cell = self.player()
            target_cell = self.next(x, y)

            new_player_cell = (
                self.Icons.FLOOR
                if player_cell == self.Icons.PLAYER
                else self.Icons.GOAL
            )

            new_target_cell = (
                self.Icons.PLAYER
                if target_cell == self.Icons.FLOOR
                else self.Icons.PLAYER_ON_GOAL
            )

            self.set_cell_content(player_x, player_y, new_player_cell)
            self.set_cell_content(player_x + x, player_y + y, new_target_cell)

        elif self.can_push(dir):
            player_x, player_y, player_cell = self.player()
            target_cell = self.next(x, y)

            new_player_cell = (
                self.Icons.FLOOR
                if player_cell == self.Icons.PLAYER
                else self.Icons.GOAL
            )

            new_target_cell = (
                self.Icons.PLAYER
                if target_cell == self.Icons.BOX
                else self.Icons.PLAYER_ON_GOAL
            )

            self._move_box(player_x + x, player_y + y, x, y)

            self.set_cell_content(player_x, player_y, new_player_cell)
            self.set_cell_content(player_x + x, player_y + y, new_target_cell)

class NodeSokoban:
    def __init__(self, level_state):
        self.level_state = level_state

    def __key(self):
        hashable_matrix = tuple(tuple(row) for row in self.level_state)
        return hash(hashable_matrix)

    def __hash__(self):
        return hash(self.__key())

    def get_level_state(self):
        return self.level_state

    def __str__(self):
        string = ""
        for row in self.level_state:
            for char in row:
                string += char.value
            string += '\n'
        return string

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.level_state == other.level_state:
            return True
        else:
            return False



def play():
    level = 10
    levels_file = "levels.txt"
    sokoban = Sokoban(level, levels_file)

    while (not sokoban.level_complete()):
        valid = False
        dir = Sokoban.Direction.NONE
        while (not valid):
            sokoban.print_level_state()
            key = input("wasd:")
            valid = True
            match key:
                case "w":
                    dir = Sokoban.Direction.UP
                case "a":
                    dir = Sokoban.Direction.LEFT
                case "s":
                    dir = Sokoban.Direction.DOWN
                case "d":
                    dir = Sokoban.Direction.RIGHT
                case _:
                    valid = False
            if (valid and sokoban.can_move(dir) or sokoban.can_push(dir)):
                sokoban.move_player(dir)

# play()
