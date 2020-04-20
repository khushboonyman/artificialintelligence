# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:06:41 2020

@author: Bruger
"""

     def Push(self,agtfrom,box,boxfrom,boxto):
        if ( self.location == agtfrom and agtfrom!=boxto and box.location == boxfrom and boxfrom != boxto and
        boxto.free() and not agtfrom.free() and agtfrom.neighbor(boxfrom) and boxfrom.neighbor(boxto) and
        self.color == box.color) :
            self.location = boxfrom
            boxfrom.assign(self.number)
            agtfrom.assign(' ')
            box.location = boxto
            boxto.assign(box.letter)
            move_dir_agent = TranslateToDir(agtfrom,boxfrom)
            move_dir_box = TranslateToDir(boxfrom,boxto)
            return 'Push('+move_dir_agent+','+move_dir_box+')'
        return 'NoOp'

        def Pull(self,agtfrom,agtto,box,boxfrom):
        if ( self.location == agtfrom and agtfrom!=agtto and box.location == boxfrom and boxfrom != agtfrom and
        agtto.free() and not boxfrom.free() and agtfrom.neighbor(agtto) and boxfrom.neighbor(agtfrom) and
        self.color == box.color) :
            self.location = agtto
            agtto.assign(self.number)
            box.location = agtfrom
            agtfrom.assign(box.letter)
            boxfrom.assign(' ')
            move_dir_agent = TranslateToDir(agtfrom,agtto)
            curr_dir_box = TranslateToDir(agtfrom,boxfrom)
            return 'Pull('+move_dir_agent+','+curr_dir_box+')'
        return 'NoOp'

        def Move(self,agtfrom,agtto):
        if self.location == agtfrom and agtfrom!=agtto and agtto.free() and not agtfrom.free() and agtfrom.neighbor(agtto) :
            self.location = agtto
            agtfrom.assign(' ')
            agtto.assign(self.number)
            move_dir_agent = TranslateToDir(agtfrom,agtto)
            return 'Move('+move_dir_agent+')'
        return 'NoOp'
        
            