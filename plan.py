# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 10:43:22 2020

@author: 
"""
from queue import PriorityQueue
from state import *
import sys
from error import *
from collections import deque
    
class Plan():
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.frontier_set = {self.start}
        self.plan = deque()

    def __eq__(self,other) :
        if self.start == other.start and self.end == other.end :
            return True
        return False
    
    def __lt__(self,other) :
        if len(self.plan) <= len(other.plan) :
            return True
        return False
    
    def __gt__(self,other) :
        if len(self.plan) > len(other.plan) :
            return True
        return False
    
    
    def __hash__(self) :
        return hash(str(self))
    
    def __str__(self):
        return ('St: ' + str(self.start) +' End : ' + str(self.end))

    def Heuristic(self, location): #we need to improve the heuristic
        return abs(self.end.x - location.x) + abs(self.end.y - location.y)

    #while finding a plan, relax the preconditions .. make A* instead .. 
    def CreateBeliefPlan(self, loc):
        if loc == self.end :
            return True        
        try :
            leaves = State.Neighbours[loc]
        except Exception as ex :
            HandleError('Plan'+str(loc)+' '+repr(ex))
            
        frontier = PriorityQueue()

        for leaf in leaves:
            if leaf not in self.frontier_set :
                try:
                    heur = self.Heuristic(leaf)
                    frontier.put((heur, leaf))
                    self.frontier_set.add(leaf)
                except Exception as ex:
                    HandleError('Plan'+str(ex) + ' ' + str(heur) + ' leaf ' + str(leaf) + ' neighbours of ' + str(loc))

        if frontier.empty():
            return False
        else:
            while not frontier.empty():
                leaf = frontier.get()[1]
                if self.CreateBeliefPlan(leaf):
                    self.plan.append(leaf)
                    return True

    #while finding a plan, take preconditions into account
    def CreateIntentionPlan(self, loc, agent_location):
        if loc == self.end:
            return True        
        try :
            leaves = State.Neighbours[loc]
        except Exception as ex :
            HandleError('Plan '+str(loc)+' '+repr(ex))
            
        frontier = PriorityQueue()

        for leaf in leaves:
            if leaf not in self.frontier_set and (leaf in State.FreeCells or leaf==self.end or leaf == agent_location) :
                try:
                    heur = self.Heuristic(leaf)
                    frontier.put((heur, leaf))
                    self.frontier_set.add(leaf)
                except Exception as ex:
                    HandleError('Plan'+str(ex) + ' ' + str(heur) + ' leaf ' + str(leaf) + ' neighbours of ' + str(loc))

        if frontier.empty():
            return False
        else:
            while not frontier.empty():
                leaf = frontier.get()[1]
                if self.CreateIntentionPlan(leaf, agent_location):
                    self.plan.append(leaf)
                    return True    

#planning a request
    def CreateAlernativeIntentionPlan(self,loc,valid_locations) :
        if loc == self.end:
            return True        
        leaves = State.Neighbours[loc]
            
        frontier = PriorityQueue()

        for leaf in leaves:
            if leaf not in self.frontier_set and (leaf in State.FreeCells or leaf==self.end or leaf in valid_locations) :
                heur = self.Heuristic(leaf)
                frontier.put((heur, leaf))
                self.frontier_set.add(leaf)

        if frontier.empty():
            return False
        else:
            while not frontier.empty():
                leaf = frontier.get()[1]
                if self.CreateAlernativeIntentionPlan(leaf,valid_locations):
                    self.plan.append(leaf)
                    return True                
    

