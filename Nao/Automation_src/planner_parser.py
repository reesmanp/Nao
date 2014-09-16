'''
Created on Jul 9, 2013
Updated on Aug 5, 2013

@author: Paul Reesman

@param plan: A string copied from the output of the SapaReplan planner

Finds the phrase 'getready' and 'EOP' and sends their indexes to low and high respectfully
Copies only the text between 'getready' and 'EOP' into instruct_plan
Loops through remaining code parsing the text between the '(' and ')'
Creates a list containing the parsed text
Appends the list into instruct_list
Returns the list: instruct_list
'''
class planner_parser(object):
    def parse(self, plan):
        instruct_list = []
                
        low = plan.find("getready")
        high = plan.find("EOP")
        instruct_plan = plan[low:high]
                
        while not high == -1:
            low = instruct_plan.find("(") + 1
            high = instruct_plan.find(")", low + 1)
            if high is not -1:
                instruct_list.append(instruct_plan[low:high].split(" "))
                instruct_plan = instruct_plan[high:]
        
        print instruct_list
        return instruct_list
    