'''
Created on Apr 21, 2017

@author: jee11
'''
from tkinter import Tk, Text, Frame, Entry, Button, Label
from tkinter.constants import TOP, LEFT, RIGHT, END, BOTTOM, DISABLED, CENTER, W
from QuEST.UI import UIWidgets
from threading import Thread, Lock
from queue import Queue
import time

class Messenger(Tk):
    '''
    classdocs
    '''


    def __init__(self,alldata):
        '''
        Constructor
        '''
        Tk.__init__(self)
        self.title("QuEST Messenger")
        self.send_queue=alldata.send_data
        self.messagepad=Text(self)
        #self.messagepad.config(state=DISABLED)
        self.messagepad.pack(side=TOP)
        self.displaymessage=alldata.displaymessage
        self.sendframe=SendFrame(self,self.send_queue,self.displaymessage,alldata)
        self.sendframe.pack(side=BOTTOM)
        self.display=DisplayThread(self.messagepad,self.displaymessage)
        self.display.start()
        
        
    def setkey(self):
        self.sendframe.setkeylabel()    
    
        
        
    
        
        
class SendFrame(Frame):
    
    def __init__(self,master,send_queue,messagequeue,alldata):
        Frame.__init__(self,master)
        self.alldata=alldata
        self.send_queue=send_queue
        self.messagequeue=messagequeue
        self.entry=Entry(self,width=50)
        self.sendbutton=Button(self,command=self.send,text="Send",width=12)
        self.key_label=Label(self)
        self.setkeylabel()
        #self.key_label.grid(row=0,column=0,sticky=W)
        self.entry.grid(row=0,column=1,sticky=W)
        self.sendbutton.grid(row=0,column=2,sticky=W)
        
        
    def send(self):
        to_send=self.entry.get()
        print("Sending: "+to_send)
        self.send_queue.put("message "+to_send)
        self.messagequeue.put("ME: "+to_send)
        self.entry.delete(0,'end')
        
    def setkeylabel(self):
        if(self.alldata.encrypt_key==""):
            self.key_label.config(text="no encryption")
            self.key_label.grid(row=0,column=0,sticky=W)
            #return "no encryption"
        else:
            text="encryption key: "+self.alldata.encrypt_key.decode('utf-8')
            self.key_label.config(text=text)
            self.key_label.grid(row=0,column=0,sticky=W)
            #return text
        
        
class DisplayThread(Thread):
    
    def __init__(self,textpad,messagequeue):
        Thread.__init__(self)
        self.messagequeue=messagequeue
        self.textpad=textpad
        
    def run(self):
        self.display()
        
    def display(self):
        while(1):            
            if(~self.messagequeue.empty()):
                data=self.messagequeue.get()
                self.textpad.insert(END,data)
                self.textpad.insert(END,'\n')
                self.textpad.see(END)
                self.messagequeue.task_done()
                time.sleep(1)
                
            
    
        
        
        

        
        
            