'''
Created on Apr 21, 2017

@author: jee11
'''
from threading import Thread
from queue import Queue
class KeyHasher(Thread):
    
    '''
    classdocs
    '''


    def __init__(self, alldata ):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.goodut=alldata.good_ut
        self.hash_queue=alldata.hash_queue
        self.ut=alldata.ut
        self.send_ut=alldata.good_utsend
        self.hashed_key=alldata.key
        self.save_data=alldata.save_data
        self.counter=0
        self.FORCESTOP=83
        self.alldata=alldata
        
    def run(self):
        self.hasher()
        
    def hasher(self):
        while(1):
            if(~self.hash_queue.empty()):
                #self.key, self.value=self.decompose(self.hash_queue.get())
                self.value=float(self.hash_queue.get())
                if(self.value>0):
                    self.counter=self.counter+1
                elif(self.value==0):
                    self.counter=0
                    self.alldata.key.clear()
                    self.alldata.good_utsend=Queue(0)
                 
                
                self.data=str(self.counter) +" "+ str(self.value)
                self.ut.put(self.data)
                self.save_data.put(self.data)
                if((self.value>0) and (self.value<self.FORCESTOP)):
                    self.goodut.put(self.data)
                    self.alldata.good_utsend.put(self.data)
                    temp_key={str(self.counter):int(self.value)}
                    self.alldata.key.update(temp_key)
                    
    def decompose(self,data_string):
        key_value=data_string.partition(" ")
        key=key_value[0]
        string_value=key_value[2].strip(" \r\n")
        value=float(string_value)
        return key, value            
        