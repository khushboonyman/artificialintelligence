from state import *

class Location :
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    
    def __eq__(self,other) :
        if self.x == other.x and self.y == other.y :
            return True
        else :
            return False
    
    def __le__(self,other) :
        if self.x < other.x :
            return True
        if self.y < other.y :
            return True
        return False
    
    def __ne__(self,other) :
        if self.x != other.x or self.y != other.y :
            return True
        return False
    
    def __str__(self) :
        return 'Location is : '+str(self.x)+','+str(self.y)
    
    def __hash__(self) :
        return hash(str(self))
        
    def assign(self,data):
        #we don't handle edge cases because there are walls on all these edge cells and they will never need to be modified
        State.current_state[self.x] = State.current_state[self.x][:self.y] + data + State.current_state[self.x][self.y+1:] 
    
    def free_cell(self) :
        self.assign(' ')    

    '''def neighbor(self,other):
        if ((self.x == other.x and self.y in [other.y+1,other.y-1]) 
        or (self.y == other.y and self.x in [other.x+1,other.x-1])) :
            return True
        return False
        
       def free(self):
        if State.current_state[self.x][self.y] == ' ' :
            return True
        return False 
        
        '''
        
    
    

