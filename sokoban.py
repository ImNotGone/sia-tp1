import sys
from enum import Enum

class sokoban:
    class Icons(Enum):
        WALL    = '#'
        FLOOR   = ' '
        GOAL    = '.'
        BOX     = '$'
        BOX_ON_GOAL     = '*'
        PLAYER  = '@'
        PLAYER_ON_GOAL  = '+'

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
        else: # I have to load the level to the level_state matrix
            file= open(levels_file, 'r')
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
                            if c != '\n' and self.is_valid_value(c):
                                row.append(c)
                            elif c == '\n': #jump to next row when newline
                                continue
                            else:
                                print ("ERROR: Level "+str(level)+" has invalid value "+c)
                                sys.exit(1)
                        self.level_state.append(row)
                    else:
                        break


    def get_level_state(self):
        return self.level_state

    def print_level_state(self):
        for row in self.level_state:
            for char in row:
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write('\n')

    def get_cell_content(self,x,y):
        return self.matrix[y][x]

    def set_cell_content(self,x,y,content):
        if self.is_valid_value(content):
            self.matrix[y][x] = content
        else:
            print("ERROR: Value " + content + " is not valid to be added")


    def player(self): #sets player to his acording starting cell depending on the level
        x = 0
        y = 0
        for row in self.matrix:
            for pos in row:
                if pos == self.Icons.PLAYER or pos == self.Icons.PLAYER_ON_GOAL:
                    return (x, y, pos)
                else:
                    x = x + 1
            y = y + 1
            x = 0

    def level_complete(self):
        for row in self.matrix:
            for cell in row:
                if cell == self.Icons.BOX:
                    return False
        return True

    def move_box(self,x,y,a,b): #x and y is the position of the box while a and b are the posible movements of the box
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


    def can_move(self,x,y):
        return self.get_cell_content(self.player()[0]+x,self.player()[1]+y) not in [self.Icons.WALL,self.Icons.BOX_ON_GOAL,self.Icons.BOX]

    def next(self,x,y):
        return self.get_cell_content(self.player()[0]+x,self.player()[1]+y)

    def can_push(self,x,y):
        return (self.next(x,y) in [self.Icons.BOX_ON_GOAL,self.Icons.BOX] and self.next(x+x,y+y) in [self.Icons.FLOOR,self.Icons.GOAL])

    def move_player(self,x,y):
        if self.can_move(x,y):
            current=self.player()
            next=self.next(x,y)
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
        elif self.can_push(x,y):
            current=self.player()
            next=self.next(x,y)
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






