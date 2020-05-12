# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 11:37:17 2020

@author: Bruger
"""

agent = CurrentState.AgentAt[0]
box = CurrentState.BoxAt[0]

#print(agent_0.Push(box_A,loc00))
#print(agent_0.Pull(loc02,box_A))
print(agent.Move(locations[1][7]))
print(agent.Move(locations[1][6]))
print(agent.Move(locations[1][5]))
print(agent.Move(locations[1][4]))
print(agent.Move(locations[1][3]))
print(agent.Move(locations[1][2]))
print(agent.Move(locations[1][1]))
print(agent.Move(locations[2][1]))
print(agent.Move(locations[3][1]))
print(agent.Move(locations[3][2]))
print(agent.Move(locations[3][3]))
print(agent.Move(locations[3][4]))
print(agent.Move(locations[3][5]))
print(agent.Move(locations[3][6]))
print(agent.Move(locations[3][7]))
print(agent.Move(locations[3][8]))
print(agent.Move(locations[3][9]))
print(agent.Move(locations[3][10]))

print(agent.Push(box,locations[1][10]))
print(agent.Pull(locations[3][10],box))


