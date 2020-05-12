"""
Created on Wed Apr 15 21:55:26 2020
@author :
"""

import location

class Box:
    def __init__(self, location, color, letter):
        self.location = location
        self.color = color
        self.letter = letter

    def __str__(self):
        return str(self.location) + ' Color : ' + self.color + ' Letter : ' + self.letter

    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        if self.location == other.location and self.letter == other.letter and self.color == other.color:
            return True
        else:
            return False

    def __lt__(self, other):
        free_self = 0
        for n in State.Neighbours[self.location] :
            if n in State.FreeCells :
                free_self+=1
            else :
                for a in State.AgentAt :
                    if n == a.location and a.color == self.color :
                        free_self+=1
        
        free_other = 0
        for n in State.Neighbours[other.location] :
            if n in State.FreeCells :
                free_other+=1
            else :
                for a in State.AgentAt :
                    if n == a.location and a.color == other.color :
                        free_other+=1
                
        if free_self <= free_other :
            return True
        return False
    
        
    def __gt__(self, other):
        free_self = 0
        for n in State.Neighbours[self.location] :
            if n in State.FreeCells :
                free_self+=1
            else :
                for a in State.AgentAt :
                    if n == a.location and a.color == self.color :
                        free_self+=1
        
        free_other = 0
        for n in State.Neighbours[other.location] :
            if n in State.FreeCells :
                free_other+=1
            else :
                for a in State.AgentAt :
                    if n == a.location and a.color == other.color :
                        free_other+=1
                
        if free_self > free_other :
            return True
        return False
    
        
    def __ne__(self, other):
        if self.location != other.location or self.letter != other.letter or self.color != other.color:
            return True
        else:
            return False
