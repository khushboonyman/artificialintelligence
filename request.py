# -*- coding: utf-8 -*-
"""
Created on Tue May 19 13:33:36 2020

@author: Bruger
"""

class Request :
    def __init__(self,status,blocking_box,blocked_agent,free_these_cells) :
        self.status = status
        self.blocking_box = blocking_box
        self.blocked_agent = blocked_agent
        self.free_these_cells = free_these_cells
    
    def __str__(self):
        return str(self.status) + ' BlockedBox : ' + str(self.blocking_box) + ' BlockedAgent : ' + str(self.blocked_agent) + ' Length og cells to free :  ' + str(len(self.free_these_cells)) 
    