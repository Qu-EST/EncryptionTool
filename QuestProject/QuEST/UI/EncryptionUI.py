'''
Created on Mar 15, 2017

@author: jee11
'''
from tkinter import *
from QuEST.UI import UIWidgets
from QuEST.UI import TDCFrames
from queue import Queue
from QuEST.COM import My_TCP
from QuEST.COM import Receiver_Thread
from QuEST.COM import Sender_Thread
from QuEST.TDC import TDCReader
from QuEST.TDC import TDCReaderThread
import threading
import time

class EncryptionUI(Tk):
    '''
    classdocs
    '''


    def __init__(self,all_data):
        '''
        Constructor
        '''
        Tk.__init__(self)
        self.all_data=all_data
        self.title("QuEST Encryption tool")
        #self.console=""
        self.console=TDCFrames.AllConsole(self,self.all_data)
        self.setting_frame=TDCFrames.SettingsFrame(self,self.all_data)
        self.console.pack(side=BOTTOM)
        self.setting_frame.pack(side=TOP)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        
    def on_exit(self):
        for threads in threading.enumerate():
            if(not((threads.name=='MainThread') or threads.isDaemon())):
                
                #if(threads.)
                print("closing the thread "+threads.name)
                threads.off()
                print(type(threads))
                threads.join()
                print(threads.is_alive())        
        print(threading.active_count())
        self.destroy()
        time.sleep(2)
        print(threading.enumerate())  
