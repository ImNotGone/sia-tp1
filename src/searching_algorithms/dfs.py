from typing import Tuple
from src.sokoban import Sokoban, NodeSokoban
from src.utils import reconstruct_path
import time


# Function to print a DFS of graph
def dfs(sokoban: Sokoban) -> Tuple[list[NodeSokoban], float]:
    start_time = time.time()

    initial_player = sokoban.get_player()
    initial_boxes = sokoban.get_boxes()

    # Create a set for DFS with the level state in the first item of the set
    stack = []
    current_node = NodeSokoban(initial_player, initial_boxes)
    stack.append(current_node)

    # Create the dictionary for parents so i can reconstruct path
    parents = {}

    while stack and not sokoban.level_complete():
        s_node = stack.pop()

        player = s_node.get_player()
        boxes = s_node.get_boxes()

        sokoban.set_status(player, boxes)

        # Get all adjacent vertices of the dequeued vertex s.
        for direction in sokoban.get_valid_directions():
            sokoban.move_player(direction)
            current_node = NodeSokoban(sokoban.get_player(), sokoban.get_boxes())

            if not sokoban.level_failed() and current_node not in parents:
                stack.append(current_node)
                parents[current_node] = s_node

                if sokoban.level_complete():
                    break

            sokoban.set_status(player, boxes)

    end_time = time.time()
    elapsed_time = end_time - start_time
    path_to_solution = reconstruct_path(
        parents, current_node, NodeSokoban(initial_player, initial_boxes)
    )

    return path_to_solution, elapsed_time
