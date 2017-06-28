'''
Created on Apr 13, 2017

@author: jee11
'''
from threading import Thread, Event
import re
import datetime
from queue import Queue
from QuEST.EncryptorData import EncryptorData
import win32api

class TDCReaderThread(Thread):
    '''
    classdocs
    '''


    def __init__(self, tdc_reader, hash_queue=Queue(0), interface="tdc"):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.hash_queue=hash_queue
        self.tdc_reader=tdc_reader
        self.tdc_switch=Event()
        self.tdc_switch.set()
        self.tdc_reader.start_TDC()
        self.interface=interface
        self.alldata=EncryptorData()
        #self.counter=0
        
    def run(self):
        if(self.interface=="tdc"):
            self.start_reading()
        else:
            self.read_time()
        
    def read_time(self):    
        print("reading the GPS time")
        
        while(self.tdc_switch.is_set()):
            byte_data=self.tdc_reader.readline()
            #print(type(byte_data))
            gpsdata=byte_data.decode('utf-8')
            if(gpsdata[0:6]=="$GPZDA"):
                timestamp=gpsdata[7:28]
                self.alldata.gpstime=timestamp
                hour=timestamp[7:9]
                min=timestamp[9:11]
                sec=timestamp[11:13]
                mmm=timestamp[14:17]
                day=timestamp[18:20]
                month=timestamp[21:23]
                year=timestamp[24:28]
                time_tuple=(year,month,day,hour,min,sec,mmm)
                dayOfWeek = datetime.datetime(time_tuple).isocalendar()[2]
                win32api.SetSystemTime( time_tuple[:2] + (dayOfWeek,) + time_tuple[2:])
                
                #print(timestamp)
            
        print("closing the com port")
        self.tdc_reader.stop_TDC()
        print(self.tdc_reader)    
    def start_reading(self):
        while(self.tdc_switch.is_set()):
            byte_data=self.tdc_reader.readline()
            string_data=byte_data.decode('utf-8')
            #macrotime=datetime.date.strftime(datetime.datetime.now(),'%m:%d_%H:%M:%S:%f')
            #data=macrotime+" "+string_data
            #print(data)
            self.hash_queue.put(string_data)
            #self.hash_queue.task_done()
        print("closing the com port")
        self.tdc_reader.stop_TDC()
        print(self.tdc_reader)
        #print("clearing the hash queue")
        #self.hash_queue=Queue()
                        
    def off(self):
        print("inside tdc reader off")
        self.tdc_switch.clear()
        #print(self.tdc_reader)
        