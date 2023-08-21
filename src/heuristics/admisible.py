import sys
from typing import Dict, Tuple
from src.sokoban import Sokoban


# Calculate the manhattan distance from the player to the closest box
# and the sum of the manhattan distances from the boxes to the closest goal
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


# Calculate the manhattan distance from the player to the closest box
# and the sum of the manhattan distances from the boxes to the closest goal
# but this time we take into account the walls because we can't move through them
# Uses dynamic programming to calculate the distances

distance_point_to_point: Dict[Tuple[Tuple[int, int], Tuple[int, int]], int] = {}


def walkable_distance(sokoban: Sokoban) -> int:
    board = sokoban.get_board()
    boxes = sokoban.get_boxes()
    goals = sokoban.get_goals()

    player_x, player_y = sokoban.get_player()

    distance_player_to_closest_box = sys.maxsize

    for box_x, box_y in boxes:
        if ((box_x, box_y), (player_x, player_y)) in distance_point_to_point:
            distance = distance_point_to_point[((box_x, box_y), (player_x, player_y))]
        else:
            distance = walkable_distance_helper(
                board, player_x, player_y, box_x, box_y
            )
            distance_point_to_point[((box_x, box_y), (player_x, player_y))] = distance
            distance_point_to_point[((player_x, player_y), (box_x, box_y))] = distance

        if distance < distance_player_to_closest_box:
            distance_player_to_closest_box = distance

    sum_distance_boxes_to_goals = 0
    for box_x, box_y in boxes:
        distance_box_to_closest_goal = sys.maxsize

        for goal_x, goal_y in goals:
            if ((box_x, box_y), (goal_x, goal_y)) in distance_point_to_point:
                distance = distance_point_to_point[((box_x, box_y), (goal_x, goal_y))]
            else:
                distance = walkable_distance_helper(
                    board, box_x, box_y, goal_x, goal_y
                )
                distance_point_to_point[((box_x, box_y), (goal_x, goal_y))] = distance
                distance_point_to_point[((goal_x, goal_y), (box_x, box_y))] = distance

            if distance < distance_box_to_closest_goal:
                distance_box_to_closest_goal = distance

        sum_distance_boxes_to_goals += distance_box_to_closest_goal

    return distance_player_to_closest_box + sum_distance_boxes_to_goals


def walkable_distance_helper(
    board: list, from_x: int, from_y: int, target_x: int, target_y: int
) -> int:
    # BFS
    queue = []
    queue.append((from_x, from_y, 0))
    visited = set()

    while queue:
        from_x, from_y, dist = queue.pop(0)
        if (from_x, from_y) in visited:
            continue
        visited.add((from_x, from_y))

        if from_x == target_x and from_y == target_y:
            return dist

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if board[from_y + dy][from_x + dx] != Sokoban.Icons.WALL:
                queue.append((from_x + dx, from_y + dy, dist + 1))

    return sys.maxsize
