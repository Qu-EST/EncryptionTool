'''
Created on Apr 1, 2017

@author: jee11
'''
from threading import Thread
from threading import Lock
from queue import Queue
from _overlapped import NULL
from _socket import socket
class Sender_Thread(Thread):
    '''
    classdocs
    '''
    

    def __init__(self,display_sent=Queue(0),tosend=Queue(0),send_socket=socket,lock=Lock()):
        '''
        Constructor
        '''
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
            if (~self.tosend.empty()):
                message=self.tosend.get()
                #message=str(data)
                print("Sending: "+message)
                self.display_sent.put(message)
                self.send_socket.send(message.encode('utf-8'))
            #self.lock.release()
                
    def off(self):
        self.sender_switch="False"            
            
        
        
        
        