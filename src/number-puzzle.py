from enum import Enum
import copy
from queue import PriorityQueue

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

    def getMatrix(self):
        return self._matrix

    def can_move(self, move: Move) -> bool:
        matrix = self.getMatrix()
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if(matrix[i][j] == 0):
                    j += dir[move.value][0]
                    i += dir[move.value][1]
                    return i >= 0 and i < len(matrix) and j >= 0 and j < len(matrix[0])

        raise RuntimeError("0 not found")

    def apply_move(self, move: Move):
        matrix = self.getMatrix()
        dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if(matrix[i][j] == 0):
                    k = i + dir[move.value][1]
                    l = j + dir[move.value][0]

                    if (not (k >= 0 and k < len(matrix) and l >= 0 and l < len(matrix[0]))):
                        raise Exception("Out of bounds")

                    new_mat = copy.deepcopy(matrix)
                    new_mat[i][j] = matrix[k][l]
                    new_mat[k][l] = 0
                    return Board(new_mat)

        raise RuntimeError("0 not found")

solved_board = Board([
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5],
])

start_board = Board([
    [1, 3, 0],
    [6, 2, 4],
    [8, 7, 5],
])

start_board = Board([
    [6, 1, 4],
    [8, 3, 2],
    [0, 7, 5],
])

class Node:
    def __init__(self, board: Board, parent = None):
        self._board = board
        self.parent = parent
        self.children = []

    def getBoard(self) -> Board:
        return self._board

    def calculate_distance(self, i, j):
        for k in range(len(solved_board.getMatrix())):
            for l in range(len(solved_board.getMatrix()[0])):
                if(solved_board.getMatrix()[k][l] == self._board.getMatrix()[i][j]):
                    return abs(i - k) + abs(l - j)
        raise Exception("value not found")

    def manhattan(self):
        value = 0
        for i in range(len(self._board.getMatrix())):
            for j in range(len(self._board.getMatrix()[0])):
                if(self._board.getMatrix()[i][j] != solved_board.getMatrix()[i][j] and self._board.getMatrix()[i][j] != 0):
                    value += self.calculate_distance(i, j)
        return value

    def h2(self):
        sum = 0
        for i in range(len(self._board.getMatrix())):
            for j in range(len(self._board.getMatrix()[0])):
                if(self._board.getMatrix()[i][j] != solved_board.getMatrix()[i][j] and self._board.getMatrix()[i][j] != 0):
                    sum += 1
        return sum

    def __lt__(self, other):
        return self.manhattan() < other.manhattan()


def printMat(mat):
    for row in mat:
        print(row)

def show_path(node: Node):
    if(node.parent is None):
        printMat(node.getBoard().getMatrix())
        return
    show_path(node.parent)
    print()
    printMat(node.getBoard().getMatrix())

seen = set()

#start_board = Board([
#    [1, 2, 3],
#    [8, 4, 5],
#    [7, 0, 6],
#])

root = Node(start_board)

queue = PriorityQueue()
queue.put(root)
i = 1
found = False
while(not queue.empty()):
    current_node = queue.get()
    # printMat(current_node.getBoard().getMatrix())
    current_node_board = current_node.getBoard()
    for move in Move:
        if(current_node_board.can_move(move)):
            board = current_node_board.apply_move(move)
            new_node = Node(board, current_node)
            if(board.getMatrix() == solved_board.getMatrix()):
                found = True
                show_path(new_node)
                print(i, "nodes expanded")
                exit(0)
            current_node.children.append(new_node)
            if(board._numeric_board not in seen):
                i += 1
                queue.put(new_node)
            seen.add(board._numeric_board)
        current_node.children.append(None)
