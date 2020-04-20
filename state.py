# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 21:55:26 2020

@author: Bruger
"""
class State :
    current_state=list()
    
class CurrentState :
    AgentAt = list()
    BoxAt = list()
    FreeCells = list()
    Neighbours = {}
    
class FinalState :
    GoalAt = list()