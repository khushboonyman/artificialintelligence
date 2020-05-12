# -*- coding: utf-8 -*-
"""
Created on Sat May  2 20:28:35 2020

@author: Bruger
"""
from agent import *
from planningClient import *
#import state

def CheckConflict(current_plan) :
    num_of_conflicts = {}
    conflicts = list()
    conflict_flag = False
    agent_in_conflict = None
    location_conflict = None
    conflict_start = None
    
    for agent1 in AgentAt :
        num_of_conflicts[agent1] = 0
        if agent1 in current_plan.keys() :
            len1 = len(current_plan[agent1][1])
            path1 = current_plan[agent1][1]
        
            for agent2 in AgentAt :
                if agent1 != agent2 and agent2 in current_plan.keys()  :
                    num_of_conflicts[agent2] = 0
                    len2 = len(current_plan[agent2][1])
                    small_path = len1 if len1 < len2 else len2 
                    path2 = current_plan[agent2][1]
                    for i in range(small_path-1) :
                        if path1[i] == path2[i] or path1[i] == path2[i+1]:
                            conflict_flag = True
                            num_of_conflicts[agent1]+=1
                            num_of_conflicts[agent2]+=1
                            conflicts.append((agent1,agent2,path1[i]))
    
    if conflict_flag :
        max_conflict = 0
        for key,value in num_of_conflicts.items() :
            if value > max_conflict :
                max_conflict = value
                agent_in_conflict = key
    
        for c in conflicts :
            if c[0] == agent_in_conflict or c[1] == agent_in_conflict :
                location_conflict = c[2]
                second_agent = c[0] if c[1] == agent_in_conflict else c[1] 
                
        for loc in current_plan[agent_in_conflict][1] :
            if loc in current_plan[second_agent][1] and conflict_start is None :
                conflict_start = loc
                break
                            
    return agent_in_conflict,location_conflict,conflict_start
                        
