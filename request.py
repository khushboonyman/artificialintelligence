# -*- coding: utf-8 -*-
"""
Created on Tue May 19 13:33:36 2020

@author: Bruger
"""

class Request :
    def __init__(self,blocking_box,free_these_cells) :
        self.blocking_box = blocking_box
        self.free_these_cells = free_these_cells
        
    def __eq__(self,other) :
        if self.blocking_box == other.blocking_box :
            return True
        return False    
    
    def __str__(self):
        return ' BlockedBox : ' + str(self.blocking_box) + ' Length of cells to free :  ' + str(len(self.free_these_cells)) 
    
    def __hash__(self) :
        return hash(str(self))