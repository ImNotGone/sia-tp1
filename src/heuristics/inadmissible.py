from src.sokoban import Sokoban

# Sum the manhattan distances from the player to the boxes
# Sum the manhattan distances from the boxes to the closest goal
# This heuristic is inadmissible because when a player gets close to a box
# it may also be getting close to another box
def inadmissible_manhattan_distance(sokoban: Sokoban) -> int:
    x, y = sokoban.get_player()

    playerToBoxes = 0

    for e in sokoban.get_boxes():
        bx, by = e
        playerToBoxes += abs(x - bx) + abs(y - by)

    boxesToStorages = 0

    for e in sokoban.get_goals():
        ex, ey = e

        minDistance = 0

        for m in sokoban.get_boxes():
            mx, my = m
            distance = abs(ex - mx) + abs(ey - my)
            minDistance = min(minDistance, distance)

        boxesToStorages += minDistance

    return playerToBoxes + boxesToStorages
