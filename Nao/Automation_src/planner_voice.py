'''
Created on Jul 24, 2013
Updated on Aug 15, 2013

@author: Paul Reesman

[[Objects True/False 1/0, [Objects]], [Events True/False 1/0, [Events]], [Goal True/False 1/0, [Goal]]]

'''

from naoqi import ALProxy
import threading
import time

class planner_voice(threading.Thread):
    global vocabulary
    vocabulary = ["stop", "stand", "forward", "left", "right", "sit", "chair", "trash"]
        
    def run(self, IP, q):
        try:
            self.stopper = False
            global voiceProxy, memProxy
            self.voiceProxy = ALProxy("ALSpeechRecognition", IP, 9559)
            self.memProxy = ALProxy("ALMemory", IP, 9559)
            self.voiceProxy.setLanguage("English")
            if "Hello.java" in self.voiceProxy.getSubscribersInfo():
                self.voiceProxy.unsubscribe("Hello.java")
            if "planner_voice.py" in self.voiceProxy.getSubscribersInfo():
                self.voiceProxy.unsubscribe("planner_voice.py")
            self.voiceProxy.setWordListAsVocabulary(vocabulary)
            self.voiceProxy.subscribe("planner_voice.py")
            while not self.stopper:
                self.voices(q)
        except Exception, e:
            print e
        finally:
            print "System Shutting Down..."
            self.voiceProxy.unsubscribe("planner_voice.py")
            #self.voiceProxy.unsubscribe("SayHello.java")
            return
        
    def voices(self, q):
        try:
            if self.memProxy.getData("SpeechDetected"):
                time.sleep(1)
                if self.memProxy.getData("WordRecognized")[1] > .5:
                    mystr = self.memProxy.getData("WordRecognized")[0]
                    q.put(mystr)
                    time.sleep(3)
                    #self.memProxy.removeData("WordRecognized")
                    #self.memProxy.removeData("SpeechDetected")
        except StandardError:
            pass
        
    def stop(self):
        self.stopper = True
                    