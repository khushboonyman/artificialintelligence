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



########################TESTING##################################

    
    def MakePlan(self) :
        if self.request is not None :
            self.MakeRequestPlan()
            return True
        
        letters = FindLetters(self.color)
        selected_goal_location = None
        selected_box = None
        
        for letter in letters :
            for goal in State.GoalAt[letter] :
                if goal in State.GoalLocations and goal not in State.GoalDependency.keys() : #Find goal to achieve
                    selected_goal_location = goal
        
                    
    
    def Execute(self) :
        if self.request is not None :
            self.MakeRequestPlan()
        
        if len(self.plan_to_execute) == 0 :
            return no_action

       
                        