from sokoban import Sokoban

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
            if key == "w":
                dir = Sokoban.Direction.UP
            elif key == "a":
                dir = Sokoban.Direction.LEFT
            elif key == "s":
                dir = Sokoban.Direction.DOWN
            elif key == "d":
                dir = Sokoban.Direction.RIGHT
            else:
                valid = False
            if (valid and sokoban.can_move(dir) or sokoban.can_push(dir)):
                sokoban.move_player(dir)

play()
