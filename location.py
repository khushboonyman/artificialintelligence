"""
Created on Wed Apr 15 21:55:26 2020
@author :
"""
from state import *
from queue import PriorityQueue

class Location:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __lt__(self, other):
        if self in State.FreeCells and other not in State.FreeCells :
            return True
        if self not in State.FreeCells and other in State.FreeCells :
            return False
        if len(State.Neighbours[self]) < len(State.Neighbours[other]) :
            return False
        
        return True

    def __gt__(self, other):
        if self in State.FreeCells and other not in State.FreeCells :
            return False
        if self not in State.FreeCells and other in State.FreeCells :
            return True
        if len(State.Neighbours[self]) < len(State.Neighbours[other]) :
            return True
        
        return False
    
    def __ne__(self, other):
        if self.x != other.x or self.y != other.y:
            return True
        return False

    def __str__(self):
        return 'Loc: ' + str(self.x) + ',' + str(self.y)

    def __hash__(self):
        return hash(str(self))

    def assign(self, data):        
        State.current_level[self.x] = State.current_level[self.x][:self.y] + data + State.current_level[self.x][self.y + 1:]        

    def free_cell(self):
        self.assign(' ')

