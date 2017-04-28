'''
Created on Apr 21, 2017

@author: jee11
'''
from threading import Thread, Lock
from queue import Queue

class ReceivedProcessor(Thread):
    '''
    classdocs
    '''


    def __init__(self, alldata, lock=Lock()):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.received=alldata.received_data
        self.lock=lock
        self.key=alldata.key
        self.goodkey=alldata.goodkey
        self.send_queue=alldata.send_data
        self.xor_switch="True"
        self.message=alldata.displaymessage
        self.processor_switch=1
        
    def run(self):
        self.process()
        
    def process(self):
        while(self.processor_switch):
            if(~self.received.empty()):
                bytedata=self.received.get()
                data=bytedata.decode('utf-8')
                command=data.partition(" ")
                if(command[0]=="goodut"):
                    pass
                    self.process_goodut(command[2])
                elif(command[0]=="stop"):
                    self.process_stop()
                elif(command[0]=="XOR"):
                    if(self.xor_switch=="true"):
                        self.process_CRC(command[2])
                elif(command[0]=="message"):
                    self.process_message(command[2])
    
    def process_goodut(self, mygooduts):
        decom=mygooduts.partition(" ")
        self.goodkey.append([decom[0],decom[2]])
    def process_stop(self):
        self.xor_switch="False"
    def process_CRC(self,mycrcdata):
        decom=mycrcdata.partition(" ")
        key1=decom[0]
        decom=decom[2].partition(" ")
        key2=decom[0]
        xor=int(decom[2].strip(" "))
        if(self.key[key1]^self.key[key2]==xor):
            self.goodkey.append([key1,key2])
            send_data="goodut " + key1+ " "+ key2
            self.send_queue.put(send_data)
            
        
    def process_message(self,enc_message):
        self.message.put("Sender: " + enc_message) 
        
    def off(self):
        self.processor_switch=0          
        
        