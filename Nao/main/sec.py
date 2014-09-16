'''
    @author: Paul Reesman
    @contact: Arizona State University

    @todo: threading
'''
from naoqi import ALProxy 
import sys
import random

class sec():
    global ip
    ip = "10.211.16.7"
    
    def __init__(self):
        self.sonarProxy = ALProxy("ALSonar", ip, 9559)
        self.memoryProxy = ALProxy("ALMemory", ip, 9559)
        self.motionProxy = ALProxy("ALMotion", ip, 9559)
        self.speechProxy = ALProxy("ALTextToSpeech", ip, 9559)
        self.sensorProxy = ALProxy("ALSensors", ip, 9559)
        self.rpos = ALProxy("ALRobotPosture", ip, 9559)
        self.sonarProxy.subscribe("sec.py")
        self.sensorProxy.subscribe("sec.py")
        self.motionProxy.stiffnessInterpolation("Body", 0, 1)
        self.rpos.goToPosture("Stand", 1.0, 0)
        self.motionProxy.moveInit()
    
    def main(self):
        self.moveForward()
        self.obstacleDetection()
        return
        
    def moveForward(self):
        self.motionProxy.moveToward(.5, 0, -.0085)
        
    def obstacleDetection(self):
        while(True):
            front = self.memoryProxy.getData("FrontTactilTouched")
            middle = self.memoryProxy.getData("MiddleTactilTouched")
            rear = self.memoryProxy.getData("RearTactilTouched")
            left = self.memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
            right = self.memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
            self.touched(front, middle, rear)
            self.footBumper()
            #self.handBumper()
            self.leftorright(left, right)
        return
            
    def leftorright(self, left, right):
        if left == right:
            if left > .25 and left < .3:
                self.motionProxy.moveToward(0, 0, 0)
                self.decision(left, right)
                self.motionProxy.moveToward(.5, 0, -.0085)
            return
        if left > right:
            if right > .25 and right < .3:
                self.motionProxy.moveToward(0, 0, 0)
                self.motionProxy.moveTo(0, 0, .5)
                self.motionProxy.moveToward(.5, 0, -.0085)
            return
        if left < right:
            if left > .25 and left < .3:
                self.motionProxy.moveToward(0, 0, 0)
                self.motionProxy.moveTo(0, 0, -.5)
                self.motionProxy.moveToward(.5, 0, -.0085)
            return
    
    def touched(self, front, middle, rear):
        if front == 1 or middle == 1 or rear == 1:
            self.motionProxy.moveToward(0, 0, 0)
            self.motionProxy.rest()
            sys.exit()
    
    def decision(self, left, right):
        self.motionProxy.moveTo(0, 0, .5)
        l1 = self.memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        self.motionProxy.moveTo(0, 0, -1)
        r2 = self.memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        self.motionProxy.moveTo(0, 0, .5)
        if l1 > r2:
            self.motionProxy(0, 0, .5)
            return
        if l1 < r2:
            self.motionProxy(0, 0, -.5)
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
    
    def handBumper(self):
        rightHand = self.memoryProxy.getData("HandRightBackTouched")
        leftHand = self.memoryProxy.getData("HandLeftBackTouched")
        if rightHand == 1:
            self.motionProxy.moveToward(0, 0, 0)
            self.motionProxy.moveTo(0, .1, 0)
            self.motionProxy.moveToward(.5, 0, -.0085)
            return
        if leftHand == 1:
            self.motionProxy.moveToward(0, 0, 0)
            self.motionProxy.moveTo(0, -.1, 0)
            self.motionProxy.moveToward(.5, 0, -.0085)
            return