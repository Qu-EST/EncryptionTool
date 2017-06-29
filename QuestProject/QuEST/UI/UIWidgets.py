'''
Created on Apr 13, 2017

@author: jee11
'''
from tkinter import Frame, IntVar
from tkinter import Label
from tkinter import Entry
from tkinter import *
from threading import Thread, Event
import os, threading
from QuEST.TDC.TDCReader import TDCReader
from QuEST.TDC.TDCReaderThread import TDCReaderThread
from QuEST.COM.My_TCP import My_TCP
from QuEST.COM.Receiver_Thread import Receiver_Thread
from QuEST.COM.Sender_Thread import Sender_Thread
from QuEST.TDC.SaveFile import SaveFile
from QuEST.UI.Messenger import Messenger
from QuEST.COM.ReceivedProcessor import ReceivedProcessor
from QuEST.COM.SendProcessor import SendProcessor
from QuEST.TDC.KeyHasher import KeyHasher
from QuEST.TDC.TestTimeProducer import TestTimeProducer
from QuEST.EncryptorData import EncryptorData
from queue import Empty
class InputFrame(Frame):
    def __init__(self,master,label_text="label"):
        Frame.__init__(self, master,width=350,height=70)
        #print(self.winfo_height())
        #print(self.winfo_width())
        self.label_text=label_text
        self.label=Label(self,text=label_text,width=12)
        self.entry=Entry(self,width=10)
        self.label.pack(side=LEFT)
        self.entry.pack(side=RIGHT)
    def get_data(self):         
        data=self.entry.get()
        #print("inside get data "+data)
        if (data==''):
            if(self.label_text=="Port No"):
                #print("default port COM3 chosen")
                data="COM6"
                return data
            elif (self.label_text=="Baud rate"):
                #print("default baud rate 38400 chosen")
                data=115200
                return data
        else: return data
    
class CheckBoxFrame(Frame):
    def __init__(self,master,label_text="server"):
        Frame.__init__(self,master,width=350,height=70)
        #self.label=Label(self,text=label_text).pack(side=LEFT)
        self.value=IntVar()
        self.checkbox=Checkbutton(self,text=label_text,variable=self.value)
        self.checkbox.pack()
        
    def getvalue(self):
        return self.value.get()
        
class ChangeButton(Button):        
    def __init__(self,master,console):
        Button.__init__(self,master,text="Load key",command=self.loadkey,width=12)
        self.all_data=EncryptorData()
        all_data=self.all_data
        self.tdc_reader=all_data.tdc_reader
        self.console=console
        self.hash_queue=all_data.hash_queue
        
    def loadkey(self):    
        pass
        os.chdir(r'C:\Users\jee11\Documents\new_28-4\EncryptionTool\QuestProject\QuEST')
        keyfile=open("Quantum_Keys.txt",'r')
        keylist=keyfile.readlines()
        index=1
        for keys in keylist:
            #print(keys.rstrip('\n'))
            tempkey={index:keys.rstrip('\n')}
            self.all_data.key.update(tempkey)
            index=index+1
        print(self.all_data.key)
        
    def unit_test(self):
        pass
        print("Starting Unit Text")
        self.time_producer=TestTimeProducer(self.hash_queue)
        self.time_producer.start()
        self.hasher=KeyHasher()
        self.hasher.start()
        self.all_data.hasher=self.hasher
        self.display_ut=TextPadWriter(self.console.micro_time, self.all_data.ut) #initialize the thread to put the data in the textpad
        self.displaygoodut=TextPadWriter(self.console.good_utime, self.all_data.good_ut)
        self.display_ut.start() #start putting the data in the textpad
        self.displaygoodut.start()
        
        
