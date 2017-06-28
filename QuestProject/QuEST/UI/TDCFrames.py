'''
Created on Apr 13, 2017

@author: Quest10
'''
from tkinter import *
from QuEST.UI import UIWidgets
from QuEST.EncryptorData import EncryptorData
class SettingsFrame(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        self.all_data=EncryptorData()
        #TDC Settings
        self.TDC_part=Label(self,text="TDC Setting",width=25)
        self.port_input=UIWidgets.InputFrame(self,label_text="Port No")
        print("port_type")
        print(type(self.port_input))
        self.baud_input=UIWidgets.InputFrame(self,label_text="Baud rate")
        self.change_button=UIWidgets.ChangeButton(self,master.console)
        self.start_button=UIWidgets.StartButton(self,master.console)
        self.saver=UIWidgets.SaveButton(self)
        self.stop_button=UIWidgets.StopButton(self)
        
        
        self.TDC_part.grid(row=0, column=0, sticky=W)
        self.port_input.grid(row=1,column=0, sticky=W)
        self.baud_input.grid(row=2,column=0,sticky=W)
        self.baud_input.entry.config(state=DISABLED)   #Disabling the baud input temporarily
        self.change_button.grid(row=3,column=0,sticky=W)
        self.start_button.grid(row=4,column=0,sticky=W)
        self.stop_button.grid(row=5,column=0,sticky=W)
        self.saver.grid(row=6,column=0,sticky=W)
        
        #GPS Settings
        
        self.GPS_part=Label(self,text="GPS Setting",width=25)
        self.gport_input=UIWidgets.InputFrame(self,label_text="Port No")
        print("port_type")
        print(type(self.port_input))
        self.gbaud_input=UIWidgets.InputFrame(self,label_text="Baud rate")
        self.gchange_button=UIWidgets.ChangeButton(self,master.console)
        self.gstart_button=UIWidgets.StartButton(self,master.console,interface="gps")
        #self.saver=UIWidgets.SaveButton(self)
        self.gstop_button=UIWidgets.StopButton(self,interface="gps")
        
        
        self.GPS_part.grid(row=0, column=1, sticky=W)
        self.gport_input.grid(row=1,column=1, sticky=W)
        self.gbaud_input.grid(row=2,column=1,sticky=W)
        self.gbaud_input.entry.config(state=DISABLED)   #Disabling the baud input temporarily
        #self.change_button.grid(row=3,column=1,sticky=W)
        self.gstart_button.grid(row=4,column=1,sticky=W)
        self.gstop_button.grid(row=5,column=1,sticky=W)
        #self.saver.grid(row=6,column=1,sticky=W)
        
        #Communication Settings
        self.comm_part=Label(self,text="Communication Setting",width=25)
        self.IP_input=UIWidgets.InputFrame(self,label_text="IP:")
        self.if_server=UIWidgets.CheckBoxFrame(self,label_text="Server")
        self.connect=UIWidgets.ConnectButton(self,master.console)
        self.disconnect=UIWidgets.DisconnectButton(self)
        self.start_sending=UIWidgets.StartSendingButton(self)
        self.messenger=UIWidgets.MessengerButton(self)
        
        self.comm_part.grid(row=0,column=2,sticky=W)
        self.IP_input.grid(row=1,column=2,sticky=W)
        self.if_server.grid(row=2,column=2,sticky=W)
        self.connect.grid(row=3,column=2,sticky=W)
        self.disconnect.grid(row=4,column=2,sticky=W)
        
        self.start_sending.grid(row=5,column=2,sticky=W)
        self.messenger.grid(row=6,column=2,sticky=W)
        
        
class AllConsole(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        all_data=EncryptorData()
        self.all_data=all_data
        self.micro_time=UIWidgets.ConsoleFrame(self, console_name="micro time")
        self.good_utime=UIWidgets.ConsoleFrame(self, console_name="good micro time")
        self.sent_data=UIWidgets.ConsoleFrame(self, console_name="data Sent")
        self.received_data=UIWidgets.ConsoleFrame(self, console_name="data Received")
        self.micro_time.grid(row=0,column=0,sticky=W)
        self.good_utime.grid(row=0,column=1,sticky=W)
        self.sent_data.grid(row=0,column=2,sticky=W)
        self.received_data.grid(row=0,column=3,sticky=W)
