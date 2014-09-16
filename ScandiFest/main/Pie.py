'''
Created on Sep 15, 2014

@author: Paul Reesman
'''

class Pie(object):
    '''
    Pie class
    '''

    def __init__(self, name):
        '''
        Sets the cost of the pie to 1
        Sets the name of the pie
        '''
        self.cost = 1
        self.name = name
    
    def __str__(self):
        return str(self.name)
