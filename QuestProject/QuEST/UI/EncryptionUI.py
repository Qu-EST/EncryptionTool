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
from QuEST.COM.SendProcessor import SendProcessor
from QuEST.UI.Messenger import Messenger
from QuEST.EncryptorData import EncryptorData
class EncryptionUI(Tk):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        Tk.__init__(self)
        self.all_data=EncryptorData()
        self.title("QuEST Encryption tool")
        #self.console=""
        self.console=TDCFrames.AllConsole(self)
        self.setting_frame=TDCFrames.SettingsFrame(self)
        self.console.pack(side=BOTTOM)
        self.setting_frame.pack(side=TOP)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        
    def on_exit(self):
        print("on exit")
        try:
            print("checking if the sender is alive")
            if(self.all_data.sender.is_alive()):
                self.setting_frame.disconnect.invoke()
#                 print("sender is alive. disconnecting the connection before exit")
# #                 disconnT=threading.Thread(target=self.setting_frame.disconnect.invoke).start().join()
# #                 time.sleep(2)
#                 print("thread object created")
# #                 disconnT.start()
#                 print("disconnect thread statred")
# #                 disconnT.join()
#                 print("the connection is disconencted.")
            else: print("no connection to disconnect")
        except AttributeError as e:
            print("no connection to disconnect")
        
#         
#         try:
#             self.all_data.messenger.quit()
#         except AttributeError:
#             print("no messenger to close")
#         
        print("closing the threads")
        for threads in threading.enumerate():
            if(not((threads.name=='MainThread') or threads.isDaemon())):
                
                #if(threads.)
                print("closing the thread "+threads.name)
                print(threads)
                try:
                    threads.off()
                    print(type(threads))
                    print(threads.is_alive())
                    threads.join()
                except AttributeError as e:
                    print("the thread: {} does not have off. hence skipping to close it.".format(threads.name))
                
                        
        print(threading.active_count())
        try:
            self.all_data.encrypt_socket.close()
        except AttributeError:
            print("no socket to close")
        self.quit()
#         time.sleep(2)
        print(threading.enumerate())
        self.quit()  
