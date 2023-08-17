from collections import defaultdict
from sokoban import Sokoban
import copy
from sokoban import NodeSokoban
import time

class DFS:
    # Constructor
    def __init__(self):
        # Default dictionary to store graph
        self.graph = defaultdict(list)

    # Function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # Function to print a DFS of graph
    def dfs(self, lvl: int):
        start_time = time.time()
        level= lvl
        levels_file= "levels.txt"
        sokoban = Sokoban(level, levels_file)

        first_state = copy.deepcopy(sokoban.get_level_state())
        player = sokoban.get_player()
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
            player = copy.deepcopy(s_node.get_player())
            boxes = copy.deepcopy(s_node.get_boxes())
            goals = copy.deepcopy(s_node.get_goals())

            sokoban.set_status(s_level_state,player,boxes,goals)


            # Get all adjacent vertices of the dequeued vertex s.
            for direction in sokoban.get_valid_directions():
                if sokoban.can_move(direction) or sokoban.can_push(direction):
                    sokoban.move_player(direction)
                    current_node = NodeSokoban(copy.deepcopy(sokoban.get_level_state()),copy.deepcopy(sokoban.get_player()),copy.deepcopy(sokoban.get_boxes()),copy.deepcopy(sokoban.get_goals()))
                    if current_node not in parents:
                        i += 1
                        stack.append((i, current_node))
                        parents[current_node] = s_node
                        if sokoban.level_complete():
                            break
                    sokoban.set_status(s_level_state,player,boxes,goals)

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time} seconds")
        for node in reconstruct_path(parents, current_node, NodeSokoban(first_state,player,boxes,goals)):
            print(str(node))


def reconstruct_path(parents, target, start):
    path = []
    current = target
    while not current == start:
        path.append(current)
        current = parents[current]
    path.append(start)
    path.reverse()
    return path

dfs = DFS()
dfs.dfs(55)
