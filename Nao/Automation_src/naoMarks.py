'''
Created on Jul 31, 2013
Updated on Aug 16, 2013

@author: Paul Reesman

[[Objects True/False 1/0, [Objects]], [Events True/False 1/0, [Events]], [Goal True/False 1/0, [Goal]]]

'''

class naoMarks(object):
    
    def __init__(self):
        global ID, revID
        ID = {"backhall": 114, "righthall": 85, "fronthall": 112, "lefthall": 108, "brseg": 119, "frseg": 107, "flseg": 80, "blseg": 84}
        revID = {114: "backhall", 85: "righthall", 112: "fronthall", 108: "lefthall", 119: "brseg", 107: "frseg", 80: "flseg", 84: "blseg"}
        self.Tcount = 0
        self.Ccount = 0
        
    def decipher(self, dataStructure, current, previous):
        textToAdd = []
        eventText = []
        goalText = []
        textToAdd.append("(:update  :objects ")
        if dataStructure and dataStructure[0][0] == 1:
            dataStructure[1][0] = 1
            for e in dataStructure[0][1]:
                if e == "trash":
                    self.Tcount = self.Tcount + 1
                    textToAdd.append("trash" + str(self.Tcount) + " - trashcan ")
                    dataStructure[1][1].append("trash" + str(self.Tcount) + " ")
                elif e == "chair":
                    self.Ccount = self.Ccount + 1
                    textToAdd.append("chair" + str(self.Ccount) + " - chair ")
                    dataStructure[1][1].append("chair" + str(self.Ccount) + " ")
        textToAdd.append(" :events ")
        if dataStructure and dataStructure[1][0] == 1:
            for e in dataStructure[1][1]:
                if "trash" in dataStructure[0][1] or "chair" in dataStructure[0][1]:
                    eventText.append(e + " at " + str(revID[previous]))
                    textToAdd.append("(at " + e + " " + str(revID[previous]) + ") ")
                else:
                    eventText.append("rob at " + str(revID[e]))
                    textToAdd.append("(at rob " + str(revID[e]) + ") ")
                    if self.naoMark(current):
                        textToAdd.append(self.naoMark(current)[0])
        textToAdd.append(" :goal (and")
        if dataStructure and dataStructure[2][0] == 1:
            for e in dataStructure[2][1]:
                if self.naoMark(current):
                    goalText.append("rob at " + revID[current])
                    textToAdd.append("(at rob " + revID[self.naoMark(current)[3]] + ") ")
                    textToAdd.append(self.naoMark(current)[1])
        textToAdd.append(") :now 0.0)")
        print '************************************************************************'
        print '************************************************************************'
        if dataStructure:
            print "Obstacles Found: " + str(dataStructure[0][1])
        else:
            print "Obstacles Found: []"
        print "Events Occurred: " + str(eventText)
        print "Goals Achieved: " + str(goalText)
        print '************************************************************************'
        print '************************************************************************\n\n'
        text = ''
        for e in textToAdd:
            text = text + e
        toPrint = ' '
        print "\nUpdate Text:"
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
        return text
        
    def naoMarkID(self, ilist):
        try:
            return ID[ilist[0][3]]
        except AttributeError:
            return None
        except IndexError:
            return None
        
    def naoMark(self, naoNum):
        if naoNum == 114:
            return
        if naoNum == 119:
            return ["(connected " + revID[119] + " " + revID[85] + ")", "(at rob " + revID[119] + ") - soft", "left", 85]
        if naoNum == 112:
            return [None, "(at rob " + revID[112] + ") - soft", "goal"]
        if naoNum == 85:
            return ["(connected " + revID[85] + " " + revID[107] + ")", "(at rob " + revID[85] + ") - soft", "forward", 107]
        if naoNum == 107:
            return ["(connected " + revID[107] + " " + revID[112] + ")", "(at rob " + revID[107] + ") - soft", "left", 112]
    
    def getNumbers(self):
        return ID.values()
    
    def getKey(self):
        return revID.values()