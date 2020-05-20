# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 21:55:26 2020
@author :
"""
from collections import deque

class State :
    
    current_level = list() #shows how the level looks currently        
    GoalDependency = dict() #dictionary of dependent goal locations .. {location : set(location)}    
    DeadCells = set()
    Neighbours = dict() #dictionary of non-wall neighbours for each location .. {location : list(location)}
    Plans = dict() #set containing path between two locations .. {start,end : list(location)}    
    AgentAt = list() #all agents .. list(Agent(location,color,number,plan))
    FreeCells = set() #Cells which are currently free .. {location(x,y)}
    MAX_ROW = 0 
    MAX_COL = 0
    SingleAgent = False
    Requests = dict()
    
    color_dict = dict()
    goal_level = list() #shows how the goal level looks .. one time
    GoalLocations = set() #all goal locations .. {location}  .. one time
    GoalPaths = dict() #stores only agent to goal paths to create dependencies
    GoalAt = dict() #Stores the locations of all goals .. {letter : list(location)}
    BoxAt = dict() #all non-goal reached boxes .. {letter : list(Box(location,color,letter))
    
    @staticmethod
    def getBoxAgent(letter,location):
        blocking_box = None
        agents = list()
        for agent in State.AgentAt :
            for box in agent.boxes :
                if box.letter == letter and box.location == location :
                    if agent.move_box is not None and agent.move_box == box :
                        return list(),None
                    else :
                        blocking_box = box
                        break
        
        for agent in State.AgentAt :
            if blocking_box is not None and blocking_box in agent.boxes :
                if agent.move_box is not None and agent.move_box == box :
                    return list(),None
                else :
                    agents.append(agent)
                    
        return agents,blocking_box
    
    @staticmethod
    def getAgentAgent(number):
        for agent in State.AgentAt:
            if agent.number == number:
                return agent
        return None

    @staticmethod
    def getCellContent(location):
        return State.current_level[location.x][location.y]

    @staticmethod
    def isCellAgent(location):
        cell_content = State.getCellContent(location)
        for agent in State.AgentAt:
            if agent.number == cell_content:
                return True
        return False

    @staticmethod
    def getCellAgent(location):
        cell_content = State.getCellContent(location)
        for agent in State.AgentAt:
            if agent.number == cell_content:
                return agent
        return None

    @staticmethod
    def Bidding():
        plan_lengths = [State.MAX_COL*State.MAX_ROW]*len(State.AgentAt)
        
        for agent,requests in State.Requests.items() :
            can,reply = agent.PlanRequest(requests)
            if can :
                plan_lengths[int(agent.number)] = reply
        
        colors = set()
        unblocking_agents = set()
        
        while sum(plan_lengths) < State.MAX_COL*State.MAX_ROW*len(State.AgentAt) :
            agent_number = plan_lengths.index(min(plan_lengths))
            agent = State.AgentAt[agent_number]
            if agent.color not in colors :
                colors.add(agent.color)
                unblocking_agents.add(agent)
            else :
                agent.request_plan = deque()
                agent.request_boxes = deque()
                agent.inform_agent = None
                
            plan_lengths[agent_number] = State.MAX_COL*State.MAX_ROW
            del(State.Requests[agent])
                
                
            
                
    