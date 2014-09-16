'''
Created on Jul 11, 2013
Updated on Aug 20, 2013

@author: Paul Reesman

[[Objects True/False 1/0, [Objects]], [Events True/False 1/0, [Events]], [Goal True/False 1/0, [Goal]]]
[[Current Mark], Previous Mark, [List of all Marks]]
'''

from naoqi import ALProxy 
from planner_voice import planner_voice
import sys
import random
import time
import Queue
import threading
import math
import almath

class planner_move(object):
    global mark
    mark = []
    def __init__(self, ip):
        self.ears = planner_voice()
        self.sonarProxy = ALProxy("ALSonar", ip, 9559)
        self.memoryProxy = ALProxy("ALMemory", ip, 9559)
        self.motionProxy = ALProxy("ALMotion", ip, 9559)
        self.speechProxy = ALProxy("ALTextToSpeech", ip, 9559)
        self.sensorProxy = ALProxy("ALSensors", ip, 9559)
        #self.compassProxy = ALProxy("ALVisualCompass", ip, 9559)
        self.markProxy = ALProxy("ALLandMarkDetection", ip, 9559)
        self.rpos = ALProxy("ALRobotPosture", ip, 9559)
        self.sonarProxy.subscribe("planner_move.py")
        self.sensorProxy.subscribe("planner_move.py")
        #self.compassProxy.subscribe("planner_move.py")
        self.markProxy.subscribe("planner_move.py", 500, 0.0)
        self.motionProxy.stiffnessInterpolation("Body", 0, 1)
        self.rpos.goToPosture("Stand", 1.0, 0)
        self.motionProxy.moveInit()
        self.queue = Queue.Queue()
        thread = threading.Thread(group = None, target = self.ears.run, name = 'thread1', args = (ip, self.queue), kwargs = {})
        thread.daemon = True
        thread.start()
    
    def main(self):
        self.moveForward()
        dataStructure = self.obstacleDetection()
        return dataStructure
        
    def moveForward(self):
        self.motionProxy.moveToward(.5, .02, -.04)
        return
        
    def obstacleDetection(self):
        while(True):
            front = self.memoryProxy.getData("FrontTactilTouched")
            middle = self.memoryProxy.getData("MiddleTactilTouched")
            rear = self.memoryProxy.getData("RearTactilTouched")
            left = self.memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
            right = self.memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
            #direction = self.memoryProxy.getData("VisualCompass/Deviation")
            detection = self.memoryProxy.getData("LandmarkDetected", 0)
            self.touched(front, middle, rear)
            dataStructure = self.landmark(detection)
            if not self.queue.empty():
                dS = self.commanded()
                if dS:
                    if dataStructure == []:
                        dataStructure = dS
                    else:
                        dataStructure[0] = dS[0]
            if not dataStructure == []:
                self.motionProxy.moveToward(0, 0, 0)
                return dataStructure
            self.footBumper()
            self.leftorright(left, right)
            #self.compass(direction)
        return
            
    def leftorright(self, left, right):
        if left == right:
            if left > .25 and left < .3:
                self.motionProxy.moveToward(0, 0, 0)
                self.decision(left, right)
                self.motionProxy.moveToward(.5, .02, -.03)
            return
        if left > right:
            if right > .25 and right < .3:
                self.motionProxy.moveToward(0, 0, 0)
                self.motionProxy.moveTo(0, 0, .5)
                self.motionProxy.moveToward(.5, .02, -.03)
            return
        if left < right:
            if left > .25 and left < .3:
                self.motionProxy.moveToward(0, 0, 0)
                self.motionProxy.moveTo(0, 0, -.5)
                self.motionProxy.moveToward(.5, .02, -.03)
            return
        
    def turn(self, radians):
        self.motionProxy.moveToward(0, 0, 0)
        self.motionProxy.moveTo(0, 0, radians)
        return
    
    def touched(self, front, middle, rear):
        if front == 1 or middle == 1 or rear == 1:
            self.motionProxy.moveToward(0, 0, 0)
            time.sleep(1)
            self.motionProxy.rest()
            sys.exit()
    
    def decision(self, left, right):
        self.motionProxy.moveTo(0, 0, .5)
        l1 = self.memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        self.motionProxy.moveTo(0, 0, -1)
        r2 = self.memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        self.motionProxy.moveTo(0, 0, .5)
        if l1 > r2:
            self.motionProxy.moveTo(0, 0, .5)
            return
        if l1 < r2:
            self.motionProxy.moveTo(0, 0, -.5)
            return
        else:
            randomBinary = random.randint(0, 1)
            if randomBinary == 0:
                self.motionProxy.moveTo(0, 0, .5)
            else:
                self.motionProxy.moveTo(0, 0, -.5)
            return
    
    def footBumper(self):
        rightBumper = self.memoryProxy.getData("RightBumperPressed")
        leftBumper = self.memoryProxy.getData("LeftBumperPressed")
        if rightBumper == 1:
            self.motionProxy.moveToward(0, 0, 0)
            self.motionProxy.moveTo(-.1, 0, .5)
            self.motionProxy.moveTo(0, 0, .5)
            return
        if leftBumper == 1:
            self.motionProxy.moveToward(0, 0, 0)
            self.motionProxy.moveTo(-.1, 0, -.5)
            self.motionProxy.moveTo(0, 0, -.5)
            return
        
    def compass(self, deviation):
        if deviation[0][0] > .3 or deviation[0][0] < -.3:
            self.motionProxy.moveToward(0, 0, 0)
            self.motionProxy.moveTo(0, 0, -deviation[0][0])
            self.motionProxy.moveToward(.5, .02, -.03)
        if deviation[0][1] > .3 or deviation[0][1] < -.3:
            self.motionProxy.moveToward(0, 0, 0)
            self.motionProxy.moveTo(0, 0, -deviation[0][1])
            self.motionProxy.moveToward(.5, .02, -.03)
        return
    
    def landmark(self, detection):
        if detection == []:
            return []
        elif (detection[1][0][0][3] and detection[1][0][0][4]) > .14:
            if int(str(detection[1][0][1]).strip('[]')) == mark[0]:
                #return ["event", detection[1][0][1]]
                return [[0, []], [1, [int(str(detection[1][0][1]).strip('[]'))]], [1, [int(str(detection[1][0][1]).strip('[]'))]]]
            elif int(str(detection[1][0][1]).strip('[]')) == mark[1]:
                    return []
            elif int(str(detection[1][0][1]).strip('[]')) in mark[2]:
                return [[0, []], [1, [int(str(detection[1][0][1]).strip('[]'))]], [1, [int(str(detection[1][0][1]).strip('[]'))]]]
        else:
            self.landmarkYmovement(detection)
            return []
    
    def landmarkYmovement(self, detection):
        zCamera = detection[1][0][0][1]
        yCamera = detection[1][0][0][2]
        angularSize = detection[1][0][0][3]
        distance = .06 / ( 2 * math.tan( angularSize / 2))
        transform = self.motionProxy.getTransform("CameraTop", 2, True)
        transformList = almath.vectorFloat(transform)
        robotToCamera = almath.Transform(transformList)
        cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, yCamera, zCamera)
        cameraToLandmarkTranslationTransform = almath.Transform(distance, 0, 0)
        robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform *cameraToLandmarkTranslationTransform
        if math.fabs(robotToLandmark.r2_c4) > .2 and math.fabs(robotToLandmark.r2_c4) < .45:
            self.motionProxy.moveToward(0, 0, 0)
            self.motionProxy.moveTo(0, robotToLandmark.r2_c4, 0)
            firstDetection = robotToLandmark.r2_c4
            secondDetection = self.memoryProxy.getData("LandmarkDetected", 0)
            if not secondDetection == []:
                zCamera = secondDetection[1][0][0][1]
                yCamera = secondDetection[1][0][0][2]
                angularSize = secondDetection[1][0][0][3]
                distance = .06 / ( 2 * math.tan( angularSize / 2))
                transform = self.motionProxy.getTransform("CameraTop", 2, True)
                transformList = almath.vectorFloat(transform)
                robotToCamera = almath.Transform(transformList)
                cameraToLandmarkRotationTransform = almath.Transform_from3DRotation(0, yCamera, zCamera)
                cameraToLandmarkTranslationTransform = almath.Transform(distance, 0, 0)
                robotToLandmark = robotToCamera * cameraToLandmarkRotationTransform *cameraToLandmarkTranslationTransform
                if not robotToLandmark < math.fabs(.2):
                    if robotToLandmark.r2_c4 < 0:
                        self.motionProxy.moveTo(0, 0, ((robotToLandmark.r2_c4 / 1.06) * 5))
                    else:
                        self.motionProxy.moveTo(0, 0, -((robotToLandmark.r2_c4 / 1.06) * 5))
            else:
                if firstDetection < 0:
                    self.motionProxy.moveTo(0, 0, ((firstDetection / 1.06) * 5))
                else:
                    self.motionProxy.moveTo(0, 0, -((firstDetection / 1.06) * 5))
            self.motionProxy.moveToward(.5, .02, -.03)
        
    def updateMark(self, update):
        if mark[0] == update:
            return
        mark[1] = mark[0]
        mark[0] = update
        return
        
    def appendMark(self, update):
        mark.append(update)
        return
        
    def returnMark(self, zeroORone):
        return mark[zeroORone]
        
    def movement(self, way):
        if way == "stop":
            self.motionProxy.moveToward(0, 0, 0)
            return 1
        elif way == "left":
            self.motionProxy.moveToward(0, 0, 0)
            self.motionProxy.moveTo(0, 0, 1.0)
            self.motionProxy.moveToward(.5, .02, -.03)
            return 1
        elif way == "right":
            self.motionProxy.moveToward(0, 0, 0)
            self.motionProxy.moveTo(0, 0, -1.0)
            self.motionProxy.moveToward(.5, .02, -.03)
            return 1
        elif way == "sit":
            self.motionProxy.moveToward(0, 0, 0)
            self.rpos.goToPosture("Sit", 1.0, 0)
            return 1
        elif way == "forward":
            self.moveForward()
            return 1
        elif way == "stand":
            self.rpos.goToPosture("Stand", 1.0, 0)
        else:
            return 0
        
    def commanded(self):
        obj = self.queue.get()
        print "************************************************************************"
        print "Command Received: " + obj
        print "************************************************************************"
        worked = self.movement(obj)
        if worked == 1:
            return None
        else:
            return [[1, [obj]], [0, []], [0, []]]
        
    def stopper(self):
        self.ears.stop()