class StartButton(Button):        
    def __init__(self, master, console, interface="tdc"):
        
        self.all_data=EncryptorData()
        all_data=self.all_data
        self.ui=master
        self.serial_reader=None
        if(interface=="tdc"):
            Button.__init__(self, master, text="Start", command=self.start, width=12)      
            self.console=console            
            self.hash_queue=all_data.hash_queue
            self.tdc_reader=all_data.tdc_reader
            
        else:
            Button.__init__(self, master, text="Start", command=self.startgps, width=12)
            self.gps_reader=all_data.gps_reader
        
    def start(self):
        print("Starting to read from TDC")
        
        if(self.serial_reader is None):
            print("initializing TDC")
            self.serial_reader=TDCReader() #initialize the serial reader
            port=self.ui.port_input.get_data()
            #print(port)
            self.serial_reader.port=port #set the port number
            self.serial_reader.baudrate=self.ui.baud_input.get_data() #set the baudrate
        if(self.all_data.tdc_reader==""):
            self.tdc_reader=TDCReaderThread(self.serial_reader,hash_queue = self.hash_queue) #initalize the reader thread
            self.tdc_reader.start() #start the thread
            self.all_data.tdc_reader=self.tdc_reader
            self.hasher=KeyHasher()
            self.hasher.start()
            self.all_data.hasher=self.hasher
            #print("from start printing the type of tdc reader " + str(type(self.tdc_reader)))
            #print(type(self.all_data.tdc_reader))
            try:
                if not (self.all_data.mt_console.is_alive()):
                    self.start_console()
            except AttributeError:
                self.start_console()
        self.ui.stop_button.config(state=NORMAL)
        self.config(state=DISABLED)
    def start_console(self):
        print("no console present")
        self.display_ut=TextPadWriter(self.console.micro_time, self.all_data.ut) #initialize the thread to put the data in the textpad
        self.displaygoodut=TextPadWriter(self.console.good_utime, self.all_data.good_ut)
        self.display_ut.start() #start putting the data in the textpad
        self.all_data.mt_console=self.display_ut
        self.displaygoodut.start()
        self.all_data.goodt_console=self.displaygoodut
#         print(threading.active_count())
#         print(threading.enumerate())
            
    def startgps(self):
        print("Starting the GPS timer")
        
        
        if(self.serial_reader is None):
            self.serial_reader=TDCReader() #initialize the serial reader
            port=self.ui.gport_input.get_data()
            #print(port)
            self.serial_reader.port=port #set the port number
            self.serial_reader.baudrate=self.ui.baud_input.get_data()
        if(self.all_data.gps_reader==""):
            self.gps_reader=TDCReaderThread(self.serial_reader, interface="gps") #initalize the reader thread
            self.gps_reader.start() #start the thread
            self.all_data.gps_reader=self.gps_reader 
        self.ui.gstop_button.config(state=NORMAL)
        self.config(state=DISABLED)       
class StopButton(Button):        
    def __init__(self,master, interface="tdc"):
        if(interface=="tdc"):
            Button.__init__(self,master,text="Stop",command=self.stop,width=12)
            self.start_button=master.start_button
            self.saver=master.saver            
        else:
            Button.__init__(self,master,text="Stop",command=self.stopgps,width=12)
            self.start_button=master.gstart_button
            
        self.alldata=EncryptorData()        
        self.config(state=DISABLED)
        
    def stop(self):
        pass
        print("Stopping to read from TDC")
        
        print("inside stop button")
        self.tdc_reader=self.alldata.tdc_reader
        hasher=self.alldata.hasher
        mt_console=self.alldata.mt_console
        goodt_console=self.alldata.goodt_console
        try: 
            if(self.tdc_reader.is_alive()):
                self.tdc_reader.off()
                self.tdc_reader.join()
                self.alldata.tdc_reader=""
        except AttributeError:
            print("from the stop. the type of serial reader is not thread{}".format(type(self.serial_reader)))            
        try: 
            if(hasher.is_alive()):
                hasher.off()
                hasher.join()
                self.alldata.hasher=None
        except AttributeError:
            print("from the stop. the type of hasher is not thread{}".format(type(hasher)))
        try:
            if(mt_console.is_alive()):
                self.mt_console.off()
                self.goodt_console.off()
                self.mt_console.join()
                self.goodt_console.join()
        except AttributeError:
            print("from stop. the console has no attributes")
        self.saver.config(state=NORMAL)
        self.config(state=DISABLED)
        self.start_button.config(state=NORMAL)    
            

    def stopgps(self):
        
        self.start_button.config(state=NORMAL)
        print("inside gps stop button")
        self.tdc_reader=self.alldata.gps_reader
        try: 
            if(self.tdc_reader.is_alive()):
                self.tdc_reader.off()
                self.tdc_reader.join()
                self.alldata.gps_reader=""
        except AttributeError:
            print("from the gps stop. the type of serial reader is not thread{}".format(type(self.tdc_reader)))            
        self.config(state=DISABLED)    
        
