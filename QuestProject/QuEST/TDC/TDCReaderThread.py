'''
Created on Apr 13, 2017

@author: jee11
'''
from threading import Thread
import re
import datetime

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
        self.tdc_switch="True"
        self.tdc_reader.start_TDC()
        
    def run(self):
        self.start_reading()
        
    def start_reading(self):
        while(self.tdc_switch=="True"):
            byte_data=self.tdc_reader.readline()
            string_data=byte_data.decode('utf-8')
            macrotime=datetime.date.strftime(datetime.datetime.now(),'%m:%d_%H:%M:%S:%f')
            data=macrotime+" "+string_data
            print(data)
            self.hash_queue.put(data)
        self.tdc_reader.stop_TDC()
                        
    def stop_reading(self):
        self.tdc_switch="False"
        