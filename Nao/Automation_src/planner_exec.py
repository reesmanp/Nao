'''
Created on Jul 9, 2013
Updated on Aug 7, 2013

@author: Paul Reesman


DEMOS:
1: navigation with NaoMarks hard coded
2: navigation with human interaction
3: navigation with miscellaneous obstacles for updates


Data Structures:
[[Current Mark], Previous Mark, [List of all Marks]]
[[Objects True/False 1/0, [Objects]], [Events True/False 1/0, [Events]], [Goal True/False 1/0, [Goal]]]
'''

import time
from planner_move import planner_move
from planner_parser import planner_parser
from planner_replan import planner_replan
from naoMarks import naoMarks

class planner_exec(object):
    global IP
    IP = "10.141.161.23"
    
    def __init__(self):
        self.operation = planner_move(IP)
        self.sapa = planner_replan()
        self.parser = planner_parser()
        self.marks = naoMarks()
        
    def main(self):
        try:
            plan = self.sapa.runJar()
            instruction_list = self.parser.parse(plan)
            currentMark = self.marks.naoMarkID(instruction_list)
            self.operation.appendMark(currentMark)
            self.operation.appendMark(114)
            self.operation.appendMark(self.marks.getNumbers())
        #thread.start_new_thread(self.ears.run, (IP, self.queue))
            while True:
                dataStructure = self.operation.main()
                send = self.marks.decipher(dataStructure, self.operation.returnMark(0), self.operation.returnMark(1))
                plan = self.sapa.writeUpdate(send)
                instruction_list = self.parser.parse(plan)
                currentMark = self.marks.naoMarkID(instruction_list)
                if not currentMark:
                    print "******All Goals Complete******"
                    self.operation.touched(1, 1, 1)
                self.operation.updateMark(currentMark)
                if self.marks.naoMark(self.operation.returnMark(1)):
                    if self.marks.naoMark(self.operation.returnMark(1))[2] == "left":
                        self.operation.turn(.9)
                    if self.marks.naoMark(self.operation.returnMark(1))[2] == "right":
                        self.operation.turn(-.9)
                    if self.marks.naoMark(self.operation.returnMark(1))[2] == "forward":
                        pass
        finally:
            self.operation.stopper()
            time.sleep(1)
    
    
h = planner_exec()
h.main()