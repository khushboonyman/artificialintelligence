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
    def __init__(self, location, color, number, plan1=deque(), plan2 = deque(),move_box = None, move_goal = None, 
        request_plan = list(), boxes = set(), next_box = None, next_goal = None):
        self.location = location
        self.color = color
        self.number = number
        self.plan1 = plan1
        self.plan2 = plan2
        self.move_box = move_box
        self.move_goal = move_goal
        self.next_box = next_box
        self.next_goal = next_goal
        self.request_plan = request_plan
        self.boxes = boxes
        
    def __str__(self):
        return str(self.location) + ' Color : ' + self.color + ' Letter : ' + self.number

    def __hash__(self):
        return hash(self.number)
    
    def __eq__(self, other):
        if self.number == other.number :
            return True
        return False
    
    def __ne__(self, other):
        if self.number != other.number :
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

    #agent had a plan but had to execute some other tasks and now she replans because she changed location .. relaxed
    def MakeBoxGoalDesirePlan(self) :
        plan_a_b_g = deque()
        plan_a_b = Plan(self.location, self.move_box.location) # Plan for the agent to reach box
        if plan_a_b in State.Plans.keys() :
            plan_a_b.plan = State.Plans[plan_a_b]
            agent_has_plan_to_box = True
        else :
            agent_has_plan_to_box = plan_a_b.CreateBeliefPlan(self.location)
            if agent_has_plan_to_box :
                plan_a_b.plan.reverse()
                    
        if agent_has_plan_to_box :
            State.Plans[plan_a_b] = plan_a_b.plan
            plan_a_b_g.extend(plan_a_b.plan)
            plan_b_g = Plan(self.move_box.location, self.move_goal) # Plan for the box to reach goal
            if plan_b_g in State.Plans.keys() :
                plan_b_g.plan = State.Plans[plan_b_g]
                box_has_plan_to_goal = True
            else :
                box_has_plan_to_goal = plan_b_g.CreateBeliefPlan(self.move_box.location)
                if box_has_plan_to_goal :
                    plan_b_g.plan.reverse()
                    
            if box_has_plan_to_goal :
                State.Plans[plan_b_g] = plan_b_g.plan
                plan_a_b_g.extend(plan_b_g.plan)
                self.plan = plan_a_b_g
    
    #agent has a request and needs to reach a box to free another agent .. unrelaxed
    def MakeBoxIntentionPlan(self,box) :        
        plan_a_b = Plan(self.location, box.location) # Plan for the agent to reach box        
        agent_has_plan_to_box = plan_a_b.CreateIntentionPlan(self.location,self.location)
        if agent_has_plan_to_box :
            plan_a_b.plan.reverse()
            plan_a_b.plan.pop()
            self.request_plan = plan_a_b.plan
                
    #there are some cells that are not free in the current plan, then agent tries to find another path .. unrelaxed
    def MakeCurrentIntentionPlan(self) :
        plan_a_b_g = deque()
        plan_a_b = Plan(self.location, self.move_box.location) # Plan for the agent to reach box
        agent_has_plan_to_box = plan_a_b.CreateIntentionPlan(self.location,self.location)
        
        if agent_has_plan_to_box :
            plan_a_b.plan.reverse()
            plan_a_b_g.extend(plan_a_b.plan)
            plan_b_g = Plan(self.move_box.location, self.move_goal) # Plan for the box to reach goal            
            box_has_plan_to_goal = plan_b_g.CreateIntentionPlan(self.move_box.location,self.location)
            if box_has_plan_to_goal :
                plan_b_g.plan.reverse()
                plan_a_b_g.extend(plan_b_g.plan)
                self.plan = plan_a_b_g
                
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
        self.FindShortestIntentionPath()
        self.FindNextBox()
        
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
        
        for box in self.boxes :
            plan_a_b = Plan(self.location, box.location) # Plan for the agent to reach box
            #if plan was found initially
            try :
                plan_a_b.plan = State.Plans[plan_a_b]
                agent_has_plan_to_box = True
            except Exception as ex :
                agent_has_plan_to_box = plan_a_b.CreateBeliefPlan(self.location)                        
                if agent_has_plan_to_box :
                    plan_a_b.plan.reverse()
                    State.Plans[plan_a_b] = plan_a_b.plan
                #plan_a_b.plan = State.Plans[plan_a_b] 
            plan_a_b_g = deque()    
            if agent_has_plan_to_box :
                plan_a_b_g.extend(plan_a_b.plan)
                
                goal_location = None
                tmpQueue = PriorityQueue()
                
                while not box.goals.empty() :
                    goal = box.goals.get()
                    goal_location = goal[1]
                    tmpQueue.put(goal)
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
                        box_has_plan_to_goal = True
                    except Exception as ex :
                        box_has_plan_to_goal = plan_b_g.CreateBeliefPlan(box.location)                        
                        if box_has_plan_to_goal :
                            plan_b_g.plan.reverse()
                            State.Plans[plan_b_g] = plan_b_g.plan
                    
                    if box_has_plan_to_goal :
                        plan_a_b_g.extend(plan_b_g.plan)
                        #save the shortest path
                        if ((len(plan_a_b_g) == min_plan_length and len(plan_b_g.plan) < min_b_g_length)
                        or len(plan_a_b_g) < min_plan_length) :
                            self.plan1 = plan_a_b_g.copy()
                            self.move_box = box
                            self.move_goal = goal_location
                            min_plan_length = len(plan_a_b_g)
                            min_b_g_length = len(plan_b_g.plan)

    def FindShortestIntentionPath(self):        
        save_box = self.move_box
        self.move_box = None
        for box in self.boxes :
            if box != save_box :
                plan_a_b = Plan(self.location, box.location) # Plan for the agent to reach box
                agent_has_plan_to_box = plan_a_b.CreateIntentionPlan(self.location,self.location)                        
                if agent_has_plan_to_box :
                    plan_a_b.plan.reverse()                    
                    plan_a_b_g = deque()    
                    plan_a_b_g.extend(plan_a_b.plan)
                
                    goal_location = None
                    tmpQueue = PriorityQueue()
                
                    while not box.goals.empty() :
                        goal = box.goals.get()
                        goal_location = goal[1]
                        tmpQueue.put(goal)
                        if goal_location not in State.GoalDependency.keys() :                        
                            plan_b_g = Plan(box.location, goal_location) # Plan for the box to reach goal
                            box_has_plan_to_goal = plan_b_g.CreateIntentionPlan(box.location,self.location) 
                            if box_has_plan_to_goal :
                                plan_b_g.plan.reverse()
                                plan_a_b_g.extend(plan_b_g.plan)
                                self.plan1 = plan_a_b_g.copy()
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
                    agent_has_plan_to_box = True
                except Exception as ex :
                    agent_has_plan_to_box = plan_a_b.CreateBeliefPlan(agent_next_loc)                        
                    if agent_has_plan_to_box :
                        plan_a_b.plan.reverse()
                    
                plan_a_b_g = deque()
                if agent_has_plan_to_box :
                    plan_a_b_g.extend(plan_a_b.plan)                                    
                
                    goal_location = None
                    tmpQueue = PriorityQueue()
                    
                    while not box.goals.empty() :
                        goal = box.goals.get()
                        goal_location = goal[1]
                        tmpQueue.put(goal)
                        if goal_location not in State.GoalDependency.keys() and goal_location != self.move_goal :
                            break
                        else :
                            goal_location = None
                    
                    while not tmpQueue.empty() :
                        box.goals.put(tmpQueue.get())
                #only select goals that don't have dependency
                    if goal_location is not None :                    
                        plan_b_g = Plan(box.location, goal_location) # Plan for the box to reach goal
                        #if plan was found initially
                        try :
                            plan_b_g.plan = State.Plans[plan_b_g]
                            box_has_plan_to_goal = True
                        except Exception as ex :
                            box_has_plan_to_goal = plan_b_g.CreateBeliefPlan(box.location)                        
                            if box_has_plan_to_goal :
                                plan_b_g.plan.reverse()
                        
                        if box_has_plan_to_goal :
                            plan_a_b_g.extend(plan_b_g.plan)
                            #save the shortest path
                            if ((len(plan_a_b_g) == min_plan_length and len(plan_b_g.plan) < min_b_g_length)
                            or len(plan_a_b_g) < min_plan_length) :
                                self.plan2 = plan_a_b_g.copy()
                                self.next_box = box
                                self.next_goal = goal_location
                                min_plan_length = len(plan_a_b_g)
                                min_b_g_length = len(plan_b_g.plan)
    
    def DeleteRequest(self,key) :
        try :
            del(self.request[key])
        except Exception as ex :
            HandleError("delete error "+str(key)+' '+str(self)+' '+str(self.move_box))
            
    #delete box goal combinations when box is on the goal location                                
    def DeleteCells(self) :
        save_key = None
        
        #Delete the box that achieved goal
        State.BoxAt[self.move_box.letter].remove(self.move_box)
        if len(State.BoxAt[self.move_box.letter]) == 0 :
            del(State.BoxAt[self.move_box.letter])
            State.color_dict[self.color].remove(self.move_box.letter)
            if len(State.color_dict[self.color]) == 0 :
                del(State.color_dict[self.color])
        
        #Delete the goal that now has a valid box        
        State.GoalAt[self.move_box.letter].remove(self.move_goal)
        if len(State.GoalAt[self.move_box.letter]) == 0 :
            del(State.GoalAt[self.move_box.letter])
        
        #Find the goals that have dependency on the goal that has been reached
        save_keys = deque()
        for key,value in State.GoalDependency.items() :
            if self.move_goal in State.GoalDependency[key] :
                save_keys.append(key)
                
        #Delete the dependent goals from the dictionary and remove the key if there are no more values remaining
        while len(save_keys) != 0 :
            save_key = save_keys.pop() 
            State.GoalDependency[save_key].remove(self.move_goal)
            if len(State.GoalDependency[save_key]) == 0 :
                del(State.GoalDependency[save_key])
                
        self.plan1 = deque()
        self.move_box = None
        self.move_goal = None

    def MoveOtherBox(self,other_box,to_free_cells) :
        #need to reach the box in the request
        if len(self.request_plan) > 0 :
            return self.Move(self.request_plan.popleft())  #move closer to the box
        #only make plan to box if its not in the neighborhood
        
        if self.location not in State.Neighbours[other_box.location] :
            
            self.MakeBoxIntentionPlan(other_box)    #i chose only intentional plan for this situation
            if len(self.request_plan) > 0 :
                move_cell = self.request_plan.popleft()
                if  move_cell in State.FreeCells :
                    self.plan = deque()
                    return self.Move(move_cell)  #agent moves towards box
                else :
                    self.request_plan = deque() #the original plan created has non free cells
            else :
                self.DeleteRequest(other_box) #delete request, so agent can go ahead with her own plan
                return self.NoOp()  #agent couldn't make a plan
        
        else :
            #now the agent is next to box, tries push first
            push_cells = deque()
            for n in State.Neighbours[other_box.location] :
                if n in State.FreeCells :
                    if n not in to_free_cells :
                        self.DeleteRequest(other_box)
                        action = self.Push(other_box,n)
                        self.plan = deque()
                        return action
                    else :
                        push_cells.append(n)

            #agent couldn't push, tries to pull away from the first cell that she has to free
            pull_cells = deque()
            for n in State.Neighbours[self.location]:
                if n in State.FreeCells :
                    if n not in to_free_cells :
                        self.DeleteRequest(other_box)
                        action = self.Pull(other_box, n)
                        self.plan = deque()
                        return action
                    else :
                        pull_cells.append(n)

            if len(pull_cells) > 0 or len(push_cells) > 0 :
                self.plan = deque()
                self.DeleteRequest(other_box)
                if len(pull_cells) > 0 :
                    cell = pull_cells.popleft()
                    action = self.Pull(other_box, cell) #pull to any neighbour
                else :
                    cell = push_cells.popleft()
                    action = self.Push(other_box, cell) #push to any neighbour
                self.request[other_box] = to_free_cells
                return action
            else :
                self.DeleteRequest(other_box)  #box couldn't be moved .. blocked by another box (should make another request ?)

            return self.NoOp()
        
    def MoveAnotherPlace(self,to_free_cells) :
        action = self.NoOp()
        for n in State.Neighbours[self.location]:
            if n in State.FreeCells and n not in to_free_cells:
                action = self.Move(n)
                break
        self.DeleteRequest(1)
        if self.location in to_free_cells:
            self.request[1] = to_free_cells
        return action
        
    #if agent has received request, follow that first
    def ExecuteRequest(self) :
        #don't pick only the first, need to improvise .. make bidding system for example
        for key in self.request.keys():
            blocking_entity = key  # picking the first request
            to_free_cells = set()
            break

        for value in self.request.values():
            to_free_cells.update(value)

        if type(blocking_entity) is int :
            return self.MoveAnotherPlace(to_free_cells)
        else:
            return self.MoveOtherBox(blocking_entity,to_free_cells)

    def AssignRequest(self,agent,blocking_box=None) :
        assigner = self
        request = Request('assign',blocking_box,self,set(self.plan1))
        if agent not in State.Requests.keys() :
            State.Requests[agent] = list()
        State.Requests[agent].append(request)            
                
    #make a request to some agent because the current plan cannot be executed, agent could be blocked or box could be blocked        
    def MakeRequest(self,free_these_cells) :        
        pattern_box = re.compile("[A-Z]+")
        pattern_agent = re.compile("[0-9]+")

        for cell in free_these_cells :
            letter_or_num = State.current_level[cell.x][cell.y]
            if pattern_box.fullmatch(letter_or_num) is not None:
                agents,blocking_box = State.getBoxAgent(letter_or_num,cell)
                if len(agents) > 0 and blocking_box is not None :
                    for agent in agents :
                        self.AssignRequest(agent,blocking_box)                                                                        
            elif pattern_agent.fullmatch(letter_or_num) is not None:
                agent = State.getAgentAgent(letter_or_num)
                if len(agent.plan1) == 0:
                    self.AssignRequest(agent)
        
    def ExecuteDecision(self) :
        
        cell1 = self.plan.popleft()
        cell2 = self.plan[0]  
        
        #Move towards the box
        if self.move_box.location != cell1 :
            return self.Move(cell1)  
        else:
            #If next to next location is where box should be, then push
            if cell2 != self.location :
                action = self.Push(self.move_box,cell2)
                if len(self.plan) <= 1 :
                    self.DeleteCells()   #Remove goals and boxes that have reached each other 
                return action 
            else:
                #if next to next location is agent's location, then pull
                small_frontier = PriorityQueue()
                for n in State.Neighbours[self.location]:
                    if n in State.FreeCells and n != self.move_box.location :
                        small_heur = -1 * (abs(n.x - self.move_goal.x) + abs(n.y - self.move_goal.y))
                        small_frontier.put((small_heur, n))
                if not small_frontier.empty():
                    agent_to = small_frontier.get()[1]
                    action = self.Pull(self.move_box, agent_to)                            
                    if len(self.plan) <= 1 :
                        self.DeleteCells()
                    return action
                return self.NoOp()
        
    #check for requests, check for feasibility of the plan and execute 
    def CheckAndExecute(self):  
        #if no desire plan was made, then agent doesn't have more plans
        if len(self.plan1) == 0 :
            return self.NoOp()
        
        #find if any desire plan path is not free
        not_free_cells = set(self.plan1).difference(State.FreeCells)
        not_free_cells.discard(self.move_box.location)
        not_free_cells.discard(self.location)
        
        #while replanning, make intentional plan
        if len(not_free_cells) != 0 and len(self.request_plan) == 0 :            
            #save_plan= self.plan1  #save the desire plan 
            #self.plan1 = deque()            
            self.MakeCurrentIntentionPlan() #first try with chosen box and goal
            if len(self.plan1) == 0 and not State.SingleAgent :       
                self.MakeAnyIntentionPlan() #see if any plan can be made
            
            if len(self.plan1) == 0 :
                #self.plan1 = save_plan
                self.MakeRequest(not_free_cells) #make request to agent whose box blocks the current agent
                
        return self.NoOp()