'''
Created on Apr 21, 2017

@author: jee11
'''
from threading import Thread, Lock
from queue import Queue
import time

class SendProcessor(Thread):
    '''
    classdocs
    '''


    def __init__(self, alldata):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.good_ut=alldata.good_utsend
        self.send_queue=alldata.send_data
        #self.lock=lock
        #self.key1, self.key2, self.send_data=""
        #self.value1, self.value2, self.xor = 0
        self.switch="True"
        
        
        
        
        
    def run(self):
        self.send()
        
    def send(self):
        while(self.switch=="True"):
            print("inside send")
            if(~self.good_ut.empty()):
                self.key1,self.value1 = self.dividor(self.good_ut.get())
                time.sleep(0.25)
                if(~self.good_ut.empty()):
                    self.key2,self.value2 = self.dividor(self.good_ut.get())
                    self.xor=self.value1^self.value2
                    self.send_data="XOR " + self.key1 + " " + self.key2 + " " + str(self.xor)
                    self.send_queue.put(self.send_data)
            
            
    def dividor(self,data):
        key_value=data.partition(" ")
        key=key_value[0]
        value=int(float(key_value[2]))
        return key, value
    
    def off(self):
        self.swich="False"
            
        