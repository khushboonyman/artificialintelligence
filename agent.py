"""
Created on Wed Apr 15 21:55:26 2020
@author :
"""

import location
from box import Box
from state import *
from plan import *
#import state  #contains global variables
import sys
import re
from queue import PriorityQueue
import copy
from collections import deque
from request import *

def TranslateToDir(locfrom, locto):        
    if locfrom.x == locto.x:
        if locto.y == locfrom.y - 1:
            return 'W'
        else:
            return 'E'
    else:
        if locto.x == locfrom.x - 1:
            return 'N'
        else:
            return 'S'
           
class Agent:
    def __init__(self, location, color, number) :
        self.location = location
        self.color = color
        self.number = number
        self.plan1 = deque()
        self.plan2 = deque()
        self.move_box = None
        self.move_goal = None
        self.next_box = None
        self.next_goal = None
        self.request_plan = deque()
        self.boxes = set()
        self.next_request = deque()
        self.request_boxes = deque()
        self.wait = False
        
    def __str__(self):
        return str(self.location) + ' Col: ' + self.color + ' Num : ' + self.number

    def __hash__(self):
        return hash(str(self))
    
    def __eq__(self, other):
        if self.number == other.number and self.color == other.color and self.location == other.location :
            return True
        return False
    
    def __ne__(self, other):
        if self.number != other.number or self.color != other.color or self.location != other.location :
            return True
        return False
    
    def __lt__(self, other):
        if self.number < other.number :
            return True
        return False
    
    def __gt__(self, other):
        if self.number > other.number :
            return True
        return False

    def NoOp(self) :
        #print('from noop')
        return 'NoOp'
    
    def Move(self, agtto):
        if (self.location != agtto and agtto in State.FreeCells and agtto in State.Neighbours[self.location]):
            move_dir_agent = TranslateToDir(self.location, agtto)
            self.location.free_cell()
            State.FreeCells.add(self.location)
            self.location = agtto
            self.location.assign(self.number)
            State.FreeCells.remove(self.location)
            return 'Move(' + move_dir_agent + ')'
        
        return self.NoOp()

    def Push(self, box, boxto):
        if (self.location != boxto and box.location != boxto and boxto in State.FreeCells and self.color == box.color 
        and box.location in State.Neighbours[self.location] and boxto in State.Neighbours[box.location]):
            move_dir_agent = TranslateToDir(self.location, box.location)
            move_dir_box = TranslateToDir(box.location, boxto)
            self.location.free_cell()
            State.FreeCells.add(self.location)
            self.location = box.location
            self.location.assign(self.number)
            box.location = boxto
            box.location.assign(box.letter)
            State.FreeCells.remove(boxto)
            return 'Push(' + move_dir_agent + ',' + move_dir_box + ')'

        return self.NoOp()

    def Pull(self, box, agtto):
        if (self.location != agtto and box.location != self.location and agtto in State.FreeCells and self.color == box.color
        and agtto in State.Neighbours[self.location] and self.location in State.Neighbours[box.location]):
            move_dir_agent = TranslateToDir(self.location, agtto)
            curr_dir_box = TranslateToDir(self.location, box.location)
            box.location.free_cell()
            State.FreeCells.add(box.location)
            box.location = self.location
            box.location.assign(box.letter)
            self.location = agtto
            self.location.assign(self.number)
            State.FreeCells.remove(agtto)
            return 'Pull(' + move_dir_agent + ',' + curr_dir_box + ')'

        return self.NoOp()
                
    #there are some cells that are not free in the current plan, then agent tries to find another path .. unrelaxed
    def MakeCurrentIntentionPlan(self,request) :
        plan_a_b_g = deque()
        plan_a_b = Plan(self.location, self.move_box.location) # Plan for the agent to reach box
        plan_a_b.CreateIntentionPlan(self.location)
        
        if len(plan_a_b.plan) > 0 :
            plan_a_b.plan.reverse()
            plan_a_b_g.extend(plan_a_b.plan)
            plan_b_g = Plan(self.move_box.location, self.move_goal) # Plan for the box to reach goal            
            plan_b_g.CreateIntentionPlan(self.location,intention=True)
            if len(plan_b_g.plan) > 0 :
                plan_b_g.plan.reverse()
                plan_a_b_g.extend(plan_b_g.plan)
                if request :
                    self.request_plan = plan_a_b_g
                else :
                    self.plan1 = plan_a_b_g                    
                return True
        return False
    
    #agent picks goals that have no dependency and all boxes and finds shortest agent-box-goal path ..relaxed
    def MakeDesirePlan(self):
        if len(self.boxes) == 0 :
            return        
        self.move_box,self.move_goal = None,None
        self.plan1 = deque()        
        self.FindShortestPath()
        self.FindNextBox()
        
    #agent finds any intention plan 
    def MakeAnyIntentionPlan(self):                        
        plan_made = self.FindShortestIntentionPath()
        self.FindNextBox()
        return plan_made
        
    def Replan(self,other_box,other_goal) :        
        if other_box in self.boxes :
            self.boxes.remove(other_box)        
        self.move_box,self.move_goal = None,None
        self.plan1 = deque()        
        self.FindShortestPath(other_goal)
        self.FindNextBox()        
        self.boxes.add(other_box)
        
    def FindShortestPath(self,old_goal=None):
        min_plan_length = State.MAX_ROW*State.MAX_COL
        min_b_g_length = State.MAX_ROW*State.MAX_COL
        plan_made = False
        
        for box in self.boxes :
            plan_a_b = Plan(self.location, box.location) # Plan for the agent to reach box
            #if plan was found initially
            try :
                plan_a_b.plan = State.Plans[plan_a_b]
            except Exception as ex :
                plan_a_b.CreateBeliefPlan()                        
                if len(plan_a_b.plan) > 0 :
                    plan_a_b.plan.reverse()
                    State.Plans[plan_a_b] = plan_a_b.plan
                #plan_a_b.plan = State.Plans[plan_a_b] 
            plan_a_b_g = deque()    
            if len(plan_a_b.plan) > 0 :
                plan_a_b_g.extend(plan_a_b.plan)
                
                goal_location = None
                tmpQueue = PriorityQueue()
                
                while not box.goals.empty() :
                    heur_goal = box.goals.get()
                    goal_location = heur_goal[1]
                    tmpQueue.put(heur_goal)
                    if goal_location not in State.GoalDependency.keys() and (old_goal is None or goal_location != old_goal) :                        
                        break
                    else :
                        goal_location = None
                                    
                while not tmpQueue.empty() :
                    box.goals.put(tmpQueue.get())
                
                if goal_location is not None :                    
                    plan_b_g = Plan(box.location, goal_location) # Plan for the box to reach goal
                    #if plan was found initially
                    try :
                        plan_b_g.plan = State.Plans[plan_b_g]
                    except Exception as ex :
                        plan_b_g.CreateBeliefPlan()   
                        if len(plan_b_g.plan) > 0 :
                            plan_b_g.plan.reverse()
                            State.Plans[plan_b_g] = plan_b_g.plan
                    
                    if len(plan_b_g.plan) > 0 :
                        plan_a_b_g.extend(plan_b_g.plan)
                        #save the shortest path
                        if ((len(plan_a_b_g) == min_plan_length and len(plan_b_g.plan) < min_b_g_length)
                        or len(plan_a_b_g) < min_plan_length) :
                            plan_made = True
                            self.plan1 = plan_a_b_g.copy()
                            self.move_box = box
                            self.move_goal = goal_location
                            min_plan_length = len(plan_a_b_g)
                            min_b_g_length = len(plan_b_g.plan)
        return plan_made

    def FindShortestIntentionPath(self):        
        save_box = self.move_box
        self.move_box = None
        for box in self.boxes :
            if box != save_box :
                plan_a_b = Plan(self.location, box.location) # Plan for the agent to reach box
                plan_a_b.CreateIntentionPlan(self.location)                        
                if len(plan_a_b.plan) > 0 :
                    plan_a_b.plan.reverse()                    
                    plan_a_b_g = deque()    
                    plan_a_b_g.extend(plan_a_b.plan)
                
                    goal_location = None
                    tmpQueue = PriorityQueue()
                
                    while not box.goals.empty() :
                        heur_goal = box.goals.get()
                        goal_location = heur_goal[1]
                        tmpQueue.put(heur_goal)
                        if goal_location not in State.GoalDependency.keys() :                        
                            plan_b_g = Plan(box.location, goal_location) # Plan for the box to reach goal
                            plan_b_g.CreateIntentionPlan(self.location,intention=True) 
                            if len(plan_b_g.plan) > 0 :
                                plan_b_g.plan.reverse()
                                plan_a_b_g.extend(plan_b_g.plan)
                                self.plan1 = plan_a_b_g
                                self.move_box = box
                                self.move_goal = goal_location
                                break
                                               
                    while not tmpQueue.empty() :
                        box.goals.put(tmpQueue.get())
 
        if self.move_box is None :
            self.move_box = save_box
    
    
    def FindNextBox(self) :
        
        if len(self.plan1) == 0 :
            return
        
        self.next_box,self.next_goal = None,None
        self.plan2 = deque()
        
        if len(self.boxes) == 0 or (len(self.boxes) == 1 and self.move_box in self.boxes) :
            return
        
        agent_next_loc =  self.plan1[-2]        
        min_plan_length = State.MAX_ROW*State.MAX_COL
        min_b_g_length = State.MAX_ROW*State.MAX_COL
        
        for box in self.boxes :
            if box != self.move_box :
                plan_a_b = Plan(agent_next_loc, box.location) # Plan for the agent to reach box
            #if plan was found initially
                try :
                    plan_a_b.plan = State.Plans[plan_a_b]
                except Exception as ex :
                    plan_a_b.CreateBeliefPlan()                        
                    if len(plan_a_b.plan) > 0 :
                        plan_a_b.plan.reverse()
                    
                plan_a_b_g = deque()
                if len(plan_a_b.plan) > 0 :
                    plan_a_b_g.extend(plan_a_b.plan)                                    
                
                    goal_location = None
                    tmpQueue = PriorityQueue()
                    
                    while not box.goals.empty() :
                        heur_goal = box.goals.get()
                        goal_location = heur_goal[1]
                        tmpQueue.put(heur_goal)  #only select goals that don't have dependency
                        if goal_location not in State.GoalDependency.keys() and goal_location != self.move_goal :
                            break
                        else :
                            goal_location = None
                    
                    while not tmpQueue.empty() :
                        box.goals.put(tmpQueue.get())
                
                    if goal_location is not None :                    
                        plan_b_g = Plan(box.location, goal_location) # Plan for the box to reach goal
                        
                        try :
                            plan_b_g.plan = State.Plans[plan_b_g]  #if plan was found initially
                        except Exception as ex :
                            plan_b_g.CreateBeliefPlan()                        
                            if len(plan_b_g.plan) > 0 :
                                plan_b_g.plan.reverse()
                        
                        if len(plan_b_g.plan) > 0 :
                            plan_a_b_g.extend(plan_b_g.plan)
                            #save the shortest path
                            if ((len(plan_a_b_g) == min_plan_length and len(plan_b_g.plan) < min_b_g_length)
                            or len(plan_a_b_g) < min_plan_length) :
                                self.plan2 = plan_a_b_g.copy()
                                self.next_box = box
                                self.next_goal = goal_location
                                min_plan_length = len(plan_a_b_g)
                                min_b_g_length = len(plan_b_g.plan)
    
    #delete box goal combinations when box is on the goal location                                
    def DeleteCells(self) :
        #update goal dependencies
        dependents = deque() #Find the goals that are dependent
        for key,value in State.GoalDependency.items() :
            if self.move_goal in value :
                dependents.append(key)                        
        while len(dependents) != 0 : #delete the dependee goal if in satellite data and remove dependent if no more dependee
            dependent = dependents.pop() 
            State.GoalDependency[dependent].remove(self.move_goal)
            if len(State.GoalDependency[dependent]) == 0 :
                del(State.GoalDependency[dependent])    
        
        #delete goal from boxes
        for box in self.boxes :
            if box != self.move_box :                
                tmpQueue = PriorityQueue()
                while not box.goals.empty() :            
                    heur_goal = box.goals.get()
                    if heur_goal[1] != self.move_goal :
                        tmpQueue.put(heur_goal)
                while not tmpQueue.empty() :
                    box.goals.put(tmpQueue.get())
        
        if self.move_goal in State.GoalLocations :
            State.GoalLocations.remove(self.move_goal)   
        #delete box from agent's box list
        new_set_of_boxes = set()
        for box in self.boxes :
            if box != self.move_box :
                new_set_of_boxes.add(box)
        self.boxes = new_set_of_boxes
        
        #delete box from other agent's box list
        for agent in State.AgentAt :
            if agent != self and agent.color == self.color :
                agent.boxes = new_set_of_boxes
                if agent.next_box is not None and agent.next_box == self.move_box :
                    agent.next_box = None
                    agent.next_goal = None
                    agent.plan2 = deque()
        

    #delete box goal combinations when box is on the goal location                                
    def UpdateCells(self) :
        #check if it was a goal the box was moved to
                    
        goal_yes = False
        if self.move_goal in State.GoalLocations :
            tmpQueue = PriorityQueue()
            while not self.move_box.goals.empty() :            
                heur_goal = self.move_box.goals.get()
                if heur_goal[1] == self.move_goal :
                    goal_yes = True                    
                tmpQueue.put(heur_goal)
            while not tmpQueue.empty() :
                self.move_box.goals.put(tmpQueue.get())
                     
        if goal_yes :
            self.DeleteCells()
        else :    
        #update box to goal priority queue
            tmpQueue = PriorityQueue()
            for box in self.boxes :
                if box == self.move_box :                    
                    while not box.goals.empty() :            
                        heur_goal = box.goals.get()
                        goal_location = heur_goal[1] 
                        plan_b_g = Plan(box.location,goal_location)    
                        try :
                            plan_b_g.plan = State.Plans[plan_b_g]
                        except Exception as ex :
                            plan_b_g.CreateBeliefPlan()                      
                            if len(plan_b_g.plan) > 0 :
                                plan_b_g.plan.reverse()
                                State.Plans[plan_b_g] = plan_b_g.plan
                        tmpQueue.put((len(plan_b_g.plan),goal_location))
                                
                    while not tmpQueue.empty() :
                        box.goals.put(tmpQueue.get())
                     
        #update next request
        if len(self.next_request) > 0 :
            self.request_plan = self.next_request
            self.move_box = self.request_boxes.popleft()
            self.next_request = deque()
            self.FindRequestGoal()
        else :
            self.request_plan = deque()
                                
        
        
    def FindDeadCells(self,how_many,box_from,to_free_cells) :        
        count = 0
        frontier = deque()
        frontier.append(box_from.location)
        frontier_set = set()
        frontier_set.add(box_from.location)
        dead_cells = deque()        
        
        while len(frontier) > 0 and count < how_many :            
            cell = frontier.popleft()
            if cell != self.location :
                #if cell not in to_free_cells and cell in State.FreeCells :
                if cell not in to_free_cells and cell in State.FreeCells :
                    count += 1
                    dead_cells.append(cell)
                for leaf in State.Neighbours[cell] :
                    if leaf not in frontier_set :
                        frontier_set.add(leaf)
                        frontier.append(leaf)
                    
        if count == how_many - 1 :
            dead_cells.append(self.location)
        return dead_cells

    def PlanMoveBoxes(self,to_free_cells) :        
        new_boxes = deque()
        self.request_plan = deque()
        
        for box in self.request_boxes :
            plan_a_b = Plan(self.location,box.location)
            plan_a_b.CreateIntentionPlan(self.location)
            if len(plan_a_b.plan) > 0 :
                plan_a_b.plan.reverse()
                new_boxes.append(box)
                self.request_boxes.remove(box)
                break
        if len(new_boxes) == 0 :
            return False,0
    
        additional_locations = set()
        additional_locations.add(box.location)
        additional_locations.add(self.location)        
        dead_cells = self.FindDeadCells(len(self.request_boxes)+1,box,State.Paths)
        if len(dead_cells) == 0 :
            return False,0
        
        dead_cell = dead_cells.pop()
        plan_b_c = Plan(box.location,dead_cell)
        plan_b_c.CreateIntentionPlan(self.location,intention=True)
        if len(plan_b_c.plan) > 0 :
            plan_b_c.plan.reverse()
            self.request_plan.extend(plan_a_b.plan)
            self.request_plan.extend(plan_b_c.plan)
        else :
            return False,0        
        
        while len(self.request_boxes) > 0 :            
            for box in self.request_boxes :
                next_agent_location = self.request_plan[-2]
                plan_a_b = Plan(next_agent_location,box.location)
                plan_a_b.CreateAlternativeIntentionPlan(additional_locations)
                if len(plan_a_b.plan) > 0 :
                    plan_a_b.plan.reverse()
                    new_boxes.append(box)
                    additional_locations.add(box.location)
                    self.request_boxes.remove(box)
                    break                    
                
            if len(plan_a_b.plan) == 0 or len(dead_cells) == 0 :
                return True,len(self.request_plan)
            
            dead_cell = dead_cells.pop()
            plan_b_c = Plan(box.location,dead_cell)
            plan_b_c.CreateAlternativeIntentionPlan(additional_locations,intention=True)
            if len(plan_b_c.plan) > 0 :
                plan_b_c.plan.reverse()
                self.request_plan.extend(plan_a_b.plan)
                self.request_plan.extend(plan_b_c.plan)
            else :
                return True,len(self.request_plan)
            
        self.request_boxes = new_boxes
        return True,len(self.request_plan)
        
    def PlanAnotherPlace(self,to_free_cells) : 
        frontier = deque()
        frontier.append(self.location)
        came_from = {}
        frontier_set = set()
        frontier_set.add(self.location)
        came_from[self.location] = None
        end_loc = None
        
        while len(frontier) > 0 :
            current = frontier.popleft()        
            if current not in to_free_cells :
                end_loc = current
                break        
            for n in State.Neighbours[current]:
                if n in State.FreeCells and n not in frontier_set :
                    frontier.append(n)
                    frontier_set.add(n)
                    came_from[n] = current
        
        self.request_plan = deque()
        
        current = end_loc 
        
        while current != self.location :
            self.request_plan.append(current)
            if current in came_from.keys() :
                current = came_from[current]
            else :
                self.request_plan = deque()
                break
        
        
    def PlanRequest(self,requests) :  #make plan for request
        self.request_boxes = deque()
        paths = set()
        for req in requests :
            if req.blocking_box is not None :
                self.request_boxes.append(req.blocking_box)
            if len(paths) == 0 :
                paths = req.free_these_cells
        
        if len(self.request_boxes) == 0 :
            self.PlanAnotherPlace(paths)
            if len(self.request_plan) > 0 :
                self.request_plan.reverse()
                return True,len(self.request_plan)
            else :
                return False,0
        else :
            return self.PlanMoveBoxes(paths)
                            
    def AssignRequest(self,agent,request,blocking_box=None) :
        if request :
            new_request = Request(blocking_box,set(self.request_plan))
        else :
            new_request = Request(blocking_box,set(self.plan1))        
            
        if agent not in State.Requests.keys() :
            State.Requests[agent] = deque()
        State.Requests[agent].append(new_request)   
                         
    #make a request to some agent because the current plan cannot be executed, agent could be blocked or box could be blocked        
    def MakeRequest(self,free_these_cells,request) :        
        pattern_box = re.compile("[A-Z]+")
        pattern_agent = re.compile("[0-9]+")

        for cell in free_these_cells :
            letter_or_num = State.current_level[cell.x][cell.y]
            if pattern_box.fullmatch(letter_or_num) is not None:
                agents,blocking_box = State.getBoxAgent(letter_or_num,cell)
                if len(agents) > 0 and blocking_box is not None :
                    for agent in agents :
                        if blocking_box not in agent.request_boxes and blocking_box != agent.move_box and len(agent.request_plan) == 0 :
                            self.AssignRequest(agent,request,blocking_box)
                if blocking_box is None or blocking_box.color != self.color :
                    self.wait = True
            elif pattern_agent.fullmatch(letter_or_num) is not None:
                agent = State.getAgentAgent(letter_or_num)
                if (len(agent.plan1) == 0 or agent.wait) and len(agent.request_plan) == 0:
                    agent.wait = False
                    self.AssignRequest(agent,request)
                else :
                    self.wait = True
                
   
    def PullDecision(self) :
        pull = False
        agent_to = None
        
        if len(self.plan2) > 0 :
            next_start = self.plan2[0]
            if next_start not in self.plan1 and next_start != self.location :
                pull = True
                if len(self.plan1) > 1 :
                    agent_to = self.plan1[1]
                    if len(self.request_plan) == 2 :
                        available = set(State.Neighbours[agent_to]).intersection(set(State.Neighbours[next_start])).discard(self.move_box.location)
                        if available is None :
                            pull = False
                            agent_to = None
                else :
                    for n in State.Neighbours[self.move_goal] :
                        if n in State.Neighbours[next_start] and n in State.FreeCells :
                            agent_to = n
                            break
        return pull,agent_to
        
    def PullRequest(self) :
        pull = False
        agent_to = None
        
        if len(self.next_request) > 0 :
            next_start = self.next_request[0]
            if next_start not in self.request_plan and next_start != self.location :
                pull = True
                if len(self.request_plan) > 1 :
                    agent_to = self.request_plan[1]
                    if len(self.request_plan) == 2 :
                        ToServer('#'+str(agent_to)+' '+str(next_start)+' '+str(self.move_box))
                        available = set(State.Neighbours[agent_to]).intersection(set(State.Neighbours[next_start])).discard(self.move_box.location)
                        if available is None :
                            pull = False
                            agent_to = None
                else :
                    for n in State.Neighbours[self.move_goal] :
                        if n in State.Neighbours[next_start] and n in State.FreeCells :
                            agent_to = n  # if it is not free, then ?
                            break
                        
        return pull,agent_to
    
    def ExecuteDecision(self) :
        
        if len(self.request_plan) > 0 :   #prioritise request
            return self.ExecuteRequest()
        
        action = self.NoOp()
        
        if self.wait :
            return action
                
        cell1 = self.plan1.popleft()
        cell2 = self.plan1[0]  
        
             
        if self.move_box.location != cell1 :  #Move towards the box
            action = self.Move(cell1)  
        else:            
            if cell2 != self.location : #If next to next location is where box should be, then push
                action = self.Push(self.move_box,cell2)
            else:
                pull,agent_to = self.PullDecision() #check if rest of actions should be pull or push                
                if pull and agent_to is not None and len(set(State.Neighbours[agent_to]).intersection(State.FreeCells)) > 1:
                    if agent_to in State.FreeCells :
                        action = self.Pull(self.move_box, agent_to)
                    else :
                        free_these_cells = set()
                        free_these_cells.add(agent_to)
                        self.MakeRequest(free_these_cells,request=False)
                else :
                    small_frontier = PriorityQueue()
                    for n in State.Neighbours[self.location]:
                        if n in State.FreeCells and n != self.move_box.location :
                            small_heur = -1 * (abs(n.x - self.move_goal.x) + abs(n.y - self.move_goal.y))
                            small_frontier.put((small_heur, n))
                    if not small_frontier.empty():
                        agent_to = small_frontier.get()[1]
                        action = self.Pull(self.move_box, agent_to)                            
        
        if self.move_box.location == self.move_goal :
            self.plan1 = deque()
            self.DeleteCells()
            
        return action

    def FindRequestGoal(self) :
        list_request = list(self.request_plan)
        
        for index,p in enumerate(list_request) :
            if index < len(list_request)-1 :
                nextP = self.request_plan[index+1]
                man_dist = abs(nextP.x - p.x) + abs(nextP.y - p.y)
                if man_dist != 1 :                    
                    self.next_request = deque(list_request[index+1:])
                    self.request_plan = deque(list_request[:index+1])
                    break
                
        self.move_goal = self.request_plan[-1]
        return
        
    def ExecuteRequest(self) :
        
        action = self.NoOp()
        if self.wait :
            return action
        
        if len(self.plan1) > 0 :
            if len(self.request_boxes) > 0 :
                self.move_box = self.request_boxes.popleft()
                self.FindRequestGoal()
        #if self.move_goal is None and self.move_box is not None :
        #    self.FindRequestGoal()
            
        cell1 = self.request_plan.popleft()       
        
        #Move towards the box
        if self.move_box is None or self.move_box.location != cell1 :  #Move towards the box
            action = self.Move(cell1)  
        else:
            cell2 = self.request_plan[0]             
            if cell2 != self.location : #If next to next location is where box should be, then push
                action = self.Push(self.move_box,cell2)
            else:
                pull,agent_to = self.PullRequest() #check if rest of actions should be pull or push
                if pull and agent_to is not None and len(set(State.Neighbours[agent_to]).intersection(State.FreeCells)) > 1:
                    if agent_to in State.FreeCells :
                        action = self.Pull(self.move_box, agent_to)
                    else :
                        free_these_cells = set()
                        free_these_cells.add(agent_to)
                        self.MakeRequest(free_these_cells,request=True)
                else :
                    small_frontier = PriorityQueue()
                    for n in State.Neighbours[self.location]:
                        if n in State.FreeCells and n != self.move_box.location :
                            small_heur = -1 * (abs(n.x - self.move_goal.x) + abs(n.y - self.move_goal.y))
                            small_frontier.put((small_heur, n))
                    if not small_frontier.empty():
                        agent_to = small_frontier.get()[1]
                        action = self.Pull(self.move_box, agent_to)                             
        
        if self.move_box is not None and self.move_goal is not None and self.move_box.location == self.move_goal :
            self.UpdateCells()
        
        if action != self.NoOp() and len(self.plan1) > 0 :
            self.plan1,self.plan2 = deque(),deque()
            self.next_box,self.next_goal = None,None
            
        return action
    
    #check for requests, check for feasibility of the plan and execute 
    def Check(self):          
        #find if any desire plan path is not free
        if len(self.request_plan) > 0 :
            self.CheckRequestPlan()
            return
            
        if len(self.plan1) == 0 :
            return
        
        not_free_cells = set(self.plan1).difference(State.FreeCells)
        if self.move_box is not None :
            not_free_cells.discard(self.move_box.location)
        not_free_cells.discard(self.location)
    
        #while replanning, make intentional plan
        if len(not_free_cells) != 0 :            
            ip_made = False             
            ip_made = self.MakeCurrentIntentionPlan(request=False) #first try with chosen box and goal
            if not ip_made and not State.SingleAgent :       
                ip_made = self.MakeAnyIntentionPlan() #see if any plan can be made        
            if not ip_made :
                self.MakeRequest(not_free_cells,request=False) #make request to agent whose box blocks the current agent
        else :        
            self.wait = False
                
    def CheckRequestPlan(self):          
        #find if any desire plan path is not free
            
        not_free_cells = set(self.request_plan).difference(State.FreeCells)
        if self.move_box is not None :
            not_free_cells.discard(self.move_box.location)
        not_free_cells.discard(self.location)
    
        #while replanning, make intentional plan
        if len(not_free_cells) != 0 :            
            ip_made = False             
            ip_made = self.MakeCurrentIntentionPlan(request=True) #first try with chosen box and goal        
            if not ip_made :
                self.MakeRequest(not_free_cells,request=True) #make request to agent whose box blocks the current agent
        else :            
            self.wait = False