class ConnectButton(Button):        
    def __init__(self,master,console):
        Button.__init__(self,master,text="Connect",command=self.connectthread,width=12)
        self.ui=master
        self.all_data=EncryptorData()
        self.alldata=self.all_data
        self.receiver=self.all_data.receiver
        self.encrypt_socket=self.all_data.encrypt_socket
        self.received_data=self.all_data.received_data
        self.sender=self.all_data.sender
        self.receivedprocessor=self.all_data.receivedprocessor
        self.send_data=self.all_data.send_data
        self.console=console
    def connectthread(self):
        conT=threading.Thread(target=self.connect)
        conT.setDaemon(True)
        conT.start()
        
    def connect(self):
        #print("this is wereh the objects of connect belong{}".format(type(self)))
        self.disconnect=self.ui.disconnect
        self.communicate=self.ui.start_sending
        self.messenger_button=self.ui.messenger
        
        print("Connecting to the server/client")
        self.IP=self.ui.IP_input.get_data()
        self.if_server=self.ui.if_server.getvalue()
        if(self.if_server):
            self.con_type="server"
        else:
            self.con_type="client"
        self.encrypt_socket=My_TCP(ip=self.IP,port=5005,con_type=self.con_type).my_socket
        print("connected", self.encrypt_socket)
        self.alldata.encrypt_socket=self.encrypt_socket
        #try:
        self.receiver=Receiver_Thread(display_received=self.alldata.displayreceived, received=self.received_data,rcv_socket=self.encrypt_socket)
#         except ConnectionResetError:
#             print("connection reset. invoking the disconnect button")
#             threading.Thread(target=self.alldata.ui.setting_frame.disconnect.invoke).start()
        self.receiver.start()
        self.alldata.receiver=self.receiver
        self.receivedprocessor=ReceivedProcessor(self.alldata)
        self.receivedprocessor.start()
        self.alldata.receivedprocessor=self.receivedprocessor
        self.sender=Sender_Thread(display_sent=self.alldata.displaysent,tosend=self.send_data,send_socket=self.encrypt_socket)
        self.sender.start()
        self.alldata.sender=self.sender
        try:
            if not (self.all_data.sent_console.is_alive()):
                self.start_console()
        except AttributeError:    
            self.start_console()
            
        self.config(state=DISABLED)
        self.disconnect.config(state=NORMAL)
        #self.communicate.config(state=NORMAL)
        self.messenger_button.config(state=NORMAL)
        
    def start_console(self):
        self.displayersent=TextPadWriter(self.console.sent_data, self.alldata.displaysent)
        self.displayerreceived=TextPadWriter(self.console.received_data, self.alldata.displayreceived)
        self.displayersent.start()
        self.displayerreceived.start()
        self.all_data.sent_console=self.displayersent
        self.all_data.received_console=self.displayerreceived
    
        
