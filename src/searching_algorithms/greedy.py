from typing import Tuple, List
from heapq import heappop, heappush
from src.sokoban import Sokoban, NodeSokoban
from src.utils import reconstruct_path
import time


def greedy(sokoban: Sokoban) -> Tuple[list[NodeSokoban], float]:
    start_time = time.time()

    initial_player = sokoban.get_player()
    initial_boxes = sokoban.get_boxes()

    # Create a queue for BFS with the initial level_state as the first item in the queue
    queue: List[Tuple[int, int, NodeSokoban]] = []

    iterations = 0

    current_node = NodeSokoban(initial_player, initial_boxes)
    heappush(
        queue, (current_node.manhattan(sokoban.get_goals()), iterations, current_node)
    )

    # Create dictionary for parents so that I can reconstruct path
    parents = {}

    while queue and not sokoban.level_complete():
        # Dequeue a level_state from queue and set it in sokoban instance
        _, _, s_node = heappop(queue)

        player = s_node.get_player()
        boxes = s_node.get_boxes()

        sokoban.set_state(player, boxes)

        # Get all adjacent vertices of the dequeued vertex s.
        for direction in sokoban.get_valid_directions():
            sokoban.move_player(direction)
            current_node = NodeSokoban(sokoban.get_player(), sokoban.get_boxes())

            if not sokoban.level_failed() and current_node not in parents:
                iterations += 1

                heappush(
                    queue,
                    (
                        current_node.manhattan(sokoban.get_goals()),
                        iterations,
                        current_node,
                    ),
                )

                parents[current_node] = s_node
                if sokoban.level_complete():
                    break

            # We go back to the parent state we were evaluating
            sokoban.set_state(player, boxes)

    end_time = time.time()
    elapsed_time = end_time - start_time
    path_to_solution = reconstruct_path(
        parents, current_node, NodeSokoban(initial_player, initial_boxes)
    )

    return path_to_solution, elapsed_time
