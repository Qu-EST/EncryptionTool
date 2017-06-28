'''
Created on Apr 1, 2017

@author: jee11
'''
import socket
from threading import Thread
class My_TCP():
    '''
    My_TCP will be used to create a server or client socket according to the type mentioned while calling the getter method.
    (will be converted to the singleton class)
    '''


    def __init__(self, ip="127.0.0.1", port=5005, con_type="client"):
        '''
        Constructor
        if the type is client, then create a socket object of client and call the connect
        or if the type is server, then create a server socket object, listen and accept the server
        '''
        #self.socket()
        if con_type=="client":
            self.my_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.my_socket.connect((ip,port))
            print("client\n")
            print(self.my_socket)
        elif con_type=="server":
            self.serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serversocket.bind((ip,port))
            print("server\n")
            print(self.serversocket)
            self.serversocket.listen(1)
            print("creating listening thread")
            self.my_socket,addr=self.serversocket.accept()
            print(addr)
            #accept_thread=Thread(target=self.my_socket.accept(),args=())
            #print("thread created")
            #accept_thread.setDaemon(True)
            #print("starting to listen from thread")
            #accept_thread.start()
            print("connected")
            self.serversocket.close()
        
    @staticmethod
    def socket_getter(ip="127.0.0.1",port=5005,con_type="client"):
        '''
        this will be getter method for the to be singleton My_TCP class
        '''
        my_socket=My_TCP(ip,port,type)
        return my_socket.my_socket
    
    
    