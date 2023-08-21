from src.sokoban import Sokoban

def play(sokoban: Sokoban):
    moves = 0
    while (not sokoban.level_complete() and not sokoban.level_failed()):
        valid = False
        dir = Sokoban.Direction.NONE
        while (not valid):
            print("\033[H\033[J")
            print(sokoban)
            key = input("wasdq:")
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
                case "q":
                    return
                case _:
                    valid = False
            if (valid and sokoban.can_move(dir) or sokoban.can_push(dir)):
                sokoban.move_player(dir)
                moves += 1

    print(sokoban)
    if (sokoban.level_complete()):
        print("Level complete!")
    else:
        print("Level failed!")
    print(f"Number of moves: {moves}")
