'''
Created on Wed Apr 15 21:55:26 2020
@author :
    
change the value of global variable 'server' to True, when running using the server
When testing it with file, make it False

This will display the actions and also update current_level. At any point you can display 
current_level to see how the level looks like after any action 

'''

import argparse
from misc import memory
import re
#from box import *
#from plan import *
from state import *
import sys
from conflict import *
from setupobjects import *

x=2500
sys.setrecursionlimit(x)

def FromServer() :
    return sys.stdin.readline()

if __name__ == '__main__':
    # Set max memory usage allowed (soft limit).
    parser = argparse.ArgumentParser(description='Client based on planning approach.')
    parser.add_argument('--max-memory', metavar='<MB>', type=float, default=2048.0,
                        help='The maximum memory usage allowed in MB (soft limit, default 2048).')

    strategy_group = parser.add_mutually_exclusive_group()
    args = parser.parse_args()
    memory.max_usage = args.max_memory

    try:
        if server :
            server_messages = sys.stdin
        else :
            server_messages=open('../levels/SAD1.lvl','r')
        
        ToServer('PlanningClient')
        #Read the input from server
        ReadHeaders(server_messages)
        
        if not server :
            server_messages.close()

    except Exception as ex:
        HandleError('PlanningClient'+str(repr(ex)))

    #Prepare objects to be used later for processing    
    SetUpObjects()    
    #Make initial pan that corresponds to the belief of the level
    MakeInitialPlan()
    #Find dependencies between goals, that is, if a goal should be achieved before another goal
    FindDependency()
    #sort the agents according to the number, so as to send their actions in the right order
    State.AgentAt.sort()
###########################################one time execution###################################################    
    count = 0 #used for testing, can be removed in the final deliverable
    
    """This gets called until every goal is reached"""
    
    while len(State.GoalLocations) > 0 and count < 10:        
        for agent in State.AgentAt :
            combined_actions = list()
            if len(agent.plan) == 0 :
                agent.MakePlan()
            combined_actions.append(agent.Execute())
            
            execute = ';'.join(combined_actions)  #prepare joint actions of agents to run parallely
            ToServer(execute)
            
            if server :
                step_succeed = FromServer() #if you want to see server's response, print with a #                
        
        count+=1
        
######################################################################################################################    
    ToServer('#Memory used ' + str(memory.get_usage()) + ' MB')
                
                
            
            
            
        
        

