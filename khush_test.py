# -*- coding: utf-8 -*-
"""
Created on Mon May 11 14:40:32 2020

@author: Bruger
"""

for p in State.Plans :
    print(p)
    for i in p.plan :
        print(i)

for key,value in State.GoalDependency.items() :
    print(key)
    print('is dependent on')
    for v in value :
        print(v)
    print()

for key,value in State.GoalAt.items() :
    print(key)
    for v in value :
        print(v)
        
for key,value in State.GoalPaths.items() :
    print('goal is'+str(key.end))
    for v in value :
        print(v)

for cells in State.DeadCells :
    if State.current_level[cells.x][cells.y] == ' ' or State.current_level[cells.x][cells.y] == '0'  :
        State.current_level[cells.x] = State.current_level[cells.x][:cells.y]+'*'+State.current_level[cells.x][cells.y+1:] 
        
l = Location(2,2)
for n in State.Neighbours[l] :
    print(n)
    
for agent in State.AgentAt :
    print('agent'+str(agent))
    for box in agent.boxes :
        print('box'+str(box))
        while not box.goals.empty() :
            length,goal = box.goals.get()
            print('goals'+str(length)+str(goal))
            
for agent in State.AgentAt :   
    print('agent '+str(agent)+ ' boxes ')
    for box in agent.request_boxes :
        print(box)
    for p in agent.request_plan :
        print(p)
                           
for key,value in State.Requests.items() :
    print('assigned to'+str(key))
    for v in value :
        print(v)
            
########################TESTING##################################

    
   

       
                        