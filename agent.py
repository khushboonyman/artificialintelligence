"""
Created on Wed Apr 15 21:55:26 2020
@author :
"""

import location
from state import *
#import state  #contains global variables
import sys
from queue import PriorityQueue

def TranslateToDir(locfrom, locto):        
    if locfrom.x == locto.x:
        if locto.y == locfrom.y - 1:
            return 'W'
        else:
            return 'E'
    else:
        if locto.x == locfrom.x - 1:
            return 'N'
        else:
            return 'S'
           
class Agent:
    def __init__(self, location, color, number, plan=[]):
        self.location = location
        self.color = color
        self.number = number
        self.plan = plan
        
    def __str__(self):
        return str(self.location) + ' Color : ' + self.color + ' Letter : ' + self.number

    def __hash__(self):
        return hash(self.number)
    
    def __eq__(self, other):
        if self.number == other.number :
            return True
        return False
    
    def __ne__(self, other):
        if self.number != other.number :
            return True
        return False
    
    def __lt__(self, other):
        if self.number < other.number :
            return True
        return False
    
    def __gt__(self, other):
        if self.number > other.number :
            return True
        return False
    
    def NoOp(self) :
        return 'NoOp'
    
    def Move(self, agtto):
        if (self.location != agtto and agtto in State.FreeCells and agtto in State.Neighbours[self.location]):
            move_dir_agent = TranslateToDir(self.location, agtto)
            self.location.free_cell()
            State.FreeCells.add(self.location)
            self.location = agtto
            self.location.assign(self.number)
            State.FreeCells.remove(self.location)
            return 'Move(' + move_dir_agent + ')'
        return self.NoOp()

    def Push(self, box, boxto):
        if (self.location != boxto and box.location != boxto and boxto in State.FreeCells and self.color == box.color 
        and box.location in State.Neighbours[self.location] and boxto in State.Neighbours[box.location]):
            move_dir_agent = TranslateToDir(self.location, box.location)
            move_dir_box = TranslateToDir(box.location, boxto)
            self.location.free_cell()
            State.FreeCells.add(self.location)
            self.location = box.location
            self.location.assign(self.number)
            box.location = boxto
            box.location.assign(box.letter)
            State.FreeCells.remove(boxto)
            return 'Push(' + move_dir_agent + ',' + move_dir_box + ')'

        return self.NoOp()

    def Pull(self, agtto, box):
        if (self.location != agtto and box.location != self.location and agtto in State.FreeCells and self.color == box.color
        and agtto in State.Neighbours[self.location] and self.location in State.Neighbours[box.location]):
            move_dir_agent = TranslateToDir(self.location, agtto)
            curr_dir_box = TranslateToDir(self.location, box.location)
            box.location.free_cell()
            State.FreeCells.add(box.location)
            box.location = self.location
            box.location.assign(box.letter)
            self.location = agtto
            self.location.assign(self.number,None,self)
            State.FreeCells.remove(agtto)
            return 'Pull(' + move_dir_agent + ',' + curr_dir_box + ')'

        return self.NoOp()

    def PrepareAction(self, box, cell1, cell2, goal_loc):
        if box.location != cell1:
            return self.Move(cell1)
        else:
            if cell2 != self.location:
                return self.Push(box, cell2)
            else:
                agents_neighbours = State.Neighbours[self.location]
                small_frontier = PriorityQueue()
                for each_neighbour in agents_neighbours:
                    small_heur = -1 * (abs(each_neighbour.x - goal_loc.x) + abs(each_neighbour.y - goal_loc.y))
                    small_frontier.put((small_heur, each_neighbour))
                while not small_frontier.empty():
                    agent_to = small_frontier.get()[1]
                    action = self.Pull(agent_to, box)
                    if action != self.NoOp():
                        return action
                return self.NoOp()

    def MakePlan(self):
        letters = [letter for letter in State.color_dict[self.color]]
        min_plan_length = MAX_ROW*MAX_COL
        
        return True

    def Execute(self) :
        return 'NoOp'
    