'''
Created on Apr 1, 2017

@author: jee11
'''
from threading import Thread
from threading import Lock
from queue import Queue, Empty
from _overlapped import NULL
from _socket import socket
class Sender_Thread(Thread):
    '''
    classdocs
    '''
    

    def __init__(self,alldata,display_sent=Queue(0),tosend=Queue(0),send_socket=socket,lock=Lock()):
        '''
        Constructor
        '''
        self.alldata=alldata
        self.sender_switch="True"
        self.send_socket=send_socket
        self.tosend=tosend
        self.lock=lock
        self.display_sent=display_sent
        Thread.__init__(self)
        
    def run(self):
        pass
        self.send()
    
    def send(self):    
        while(self.sender_switch=="True"):
            #self.lock.acquire()
            pass
            try:
                message=self.tosend.get(timeout=1)
                #message=str(data)
                #print("Sending: "+message)
            except Empty: pass#print("timeout from sender queue")
            else:
                self.display_sent.put(message)
                if(type(message)==type("")):
                    self.send_socket.send(message.encode('utf-8'))
                else:
                    print(message)
                    self.send_socket.send(message)
            #self.lock.release()
                
    def off(self):
        self.sender_switch="False"            
            
        
        
        
        