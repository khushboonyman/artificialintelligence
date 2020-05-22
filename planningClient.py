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
from setupobjects import *
import globals

x=2500
sys.setrecursionlimit(x)

def FromServer() :
    return sys.stdin.readline()

if __name__ == '__main__':
    # Set max memory usage allowed (soft limit).
    parser = argparse.ArgumentParser(description='Client based on planning approach.')
    parser.add_argument('--max-memory', metavar='<MB>', type=float, default=2048.0,
                        help='The maximum memory usage allowed in MB (soft limit, default 2048).')
    parser.add_argument('--server', type=bool, default=False,
                        help='The maximum memory usage allowed in MB (soft limit, default 2048).')

    args = parser.parse_args()
    memory.max_usage = args.max_memory
    globals.server = args.server

    try:
        if globals.server:
            server_messages = sys.stdin
        else :
            server_messages = open('levels/levels2020/works/SAthreePO.lvl', 'r')
        ToServer('PlanningClient')
        #Read the input from server
        ReadHeaders(server_messages)
        
        if not globals.server :
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
    #FindDeadCells()
    no_op = 'NoOp'
###########################################one time execution###################################################    
    """This gets called until every goal is reached"""
    #while len(State.GoalAt) > 0 and count < 1:
    while True :
        cont = False
        for agent in State.AgentAt :
            if len(agent.plan1) == 0 and len(agent.request_plan) == 0 :
                if len(agent.plan2) == 0 :
                    agent.MakeDesirePlan()
                else :
                    agent.plan1 = agent.plan2
                    agent.move_box = agent.next_box
                    agent.move_goal = agent.next_goal
                    agent.FindNextBox()
                    
            if len(agent.plan1) != 0 or len(agent.request_plan) != 0 :
                cont = True
        
        if not cont :
            break
        
        while True :
            conflict = False
            for agent1 in State.AgentAt :
                for agent2 in State.AgentAt :
                    if ((agent1.color == agent2.color and agent1 != agent2) 
                    and ((agent1.move_box is not None and agent2.move_box is not None and agent1.move_box == agent2.move_box) 
                    or (agent1.move_goal is not None and agent2.move_goal is not None and agent1.move_goal == agent2.move_goal))) :
                        conflict = True
                        if len(agent1.plan1) <= len(agent2.plan1) :
                            agent2.Replan(agent1.move_box,agent1.move_goal)
                        else :
                            agent1.Replan(agent2.move_box,agent2.move_goal)
            if not conflict :
                break
        
        combined_actions = list()
        
        for agent in State.AgentAt :
            agent.Check()
        
        if len(State.Requests) != 0 :
            State.Bidding()
            
############################################################################################################        
        for agent in State.AgentAt :
            agent_action = no_op
            if len(agent.plan1) > 0 or len(agent.request_plan) > 0 :
                agent_action = agent.ExecuteDecision()            
            combined_actions.append(agent_action)
        
        
        execute = ';'.join(combined_actions)  #prepare joint actions of agents to run parallely    
        ToServer(execute)
                     
        if globals.server :
            step_succeed = FromServer() #if you want to see server's response, print with a #                
            result = step_succeed.rstrip().split(';')
            if 'false' in result :
                final_combined_actions = list()
                for index,r in enumerate(result) :
                    if r == 'true' :
                        agent_action = no_op
                    else :
                        agent_action = combined_actions[index]
                    final_combined_actions.append(agent_action)
                execute = ';'.join(final_combined_actions)  #prepare joint actions of agents to run parallely    
                ToServer(execute)         
        
        
######################################################################################################################    
    ToServer('#Memory used ' + str(memory.get_usage()) + ' MB')

            
            
            
        
        

