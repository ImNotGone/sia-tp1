from collections import defaultdict
from typing import Tuple
from queue import PriorityQueue
from src.sokoban import Sokoban, NodeSokoban
from src.utils import reconstruct_path
import copy
import time

# Function to print a BFS of graph
def bfs(sokoban: Sokoban) -> Tuple[list[NodeSokoban], float]:
    start_time = time.time()


    first_state = copy.deepcopy(sokoban.get_level_state())
    player = sokoban.get_play()
    boxes = copy.deepcopy(sokoban.get_boxes())
    goals = copy.deepcopy(sokoban.get_goals())

    # Create a queue for BFS with the initial level_state as the first item in the queue
    queue = PriorityQueue()
    i = 0
    current_node = NodeSokoban(first_state,player,boxes,goals)
    queue.put((i, current_node))

    # Create dictionary for parents so that I can reconstruct path
    parents = {}

    while queue and not sokoban.level_complete():
        # Dequeue a level_state from queue and set it in sokoban instance
        s_node = queue.get()[1]
        s_level_state = copy.deepcopy(s_node.get_level_state())
        player = copy.deepcopy(s_node.get_play())
        boxes = copy.deepcopy(s_node.get_boxes())
        goals = copy.deepcopy(s_node.get_goals())
        
        sokoban.set_status(s_level_state,player,boxes,goals)
        # Get all adjacent vertices of the dequeued vertex s.
        for direction in sokoban.get_valid_directions():
            if sokoban.can_move(direction) or sokoban.can_push(direction):
                sokoban.move_player(direction)
                current_node = NodeSokoban(copy.deepcopy(sokoban.get_level_state()),copy.deepcopy(sokoban.get_play()),copy.deepcopy(sokoban.get_boxes()),copy.deepcopy(sokoban.get_goals()))
                if current_node not in parents:
                    i += 1
                    #print(i)
                    queue.put((i, current_node))
                    parents[current_node] = s_node
                    if sokoban.level_complete():
                        break
                sokoban.set_status(s_level_state,player,boxes,goals)  # We go back to the parent state we were evaluating
                


    end_time = time.time()
    elapsed_time = end_time - start_time
    path_to_solution = reconstruct_path(parents, current_node, NodeSokoban(first_state,player,boxes,goals))

    return path_to_solution, elapsed_time
