from collections import defaultdict
from sokoban import Sokoban
import copy
from queue import PriorityQueue
from sokoban import NodeSokoban

class BFS:

    # Constructor
    def __init__(self):
        # Default dictionary to store graph
        self.graph = defaultdict(list)

    # Function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    # Function to print a BFS of graph
    def bfs(self, lvl: int):
        level = lvl
        levels_file = "levels.txt"
        sokoban = Sokoban(level, levels_file)

        first_state = copy.deepcopy(sokoban.get_level_state())

        # Create a queue for BFS with the initial level_state as the first item in the queue
        queue = PriorityQueue()
        i = 0
        current_node = NodeSokoban(first_state)
        queue.put((i, current_node))

        # Create dictionary for parents so that I can reconstruct path
        parents = {}

        while queue and not sokoban.level_complete():
            # Dequeue a level_state from queue and set it in sokoban instance
            s_node = queue.get()[1]
            s_level_state = copy.deepcopy(s_node.get_level_state())
            sokoban.set_level_state(s_level_state)

            # Get all adjacent vertices of the dequeued vertex s.
            for direction in sokoban.get_valid_directions():
                if sokoban.can_move(direction) or sokoban.can_push(direction):
                    sokoban.move_player(direction)
                    current_node = NodeSokoban(copy.deepcopy(sokoban.get_level_state()))
                    if current_node not in parents:
                        i += 1
                        print(i)
                        queue.put((i, current_node))
                        parents[current_node] = s_node
                        if sokoban.level_complete():
                            break
                    sokoban.set_level_state(s_level_state)  # We go back to the parent state we were evaluating

        for node in reconstruct_path(parents, current_node, NodeSokoban(first_state)):
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


bfs = BFS()
bfs.bfs(2)
