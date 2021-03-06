'''
Created on Apr 13, 2017

@author: jee11
'''
from threading import Thread, Event
import re
import datetime
from queue import Queue

class TDCReaderThread(Thread):
    '''
    classdocs
    '''


    def __init__(self, hash_queue, tdc_reader):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.hash_queue=hash_queue
        self.tdc_reader=tdc_reader
        self.tdc_switch=Event()
        self.tdc_switch.set()
        self.tdc_reader.start_TDC()
        #self.counter=0
        
    def run(self):
        self.start_reading()
        
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
        