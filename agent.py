from location import *
from state import *    
import sys

def TranslateToDir(locfrom,locto):
    if locfrom.x == locto.x :
        if locto.y == locfrom.y-1 :
            return 'W'
        else :
            return 'E'
    else :
        if locto.x == locfrom.x-1 :
            return 'N'
        else :
            return 'S'
        
def ToServer(message):
    #remove it with sysin
    print(message)
    #add it with sysin
    #print(message, file=sys.stdout, flush=True)
                    
class Agent :
    def __init__(self,location,color,number):
        self.location = location
        self.color = color
        self.number = number
        
    def __str__(self) :
        return str(self.location)+'\nColor : '+self.color+'\nLetter : '+self.number
    
    def __hash__(self) :
        return hash(str(self))
    
    def Move(self,agtto):
        if (self.location !=agtto and agtto in CurrentState.FreeCells and self.location not in CurrentState.FreeCells and 
        agtto in CurrentState.Neighbours[self.location]) :
            
            move_dir_agent = TranslateToDir(self.location,agtto)
            self.location.free_cell()
            CurrentState.FreeCells.append(self.location)
            self.location = agtto
            self.location.assign(self.number)
            CurrentState.FreeCells.remove(self.location)
            return 'Move('+move_dir_agent+')'
        
        return 'NoOp'
               
    def Push(self,box,boxto):
        if (self.location !=boxto and box.location != boxto and boxto in CurrentState.FreeCells and 
        self.location not in CurrentState.FreeCells and self.color == box.color and 
        box.location in CurrentState.Neighbours[self.location] and boxto in CurrentState.Neighbours[box.location]) :
        
            move_dir_agent = TranslateToDir(self.location,box.location)
            move_dir_box = TranslateToDir(box.location,boxto)
            self.location.free_cell()
            CurrentState.FreeCells.append(self.location)
            self.location = box.location
            self.location.assign(self.number)
            box.location = boxto
            box.location.assign(box.letter)
            CurrentState.FreeCells.remove(boxto)
            return 'Push('+move_dir_agent+','+move_dir_box+')'
        
        return 'NoOp' 
    
    def Pull(self,agtto,box):
        if ( self.location != agtto and box.location != self.location and agtto in CurrentState.FreeCells and 
        box.location not in CurrentState.FreeCells and self.color == box.color and 
        agtto in CurrentState.Neighbours[self.location] and self.location in CurrentState.Neighbours[box.location]) : 
            
            move_dir_agent = TranslateToDir(self.location,agtto)
            curr_dir_box = TranslateToDir(self.location,box.location)
            box.location.free_cell()
            CurrentState.FreeCells.append(box.location)
            box.location = self.location
            box.location.assign(box.letter)
            self.location = agtto
            self.location.assign(self.number)
            CurrentState.FreeCells.append(agtto)
            return 'Pull('+move_dir_agent+','+curr_dir_box+')'
        
        return 'NoOp'
    
    def ExecutePlan(self,box,cells) :
        if len(cells) <= 1 :
            return
        cell = cells.pop(0)
        #print(cell,cells)
        if box.location != cell :
            ToServer(self.Move(cell))
        else :
            if cells[0] != self.location :
                ToServer(self.Push(box,cells[0]))
            else :
                nabo = CurrentState.Neighbours[self.location]
                for n in nabo :
                    action = self.Pull(nabo,box)
                    if action != 'NoOp' :
                        break
            
        self.ExecutePlan(box,cells)
        
    
    
    
                
            
        
            
            
            
        
        
    