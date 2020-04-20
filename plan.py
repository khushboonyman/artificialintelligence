# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 10:43:22 2020

@author: Bruger
"""
from queue import PriorityQueue
from state import *
import sys

def printplan(plan):
    for i in plan :
        print(i)
        
class Plan() :
    def __init__(self,start,end) :
        self.start = start
        self.end = end
        self.frontier_set = {self.start}
        self.plan = []
    
    def __str__(self) :
        return ('Start location  : ' + str(self.start)+
             '\nEnd location : '+str(self.end)+
             '\nFrontier      : '+str(self.frontier_set))
    
    def Heuristic(self,location) :
        return abs(self.end.x - location.x) + abs(self.end.y - location.y)
    
    def CreatePlan(self,loc) :
        if loc == self.end :
            return True
        
        leaves = CurrentState.Neighbours[loc]
        frontier = PriorityQueue()
        
        for leaf in leaves :
            if leaf not in self.frontier_set :
                try :
                    heur = self.Heuristic(leaf)
                    frontier.put((heur,leaf))
                    self.frontier_set.add(leaf)
                except Exception as ex:
                    print('error for '+str(heur)+' leaf '+str(leaf)+' neighbours of '+str(loc))
                    sys.exit(1)
        
        
        if frontier.empty() :
            return False
        else :
            while not frontier.empty() :
                leaf = frontier.get()[1]
                if self.CreatePlan(leaf) :
                    self.plan.append(leaf)
                    return True
        
            
            
        
        
        