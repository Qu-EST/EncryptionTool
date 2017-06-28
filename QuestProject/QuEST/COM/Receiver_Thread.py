'''
Created on Apr 1, 2017

@author: jee11
'''

from threading import Thread, Lock
from queue import Queue
from _overlapped import NULL
from _socket import socket, timeout
import time, threading
from QuEST.EncryptorData import EncryptorData
class Receiver_Thread(Thread):
    '''
    classdocs
    '''
    

    def __init__(self,display_received=Queue(0),received=Queue(0),rcv_socket=socket,lock=Lock()):
        '''
        Constructor
        '''
        self.switch="True"
        self.alldata=EncryptorData()
        self.received=received
        self.rcv_socket=rcv_socket
        rcv_socket.settimeout(1)
        self.lock=lock
        self.display_received=display_received
        Thread.__init__(self)
        
    def run(self):
#         try:
        self.receive()
#         except ConnectionResetError:
#             print("connection reset error, disconnecting")
#             threading.Thread(target=self.alldata.ui.setting_frame.disconnect.invoke).start()
#     
    def receive(self):
        while(self.switch=="True"):
            #print("printing the receiver switch value")
            #print(self.switch)
            pass
            #self.lock.acquire()
            try:
                bytedata=self.rcv_socket.recv(1024)
            except timeout:
                pass#print("socket timeout exception")
            except ConnectionResetError:
                print("connection reset error, disconnecting")
                threading.Thread(target=self.alldata.ui.setting_frame.disconnect.invoke).start()
            except OSError as e:
                print("From received processor. got the error:{} hence disconnecting".format(e))
                threading.Thread(target=self.alldata.ui.setting_frame.disconnect.invoke).start()
            else:
                print(b'recieved: '+ bytedata)
                if(bytedata==b''): 
                    threading.Thread(target=self.alldata.ui.setting_frame.disconnect.invoke).start()
                else:
                    try:
                        stringdata=bytedata.decode('utf-8')
                    except:
                        pass
                        stringdata=bytedata
                    finally:
                        pass
                    #print("Received: "+stringdata)
                    self.received.put(bytedata)
                    self.display_received.put(stringdata)
                    #self.lock.release()
                    #time.sleep(0.25)
    
    def off(self):
        print("offing the receiver thread")
        self.switch="False" 
        print("receiver thread is offed")       
                
