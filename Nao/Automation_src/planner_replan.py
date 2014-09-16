'''
Created on Jul 10, 2013
Updated on Aug 5, 2013

@author: Paul Reesman
'''

from subprocess import Popen, PIPE

class planner_replan(object):
    global k, output
    output = ["java", "-jar", "C:\Users\Paul\Documents\PDDL\SapaReplan.jar", "C:\Users\Paul\Documents\PDDL\AILab2.pddl", "C:\Users\Paul\Documents\PDDL\CircleLab3.pddl"]
    
    def __init__(self):
        global plan
        plan = Popen(output, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    
    def writePDDL(self, tta):
        f = open("CircleLab.pddl", "w+")
        lines = f.read()
        f.truncate()
        low = lines.find("rob rob")
        lowLines = lines[:low]
        lowLines = lowLines + tta
        high = len(lowLines)
        highLines = lines[high:]
        lines = lowLines + highLines
        f.write(lines)
        f.close()
        self.runJar()
        
    def writeUpdate(self, text):
        plan.stdin.write(text)
        phrase = ''
        while phrase.find("EOP") == -1:
            phrase = phrase + plan.stdout.readline()
        return phrase
        
    def runJar(self):
        f = open("C:\Users\Paul\Documents\PDDL\CircleLab3.pddl", "r")
        text = f.read()
        toPrint = ' '
        print "Problem PDDL File: CircleLab3.pddl"
        print '************************************************************************'
        for e in text:
            if e == ')':
                toPrint = toPrint + e + '\n'
            else:
                if len(toPrint) > 2:
                    if toPrint[-2] == ')':
                        if e == '\n':
                            continue
                toPrint = toPrint + e
        print toPrint
        print '************************************************************************'
        phrase = ''
        while phrase.find("EOP") == -1:
            phrase = phrase + plan.stdout.readline()
        return phrase
        