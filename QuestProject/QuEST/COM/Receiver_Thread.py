'''
Created on Apr 1, 2017

@author: jee11
'''
from threading import Thread, Lock
from queue import Queue
from _overlapped import NULL
from _socket import socket
import time
class Receiver_Thread(Thread):
    '''
    classdocs
    '''
    

    def __init__(self,display_received=Queue(0),received=Queue(0),rcv_socket=socket,lock=Lock()):
        '''
        Constructor
        '''
        self.switch="True"
        self.received=received
        self.rcv_socket=rcv_socket
        self.lock=lock
        self.display_received=display_received
        Thread.__init__(self)
        
    def run(self):
        pass
        self.receive()
    
    def receive(self):
        while(self.switch=="True"):
            pass
            #self.lock.acquire()
            bytedata=self.rcv_socket.recv(1024)
            stringdata=bytedata.decode('utf-8')
            print("Received: "+stringdata)
            self.received.put(bytedata)
            self.display_received.put(stringdata)
            #self.lock.release()
            #time.sleep(0.25)
    
    def off(self):
        self.switch="False"        
                