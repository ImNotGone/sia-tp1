from src.sokoban import Sokoban

def play(sokoban: Sokoban):
    while (not sokoban.level_complete()):
        valid = False
        dir = Sokoban.Direction.NONE
        while (not valid):
            sokoban.print_level_state()
            key = input("wasdq:")
            valid = True
            if key == "w":
                dir = Sokoban.Direction.UP
            elif key == "a":
                dir = Sokoban.Direction.LEFT
            elif key == "s":
                dir = Sokoban.Direction.DOWN
            elif key == "d":
                dir = Sokoban.Direction.RIGHT
            elif key == "q":
                return
            else:
                valid = False
            if (valid and sokoban.can_move(dir) or sokoban.can_push(dir)):
                sokoban.move_player(dir)
