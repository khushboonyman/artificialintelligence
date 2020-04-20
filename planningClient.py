import sys
import argparse
import memory
import re
from HardCoded import *
from location import *
from agent import *
from box import *
from state import *
from plan import *

def HandleError(message):
    print(message,file=sys.stderr,flush=True)

def Readlines(msg):
    #add it when using sysin
    #return msg.readline().rstrip()
    #remove it when using sysin
    return msg.pop(0).rstrip()
    
def ReadHeaders(messages) :
    list_of_colors = ['blue','red','cyan','purple','green','orange','pink','grey','lightblue','brown']
    line = Readlines(messages)
    if line == '#domain' :
        line = Readlines(messages)
        if line != 'hospital' :
            HandleError('Incorrect domain, it can only be hospital')
        else:
            ToServer('#Domain is '+line)
    else :
        HandleError('First line should be #domain') 
    
    line = Readlines(messages)
    if line == '#levelname' :
        line = Readlines(messages)
        ToServer('#Level name is '+line)
    else :
        HandleError('Level name is missing') 
    
    line = Readlines(messages)
    added = list()
    if line == '#colors' :
        color_dict = {}
        while True :
            line = Readlines(messages)
            color_data = re.split(', |: |\s',line)
            if color_data[0] in list_of_colors :
                if color_data[0] in color_dict.keys() :
                    HandleError('Color is repeated')
                else :
                    for box_or_agent in color_data :
                        if box_or_agent in added :
                            HandleError('Box or agent has already been specified')
                        else :
                            added.append(box_or_agent)
                    color_dict[color_data[0]] = color_data[1:]
            else :
                if line[0] == '#' :
                    break
                else :
                    HandleError('Unacceptable color')
    else :
        HandleError('Colors missing')
    
    if line == '#initial' :
        line = Readlines(messages)
        initial_state = list()
        while line[0] == '+' :
            initial_state.append(line)
            line = Readlines(messages)
    else :
        HandleError('Initial state missing')
             
    if line == '#goal' :
        line = Readlines(messages)
        goal_state = list()
        while line[0] == '+' :
            goal_state.append(line)
            line = Readlines(messages)
    else :
        HandleError('Goal state missing')
             
    if line != '#end' :
        HandleError('End missing')    
    
    return color_dict,initial_state,goal_state
 
def FindBox(color,letter) :
    boxes = list()
    for box in CurrentState.BoxAt :
        if box.color == color and box.letter == letter :
            boxes.append(box)
    return boxes

def FindAgent(color) :
    for agent in CurrentState.AgentAt :
        if agent.color == color :
            return agent
    return None

def MakePlan() :
    plans_box = {}
    for goal in FinalState.GoalAt :
        boxes = FindBox(goal.color,goal.letter)
        agent = FindAgent(goal.color)
        if agent is not None :            
            plans = list()
            for box in boxes :
                plan_a = Plan(agent.location,box.location)
                plan_b = Plan(box.location,goal.location)
                action = []
                if plan_a.CreatePlan(agent.location) :
                    #print(plan_a.plan)
                    plan_a.plan.reverse()
                    action.extend(plan_a.plan)
                if plan_b.CreatePlan(box.location) :
                    #print(plan_b.plan)
                    plan_b.plan.reverse()
                    action.extend(plan_b.plan)
                plans.append(action)
            index_of_box = plans.index(min(plans))
            box_chosen = boxes[index_of_box]
            plans_box[agent]=(box_chosen,min(plans))
            
    return plans_box
                
if __name__ == '__main__':    
    # Set max memory usage allowed (soft limit).
    parser = argparse.ArgumentParser(description='Client based on planning approach.')
    parser.add_argument('--max-memory', metavar='<MB>', type=float, default=2048.0, help='The maximum memory usage allowed in MB (soft limit, default 2048).')
    
    strategy_group = parser.add_mutually_exclusive_group()
    args = parser.parse_args()
    memory.max_usage = args.max_memory
    
    # Run client.
    try:
        #add when using input from sysin
        #server_messages = sys.stdin
        #ToServer('PlanningClient')
        #remove when using sysin
        f=open('../SAExample.lvl','r')
        server_messages = f.readlines()
        f.close()
        #remove until here
        color_dict,initial_state,goal_state = ReadHeaders(server_messages) 
            
    except Exception as ex:
        print('Error parsing level: {}.'.format(repr(ex)), file=sys.stderr, flush=True)
        sys.exit(1)
    
    #below line is only for testing purpose                      
    #HardCodedForDefault()    
    State.current_state = initial_state
    MAX_ROW = len(initial_state)
    MAX_COL = len(initial_state[0])
    locations = list()
    pattern_agent = re.compile("[0-9]+")
    pattern_box = re.compile("[A-Z]+")
    for i_index,row in enumerate(State.current_state) :
        firstlist = list()
        for j_index,col in enumerate(row) :
            loc = Location(i_index,j_index)
            firstlist.append(loc)
            if col == ' ' :
                CurrentState.FreeCells.append(loc)
            if pattern_agent.fullmatch(col) is not None :
                for key,value in color_dict.items() :
                    if col in value :
                        agent = Agent(loc,key,col)
                        CurrentState.AgentAt.append(agent)
            if pattern_box.fullmatch(col) is not None :
                for key,value in color_dict.items() :
                    if col in value :
                        box = Box(loc,key,col)
                        CurrentState.BoxAt.append(box)
            goal = goal_state[i_index][j_index]
            if pattern_box.fullmatch(goal) is not None :
                for key,value in color_dict.items() :
                    if goal in value :
                        box = Box(loc,key,goal)
                        FinalState.GoalAt.append(box)
        locations.append(firstlist)
    for row in range(1,MAX_ROW-1) :
        for col in range(1,MAX_COL-1):
            CurrentState.Neighbours[locations[row][col]] = list()
            if State.current_state[row+1][col] != '+' :
                CurrentState.Neighbours[locations[row][col]].append(locations[row+1][col])
            if State.current_state[row-1][col] != '+' :
                CurrentState.Neighbours[locations[row][col]].append(locations[row-1][col])
            if State.current_state[row][col+1] != '+' :
                CurrentState.Neighbours[locations[row][col]].append(locations[row][col+1])
            if State.current_state[row][col-1] != '+' :
                CurrentState.Neighbours[locations[row][col]].append(locations[row][col-1])
    current_plan = MakePlan()
    for agent,box_cells in current_plan.items() :
        box = box_cells[0]
        cells = box_cells[1]
        agent.ExecutePlan(box,cells)
        
    
#for c in cells :
#    print(c)
    
#for c in current_plan[1] :
#    print(c)       
