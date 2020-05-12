# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 21:55:26 2020
@author :
"""

class State :

    color_dict = dict()
    current_level = list() #shows how the level looks currently
    goal_level = list() #shows how the goal level looks 
    
    GoalDependency = dict() #dictionary of dependent goal locations .. {location : set(location)}
    GoalLocations = set() #all goal locations .. {location}    
    
    Neighbours = dict() #dictionary of non-wall neighbours for each location .. {location : list(location)}
    GoalAt = dict() #Stores the locations of all goals .. {letter : list(location)}
    Plans = dict() #Dictionary containing path between two locations .. {start,end : list(location)}    
    AgentAt = list() #all agents .. list(Agent(location,color,number,plan))
    BoxAt = dict() #all non-goal reached boxes .. {letter : list(Box(location,color,letter))
    FreeCells = set() #Cells which are currently free .. {location(x,y)}
    MAX_ROW = 0 
    MAX_COL = 0
