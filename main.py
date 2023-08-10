from enum import Enum

class Move(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

class Board:
    def __init__(self, matrix):
        self._matrix = matrix
        num = 0
        for row in matrix:
            for col in row:
                num += col
                num *= 10
        self._numeric_board = num

#    def __hash__(self) -> int:
#        return self._numeric_board

    def getMatrix(self):
        return self._matrix

    def can_move(self, move: Move) -> bool:
        matix = self.getMatrix()
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for i in range(len(matix)):
            for j in range(len(matix[0])):
                if(matix[i][j] == 0):
                    j += dir[move.value][0]
                    i += dir[move.value][1]
                    return i >= 0 and i < len(matix) and j >= 0 and j < len(matix[0])

        raise UnboundLocalError

    def apply_move(self, move: Move):
        matix = self.getMatrix()
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for i in range(len(matix)):
            for j in range(len(matix[0])):
                if(matix[i][j] == 0):
                    k = j + dir[move.value][0]
                    l = i + dir[move.value][1]
                    new_mat = matix[:] # generate a copy
                    new_mat[i][j] = matix[k][l]
                    new_mat[k][l] = 0
                    return Board(new_mat)

        raise UnboundLocalError

class Node:
    def __init__(self, board: Board, parent = None):
        self._board = board
        self.parent = parent
        self.children = []

    def getBoard(self) -> Board:
        return self._board

#    def __hash__(self) -> int:
#        return self._board.__hash__()

def show_path(node: Node):
    if(node.parent == None):
        print(node.getBoard().getMatrix())
        return
    show_path(node.parent)
    print(node.getBoard().getMatrix())

# dict of nodes
nodes = {}

solved_board = Board([
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5],
])

start_board = Board([
    [5, 7, 3],
    [8, 2, 0],
    [7, 6, 5],
])

start_board = Board([
    [1, 2, 3],
    [8, 4, 0],
    [7, 6, 5],
])

root = Node(start_board)

queue = [root]
found = False
while(len(queue) != 0):
    current_node = queue.pop()
    current_node_board = current_node.getBoard()
    for move in Move:
        if(current_node_board.can_move(move)):
            board = current_node_board.apply_move(move)
            new_node = Node(board, current_node)
            if(board.getMatrix() == solved_board.getMatrix()):
                found = True
                show_path(new_node)
                exit(0)
            current_node.children.append(new_node)
            queue.append(new_node)
        current_node.children.append(None)

