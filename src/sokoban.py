import sys
from enum import Enum
from typing import Tuple, Set
import copy


class Sokoban:
    class Icons(Enum):
        WALL = "#"
        FLOOR = " "
        GOAL = "."
        BOX = "$"
        BOX_ON_GOAL = "*"
        PLAYER = "@"
        PLAYER_ON_GOAL = "+"

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
            if (
                self.can_move(direction) or self.can_push(direction)
            ) and direction != self.Direction.NONE:
                valid_moves.append(direction)
        return valid_moves

    def __init__(self, level: int, levels_file: str):
        self._board = []
        self._boxes = set()
        self._goals = set()
        self._player = (0, 0)

        # levels_file will have all the sokoban levels inside them
        # level lets you choose which one to play
        if level < 1:
            print("ERROR: Level " + str(level) + " does not exist")
            sys.exit(1)

        # I have to load the level to the level_state matrix
        file = open(levels_file, "r")
        level_found = False

        x = 0
        y = 0
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
                        y += 1
                        x = 0
                        continue

                    point = (x, y)
                    match c:
                        case self.Icons.WALL.value:
                            row.append(self.Icons.WALL)
                        case self.Icons.FLOOR.value:
                            row.append(self.Icons.FLOOR)
                        case self.Icons.GOAL.value:
                            row.append(self.Icons.GOAL)
                            self._goals.add(point)
                        case self.Icons.PLAYER.value:
                            row.append(self.Icons.FLOOR)
                            self._player = point
                        case self.Icons.BOX.value:
                            row.append(self.Icons.FLOOR)
                            self._boxes.add(point)
                        case self.Icons.BOX_ON_GOAL.value:
                            row.append(self.Icons.GOAL)
                            self._boxes.add(point)
                            self._goals.add(point)
                        case self.Icons.PLAYER_ON_GOAL.value:
                            row.append(self.Icons.GOAL)
                            self._player = point
                            self._goals.add(point)
                        case _:
                            raise Exception("ERROR: Invalid value " + c)

                    x += 1
                self._board.append(row)

        if not level_found:
            raise Exception("ERROR: Level " + str(level) + " does not exist")

    def get_player(self):
        return self._player

    def get_boxes(self):
        return self._boxes

    def get_goals(self):
        return self._goals

    def set_state(self, player: Tuple[int, int], boxes: Set[Tuple[int, int]]):
        self._player = player
        self._boxes = copy.deepcopy(boxes)

    def level_complete(self) -> bool:
        for box in self._boxes:
            if box not in self._goals:
                return False
        return True

    def level_failed(self) -> bool:
        for box in self._boxes:
            if box not in self._goals:
                box_x, box_y = box

                has_adjacent_wall_y = (
                    self._board[box_y - 1][box_x] == Sokoban.Icons.WALL
                    or self._board[box_y + 1][box_x] == Sokoban.Icons.WALL
                )
                has_adjacent_wall_x = (
                    self._board[box_y][box_x - 1] == Sokoban.Icons.WALL
                    or self._board[box_y][box_x + 1] == Sokoban.Icons.WALL
                )

                if has_adjacent_wall_x and has_adjacent_wall_y:
                    return True

        return False

    # ------------------ MOVEMENT ------------------

    def can_move(self, direction: Direction) -> bool:
        player_x, player_y = self._player
        x_diff, y_diff = direction.value

        target_cell = self._board[player_y + y_diff][player_x + x_diff]
        target = (player_x + x_diff, player_y + y_diff)

        return target_cell != self.Icons.WALL and target not in self._boxes

    def can_push(self, dir: Direction) -> bool:
        player_x, player_y = self._player
        diff_x, diff_y = dir.value

        player_target = (player_x + diff_x, player_y + diff_y)
        player_is_adjacent_to_box = player_target in self._boxes

        # Check that nor x nor y are out of bounds
        box_target_x, box_target_y = player_x + 2 * diff_x, player_y + 2 * diff_y
        box_target = (box_target_x, box_target_y)

        if (
            box_target_x < 0
            or box_target_y < 0
            or box_target_y >= len(self._board)
            or box_target_x >= len(self._board[box_target_y])
        ):
            return False

        box_target_cell = self._board[box_target_y][box_target_x]
        box_can_be_pushed = (
            box_target_cell != self.Icons.WALL and box_target not in self._boxes
        )

        return player_is_adjacent_to_box and box_can_be_pushed

    def move_player(self, dir: Direction):
        player_x, player_y = self._player
        diff_x, diff_y = dir.value

        new_player_x, new_player_y = player_x + diff_x, player_y + diff_y

        if self.can_push(dir):
            box = (new_player_x, new_player_y)
            pushed_box = (new_player_x + diff_x, new_player_y + diff_y)

            self._boxes.remove(box)
            self._boxes.add(pushed_box)

        self._player = (new_player_x, new_player_y)

    # ------------------ PRINT ------------------

    def __str__(self) -> str:
        board_string = ""
        for y, row in enumerate(self._board):
            for x, cell in enumerate(row):
                char_to_add = cell.value
                if (x, y) == self._player:
                    char_to_add = (
                        self.Icons.PLAYER.value
                        if cell == self.Icons.FLOOR
                        else self.Icons.PLAYER_ON_GOAL.value
                    )
                elif (x, y) in self._boxes:
                    char_to_add = (
                        self.Icons.BOX.value
                        if cell == self.Icons.FLOOR
                        else self.Icons.BOX_ON_GOAL.value
                    )
                board_string += char_to_add

            board_string += "\n"
        return board_string



class NodeSokoban:
    def __init__(self, player: Tuple[int, int], boxes: Set[Tuple[int, int]]):
        self.player = player
        self.boxes = boxes

    def __key(self):
        return (self.player, frozenset(self.boxes))

    def __hash__(self):
        return hash(self.__key())

    def get_player(self):
        return self.player

    def get_boxes(self):
        return self.boxes

    def __str__(self):
        return "Player: " + str(self.player) + " Boxes: " + str(self.boxes) + "\n"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__key() == other.__key()
