from collections import defaultdict
from typing import Tuple
from src.sokoban import Sokoban, NodeSokoban
from src.utils import reconstruct_path
import copy
import time


# Function to print a DFS of graph
def dfs(sokoban: Sokoban) -> Tuple[list[NodeSokoban], float]:
    start_time = time.time()
    """ level= lvl """
    """ levels_file= "levels.txt" """
    """ sokoban = Sokoban(level, levels_file) """

    first_state = copy.deepcopy(sokoban.get_level_state())
    player = sokoban.get_play()
    boxes = copy.deepcopy(sokoban.get_boxes())
    goals = copy.deepcopy(sokoban.get_goals())

    # Create a set for DFS with the level state in the first item of the set
    stack = []
    i=0
    current_node = NodeSokoban(first_state, player,boxes,goals)
    stack.append((i, current_node))

    #Create the dictionary for parents so i can reconstruct path
    parents = {}

    while stack and not sokoban.level_complete():

        s_node= stack.pop()[1]
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
                    print(i)
                    stack.append((i, current_node))
                    parents[current_node] = s_node
                    if sokoban.level_complete():
                        break
                sokoban.set_status(s_level_state,player,boxes,goals)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    path_to_solution = reconstruct_path(parents, current_node, NodeSokoban(first_state,player,boxes,goals))
    """ print(f"Elapsed time: {elapsed_time} seconds") """
    """ for node in reconstruct_path(parents, current_node, NodeSokoban(first_state,player,boxes,goals)): """
    """     print(str(node)) """
    return path_to_solution, elapsed_time