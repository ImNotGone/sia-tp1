import sys
from src.sokoban import Sokoban

def admissible_manhattan_distance(sokoban: Sokoban) -> int:
    player_x, player_y = sokoban.get_player()

    distance_player_to_closest_box = sys.maxsize

    for box_x, box_y in sokoban.get_boxes():
        distance = abs(player_x - box_x) + abs(player_y - box_y)
        if distance < distance_player_to_closest_box:
            distance_player_to_closest_box = distance

    sum_distance_boxes_to_goals = 0

    for box_x, box_y in sokoban.get_boxes():
        distance_box_to_closest_goal = sys.maxsize

        for goal_x, goal_y in sokoban.get_goals():
            distance = abs(box_x - goal_x) + abs(box_y - goal_y)
            if distance < distance_box_to_closest_goal:
                distance_box_to_closest_goal = distance

        sum_distance_boxes_to_goals += distance_box_to_closest_goal

    return distance_player_to_closest_box + sum_distance_boxes_to_goals

# Same idea but we take into account the walls
def manhattan_distance_with_walls(sokoban: Sokoban) -> int:
    board = sokoban.get_board()
    boxes = sokoban.get_boxes()
    goals = sokoban.get_goals()

    player_x, player_y = sokoban.get_player()

    distance_player_to_closest_box = sys.maxsize

    ## BFS 
    queue = []
    queue.append((player_x, player_y, 0))
    visited = set()
    while queue:
        x, y, dist = queue.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if (x, y) in boxes:
            distance_player_to_closest_box = dist
            break
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if board[y + dy][x + dx] != Sokoban.Icons.WALL:
                queue.append((x + dx, y + dy, dist + 1))

    sum_distance_boxes_to_goals = 0
    for box_x, box_y in boxes:
        distance_box_to_closest_goal = sys.maxsize

        ## BFS
        queue = []
        queue.append((box_x, box_y, 0))
        visited = set()
        while queue:
            x, y, dist = queue.pop(0)
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if (x, y) in goals:
                distance_box_to_closest_goal = dist
                break
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if board[y + dy][x + dx] != Sokoban.Icons.WALL:
                    queue.append((x + dx, y + dy, dist + 1))

        sum_distance_boxes_to_goals += distance_box_to_closest_goal

    return distance_player_to_closest_box + sum_distance_boxes_to_goals
