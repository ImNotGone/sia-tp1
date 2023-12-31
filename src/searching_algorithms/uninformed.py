from typing import Tuple, List
from queue import PriorityQueue
from src.sokoban import Sokoban, NodeSokoban
from src.utils import reconstruct_path
import time


# Function to print a BFS of graph
def bfs(sokoban: Sokoban) -> Tuple[list[NodeSokoban], float, int, int]:
    start_time = time.time()

    initial_player = sokoban.get_player()
    initial_boxes = sokoban.get_boxes()

    # Create a queue for BFS with the initial level_state as the first item in the queue
    queue: List[NodeSokoban] = []
    current_node = NodeSokoban(initial_player, initial_boxes)

    queue.insert(0, current_node)
    nodes_expanded = 0

    # Create dictionary for parents so that I can reconstruct path
    parents = {}

    while queue and not sokoban.level_complete():
        # Dequeue a level_state from queue and set it in sokoban instance
        s_node = queue.pop()

        player = s_node.get_player()
        boxes = s_node.get_boxes()

        sokoban.set_state(player, boxes)

        # Get all adjacent vertices of the dequeued vertex s.
        for direction in sokoban.get_valid_directions():
            sokoban.move_player(direction)
            current_node = NodeSokoban(sokoban.get_player(), sokoban.get_boxes())

            if not sokoban.level_failed() and current_node not in parents:
                nodes_expanded += 1
                queue.insert(0, current_node)

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
    frontier_nodes = len(queue)

    return path_to_solution, elapsed_time, nodes_expanded, frontier_nodes


# Function to print a DFS of graph
def dfs(sokoban: Sokoban) -> Tuple[list[NodeSokoban], float, int, int]:
    start_time = time.time()

    initial_player = sokoban.get_player()
    initial_boxes = sokoban.get_boxes()

    # Create a set for DFS with the level state in the first item of the set
    stack = []
    current_node = NodeSokoban(initial_player, initial_boxes)
    nodes_expanded = 0
    stack.append(current_node)

    # Create the dictionary for parents so i can reconstruct path
    parents = {}

    while stack and not sokoban.level_complete():
        s_node = stack.pop()

        player = s_node.get_player()
        boxes = s_node.get_boxes()

        sokoban.set_state(player, boxes)

        # Get all adjacent vertices of the dequeued vertex s.
        for direction in sokoban.get_valid_directions():
            sokoban.move_player(direction)
            current_node = NodeSokoban(sokoban.get_player(), sokoban.get_boxes())

            if not sokoban.level_failed() and current_node not in parents:
                nodes_expanded += 1
                stack.append(current_node)
                parents[current_node] = s_node

                if sokoban.level_complete():
                    break

            sokoban.set_state(player, boxes)

    end_time = time.time()
    elapsed_time = end_time - start_time
    path_to_solution = reconstruct_path(
        parents, current_node, NodeSokoban(initial_player, initial_boxes)
    )
    frontier_nodes = len(stack)

    return path_to_solution, elapsed_time, nodes_expanded, frontier_nodes
