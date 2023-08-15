import sys
from enum import Enum

class Sokoban:
    class Icons(Enum):
        WALL    = '#'
        FLOOR   = ' '
        GOAL    = '.'
        BOX     = '$'
        BOX_ON_GOAL     = '*'
        PLAYER  = '@'
        PLAYER_ON_GOAL  = '+'
    
    class Direction(Enum):
        LEFT  = (-1,  0)
        RIGTH = ( 1,  0)
        UP    = ( 0, -1)
        DOWN  = ( 0,  1)
        NONE  = ( 0,  0)

    def is_valid_value(self, c):
        return (
            c == self.Icons.FLOOR   or
            c == self.Icons.WALL    or
            c == self.Icons.PLAYER  or
            c == self.Icons.GOAL    or
            c == self.Icons.BOX_ON_GOAL  or
            c == self.Icons.BOX     or
            c == self.Icons.PLAYER_ON_GOAL
        )

    def __init__(self, level, levels_file):
        self.level_state=[]

        #levels_file will have all the sokoban levels inside them and with level you choose which one to play

        if level<1:
            print("ERROR: Level " + str(level) + " does not exist")
            sys.exit(1)

        # I have to load the level to the level_state matrix
        file = open(levels_file, 'r')
        level_found = False
        for line in file:
            row = []
            if not level_found:
                if  "Level "+str(level) == line.strip():
                    level_found = True
            else:
                if line.strip() != "":
                    row = []
                    for c in line:
                        match c:
                            case '\n':
                                continue
                            case self.Icons.FLOOR.value:  
                                enum_value = self.Icons.FLOOR
                            case self.Icons.WALL.value:  
                                enum_value = self.Icons.WALL
                            case self.Icons.PLAYER.value: 
                                enum_value = self.Icons.PLAYER
                            case self.Icons.GOAL.value:
                                enum_value = self.Icons.GOAL
                            case self.Icons.BOX_ON_GOAL.value:
                                enum_value = self.Icons.BOX_ON_GOAL
                            case self.Icons.BOX.value:
                                enum_value = self.Icons.BOX
                            case self.Icons.PLAYER_ON_GOAL.value:
                                enum_value = self.Icons.PLAYER_ON_GOAL
                            case _:
                                print ("ERROR: Level "+str(level)+" has invalid value "+c)
                                sys.exit(1)
                        row.append(enum_value)

                    self.level_state.append(row)
                else:
                    break


    def get_level_state(self):
        return self.level_state

    def print_level_state(self):
        for row in self.level_state:
            for char in row:
                sys.stdout.write(char.value)
                sys.stdout.flush()
            sys.stdout.write('\n')

    def get_cell_content(self,x,y):
        return self.level_state[y][x]

    def set_cell_content(self,x,y,content):
        if self.is_valid_value(content):
            self.level_state[y][x] = content
        else:
            print("ERROR: Value " + content + " is not valid to be added")


    def player(self): #sets player to his acording starting cell depending on the level
        x = 0
        y = 0
        for row in self.level_state:
            for pos in row:
                if pos == self.Icons.PLAYER or pos == self.Icons.PLAYER_ON_GOAL:
                    return (x, y, pos)
                else:
                    x = x + 1
            y = y + 1
            x = 0
        raise RuntimeError("Player not found")

    def level_complete(self):
        for row in self.level_state:
            for cell in row:
                if cell == self.Icons.BOX:
                    return False
        return True

    # private
    def move_box(self,x,y, a, b): #x and y is the position of the box while a and b are the posible movements of the box
        box= self.get_cell_content(x,y)
        moved_box= self.get_cell_content(x+a,y+b)

        if box == self.Icons.BOX and moved_box == self.Icons.FLOOR:
            self.set_cell_content(x+a,y+b, self.Icons.BOX)
            self.set_cell_content(x,y, self.Icons.FLOOR)
        elif box == self.Icons.BOX and moved_box == self.Icons.GOAL:
            self.set_cell_content(x+a,y+b, self.Icons.BOX_ON_GOAL)
            self.set_cell_content(x,y, self.Icons.FLOOR)
        elif box == self.Icons.BOX_ON_GOAL and moved_box == self.Icons.FLOOR:
            self.set_cell_content(x+a,y+b, self.Icons.BOX)
            self.set_cell_content(x,y, self.Icons.GOAL)
        elif box == self.Icons.BOX_ON_GOAL and moved_box == self.Icons.GOAL:
            self.set_cell_content(x+a,y+b, self.Icons.BOX_ON_GOAL)
            self.set_cell_content(x,y, self.Icons.GOAL)


    def can_move(self,  dir: Direction):
        (x, y) = dir.value
        return self.get_cell_content(self.player()[0]+x,self.player()[1]+y) not in [self.Icons.WALL,self.Icons.BOX_ON_GOAL,self.Icons.BOX]

    def next(self, x, y):
        return self.get_cell_content(self.player()[0]+x,self.player()[1]+y)

    def can_push(self, dir: Direction):
        (x, y) = dir.value
        return (self.next(x,y) in [self.Icons.BOX_ON_GOAL,self.Icons.BOX] and self.next(x+x,y+y) in [self.Icons.FLOOR,self.Icons.GOAL])

    def move_player(self, dir: Direction):
        (x, y) = dir.value
        if self.can_move(dir):
            current=self.player()
            next=self.next(x, y)
            if current[2] == self.Icons.PLAYER and next == self.Icons.FLOOR:
                self.set_cell_content(current[0]+x,current[1]+y, self.Icons.PLAYER)
                self.set_cell_content(current[0],current[1], self.Icons.FLOOR)
            elif current[2] == self.Icons.PLAYER and next == self.Icons.GOAL:
                self.set_cell_content(current[0]+x,current[1]+y, self.Icons.PLAYER_ON_GOAL)
                self.set_cell_content(current[0],current[1], self.Icons.FLOOR)
            elif current[2] == self.Icons.PLAYER_ON_GOAL and next == self.Icons.FLOOR:
                self.set_cell_content(current[0]+x,current[1]+y, self.Icons.PLAYER)
                self.set_cell_content(current[0],current[1], self.Icons.GOAL)
            elif current[2] == self.Icons.PLAYER_ON_GOAL and next == self.Icons.GOAL:
                self.set_cell_content(current[0]+x,current[1]+y, self.Icons.PLAYER_ON_GOAL)
                self.set_cell_content(current[0],current[1], self.Icons.GOAL)
        elif self.can_push(dir):
            current=self.player()
            next=self.next(x, y)
            moved_box= self.next(x+x, y+y)
            if current[2] == self.Icons.PLAYER and next == self.Icons.BOX and moved_box == self.Icons.FLOOR:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_cell_content(current[0],current[1], self.Icons.FLOOR)
                self.set_cell_content(current[0]+x,current[1]+y, self.Icons.PLAYER)
            elif current[2] == self.Icons.PLAYER and next == self.Icons.BOX and moved_box == self.Icons.GOAL:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_cell_content(current[0],current[1], self.Icons.FLOOR)
                self.set_cell_content(current[0]+x,current[1]+y, self.Icons.PLAYER)
            elif current[2] == self.Icons.PLAYER and next == self.Icons.BOX_ON_GOAL and moved_box == self.Icons.FLOOR:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_cell_content(current[0],current[1], self.Icons.FLOOR)
                self.set_cell_content(current[0]+x,current[1]+y, self.Icons.PLAYER_ON_GOAL)
            elif current[2] == self.Icons.PLAYER and next == self.Icons.BOX_ON_GOAL and moved_box == self.Icons.GOAL:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_cell_content(current[0],current[1], self.Icons.FLOOR)
                self.set_cell_content(current[0]+x,current[1]+y, self.Icons.PLAYER_ON_GOAL)
            if current[2] == self.Icons.PLAYER_ON_GOAL and next == self.Icons.BOX and moved_box == self.Icons.FLOOR:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_cell_content(current[0],current[1], self.Icons.GOAL)
                self.set_cell_content(current[0]+x,current[1]+y, self.Icons.PLAYER)
            elif current[2] == self.Icons.PLAYER_ON_GOAL and next == self.Icons.BOX and moved_box == self.Icons.GOAL:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_cell_content(current[0],current[1], self.Icons.GOAL)
                self.set_cell_content(current[0]+x,current[1]+y, self.Icons.PLAYER_ON_GOAL)
            elif current[2] == self.Icons.PLAYER_ON_GOAL and next == self.Icons.BOX_ON_GOAL and moved_box == self.Icons.FLOOR:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_cell_content(current[0],current[1], self.Icons.GOAL)
                self.set_cell_content(current[0]+x,current[1]+y, self.Icons.PLAYER_ON_GOAL)
            elif current[2] == self.Icons.PLAYER_ON_GOAL and next == self.Icons.BOX_ON_GOAL and moved_box == self.Icons.GOAL:
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_cell_content(current[0],current[1], self.Icons.GOAL)
                self.set_cell_content(current[0]+x,current[1]+y, self.Icons.PLAYER_ON_GOAL)



def play():
    level = 1
    levels_file = "levels.txt"
    sokoban = Sokoban(level, levels_file)

    while(not sokoban.level_complete()):
        valid = False
        dir = Sokoban.Direction.NONE
        while(not valid):
            sokoban.print_level_state()
            key = input("wasd:")
            valid = True
            match key:
                case "w": 
                    dir = Sokoban.Direction.UP
                case "a":
                    dir = Sokoban.Direction.LEFT
                case "s":
                    dir = Sokoban.Direction.DOWN
                case "d":
                    dir = Sokoban.Direction.RIGTH
                case _:
                    valid = False
            if(valid and sokoban.can_move(dir) or sokoban.can_push(dir)):
                sokoban.move_player(dir)       


play()