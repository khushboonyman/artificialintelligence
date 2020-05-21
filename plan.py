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
        self.cost = ()

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
        
    def CreatePath(self,came_from) :
        current = self.end
        self.plan = deque()
        while current != self.start:
            self.plan.append(current)
            if current in came_from.keys() :
                current = came_from[current]
            else :
                self.plan = deque()
                return    
        
    #while finding a plan, relax the preconditions .. make A* instead .. 
    def CreateBeliefPlan(self):
        frontier = PriorityQueue()
        frontier.put((0,self.start))
        came_from = {}
        cost_so_far = {}
        came_from[self.start] = None
        cost_so_far[self.start] = 0
        
        while not frontier.empty():
            current = frontier.get()[1]        
            if current == self.end:
                break        
            for n in State.Neighbours[current]:
                new_cost = cost_so_far[current] + 1
                if n not in cost_so_far or new_cost < cost_so_far[n]:
                    cost_so_far[n] = new_cost
                    priority = new_cost + self.Heuristic(n)
                    frontier.put((priority,n))
                    came_from[n] = current
        
        self.CreatePath(came_from)

    #while finding a plan, relax the preconditions .. make A* instead .. 
    def CreateIntentionPlan(self,agent_location):
        frontier = PriorityQueue()
        frontier.put((0,self.start))
        came_from = {}
        cost_so_far = {}
        came_from[self.start] = None
        cost_so_far[self.start] = 0
        
        while not frontier.empty():
            current = frontier.get()[1]        
            if current == self.end:
                break        
            for n in State.Neighbours[current]:
                if n in State.FreeCells or n == self.end or n == agent_location :
                    new_cost = cost_so_far[current] + 1
                    if n not in cost_so_far or new_cost < cost_so_far[n] :                        
                        cost_so_far[n] = new_cost 
                        priority = new_cost + self.Heuristic(n)
                        frontier.put((priority,n))
                        came_from[n] = current
    
        self.CreatePath(came_from)
#planning a request
    def CreateAlternativeIntentionPlan(self,valid_locations) :
        frontier = PriorityQueue()
        frontier.put((0,self.start))
        came_from = {}
        cost_so_far = {}
        came_from[self.start] = None
        cost_so_far[self.start] = 0
        
        while not frontier.empty():
            current = frontier.get()[1]        
            if current == self.end:
                break        
            for n in State.Neighbours[current]:
                if n in State.FreeCells or n == self.end or n in valid_locations :
                    new_cost = cost_so_far[current] + 1
                    if n not in cost_so_far or new_cost < cost_so_far[n] : 
                        cost_so_far[n] = new_cost
                        priority = new_cost + self.Heuristic(n)
                        frontier.put((priority,n))
                        came_from[n] = current
    
        self.CreatePath(came_from) 
    

