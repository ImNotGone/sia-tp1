from typing import Tuple
from queue import PriorityQueue
from src.sokoban import Sokoban, NodeSokoban
from src.utils import reconstruct_path
import time


# Function to print a BFS of graph
def bfs(sokoban: Sokoban) -> Tuple[list[NodeSokoban], float]:
    start_time = time.time()

    initial_player = sokoban.get_player()
    initial_boxes = sokoban.get_boxes()

    # Create a queue for BFS with the initial level_state as the first item in the queue
    queue = PriorityQueue()
    i = 0
    current_node = NodeSokoban(initial_player, initial_boxes)
    queue.put((i, current_node))

    # Create dictionary for parents so that I can reconstruct path
    parents = {}

    while queue and not sokoban.level_complete():
        # Dequeue a level_state from queue and set it in sokoban instance
        s_node = queue.get()[1]

        player = s_node.get_player()
        boxes = s_node.get_boxes()

        sokoban.set_status(player, boxes)

        # Get all adjacent vertices of the dequeued vertex s.
        for direction in sokoban.get_valid_directions():
                sokoban.move_player(direction)
                current_node = NodeSokoban(sokoban.get_player(), sokoban.get_boxes())
                if not sokoban.level_failed() and current_node not in parents:
                    i += 1

                    queue.put((i, current_node))
                    parents[current_node] = s_node
                    if sokoban.level_complete():
                        break
                sokoban.set_status(
                    player, boxes
                )  # We go back to the parent state we were evaluating

    end_time = time.time()
    elapsed_time = end_time - start_time
    path_to_solution = reconstruct_path(
        parents, current_node, NodeSokoban(initial_player, initial_boxes)
    )

    return path_to_solution, elapsed_time
