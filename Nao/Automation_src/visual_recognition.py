'''
Created on Jul 12, 2013

@author: Paul Reesman
'''

from naoqi import *

class visual_recognition():
    global obstacles
    obstacles = []
    
    def __init__(self, ip):
        memoryProxy = ALProxy("ALMemory", ip, 9559)
        memoryProxy.subscribeToEvent("PictureDetected", "visual_recognition.py", "obstacle_detection")
        
    
    def obstacle_detection(self):
        return