class DisconnectButton(Button):        
    def __init__(self,master):
        Button.__init__(self,master,text="Disconnect",command=self.disconnect,width=12)
        all_data=EncryptorData()
        self.alldata=all_data
        self.sockettoclose=all_data.encrypt_socket
        #self.sendprocessor=all_data.sendprocessor
        self.receiver=all_data.receiver
        self.receivedprocessor=all_data.receivedprocessor
        self.sender=all_data.sender
        self.messenger=all_data.messenger
        self.config(state=DISABLED)
        self.master=master
        
        
        # to make all queues empty here
        
        
        #self.send_thread=all_data.
    def disconnect(self):
        self.connect=self.master.connect
        self.communicate=self.master.start_sending
        self.messenger_button=self.master.messenger
        print("disConnecting to the server/client")
        
        try:
            print("Trying to close the Messenger")
            self.alldata.messenger.destroy()
            print("messenger closed")
        except AttributeError:
            pass 
            print("no messenger now to destroy")
        except TclError:
            pass
            print("messenger already closed")
        try:
            self.alldata.sendprocessor.off()
        except AttributeError:
            print("no send processor present")
        #self.alldata.encrypt_socket.settimeout(1)
        print("closing the receiver")
        self.alldata.receiver.off()        
        self.alldata.receiver.join()
        print("receiver closed/n closing the received processor")
        self.alldata.receivedprocessor.off()
        self.alldata.receivedprocessor.join()
        print("reciever processor closed/n closig the sender")
        self.alldata.sender.off()
        self.alldata.sender.join()
        print("Sender closed\n closing the socket")
        
        self.alldata.encrypt_socket.close()
        print("socket closed")
        self.connect.config(state=NORMAL)
        self.config(state=DISABLED)
        self.communicate.config(state=DISABLED)
        self.messenger_button.config(state=DISABLED)
        #print(threading.enumerate())
        
        
class StartSendingButton(Button):        
    def __init__(self,master):
        Button.__init__(self,master,text="Error Check",command=self.send,width=12)
        alldata=EncryptorData()
        self.alldata=alldata
        self.sendprocessor=alldata.sendprocessor
        self.config(state=DISABLED)
    def send(self):
        pass
        print("Communicating with the other lab")
        self.sendprocessor=SendProcessor(self.alldata)
        self.sendprocessor.start()
        self.alldata.sendprocessor=self.sendprocessor
        
        
class MessengerButton(Button):
    def __init__(self,master):
        Button.__init__(self,master,text="Messenger",command=self.start_messenger,width=12)
        alldata=EncryptorData()
        self.alldata=alldata
        self.messenger=alldata.messenger
        self.config(state=DISABLED)
    def start_messenger(self):
        pass
        print("Starting the messenger")
        self.config(state=DISABLED)
        self.messenger=Messenger(self.alldata)
        self.alldata.messenger=self.messenger
        self.messenger.mainloop()
        
class SaveButton(Button):
    def __init__(self,master):
        Button.__init__(self,master,text="Save",command=self.start_save,width=12)
        alldata=EncryptorData()
        self.save_data=alldata.save_data
        self.config(state=DISABLED)
    def start_save(self):
        pass
        print("Starting to save")
        self.config(state=DISABLED)
        self.saver=SaveFile(self.save_data)
        self.saver.start()
        
class ConsoleFrame(Frame):
    def __init__(self,master, console_name="micro time"):
        Frame.__init__(self,master)
        self.label=Label(self,text=console_name)
        self.console=Text(self,width=30)
        self.label.pack()
        self.console.pack()
        
class TextPadWriter(Thread):
    def __init__(self, text_pad, data_queue):
        Thread.__init__(self)
        self.data_queue=data_queue
        self.text_pad=text_pad.console        
        self.setDaemon(True)
        self.switch=Event()
        self.switch.set()
        
    def run(self):
        self.display()        
    
    def display(self):
        linecount=lambda T: (int(T.index('end').split('.')[0])-1)
        #if(self.switch.is_set()): print("switch is set: before the while loop")
        while(self.switch.is_set()):
            #print(self.switch.is_set())
            #if(self.switch.is_set()): print("switch is set: inside the while loop")
            #print(linecount(self.text_pad))
            if(linecount(self.text_pad)>40):
                print("exceeded 40 lines in console")
                self.text_pad.delete("1.0","10.0")
            try:
                data=self.data_queue.get(timeout=1)
                self.data_queue.task_done()
            except Empty: pass
                #print("no data in queue")    
            else:
                try:
                    self.text_pad.insert(END,(data+ '\n'))
                except:
                    self.text_pad.insert(END,data)
                    self.text_pad.insert(END,'\n')
                finally:
                    pass
                    self.text_pad.see(END)
                
                 
    def off(self):
        print("inside the textpad writer off")
        self.switch.clear()
        self.switch.clear()
        print(self.switch.is_set())
        print("starting the wait to check if the switch is set to true")
        self.switch.wait()
        print("exited wait")            
                        
