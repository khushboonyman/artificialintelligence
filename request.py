# -*- coding: utf-8 -*-
"""
Created on Tue May 19 13:33:36 2020

@author: Bruger
"""

class Request :
    def __init__(self,blocking_box,blocked_agent,free_these_cells) :
        self.status = status
        self.blocking_box = blocking_box
        self.blocked_agent = blocked_agent
        self.free_these_cells = free_these_cells
        
    def __eq__(self,other) :
        if self.blocking_box == other.blocking_box and self.blocked_agent == other.blocked_agent :
            return True
        return False    
    
    def __str__(self):
        return ' BlockedBox : ' + str(self.blocking_box) + ' BlockedAgent : ' + str(self.blocked_agent) + ' Length og cells to free :  ' + str(len(self.free_these_cells)) 
    
    def __hash__(self) :
        return hash(str(self))