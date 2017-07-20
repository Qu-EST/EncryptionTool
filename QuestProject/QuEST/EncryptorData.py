'''
Created on Apr 19, 2017

@author: jee11
'''
from queue import Queue
#from QuEST.TDC.TDCReaderThread import TDCReaderThread
from threading import RLock
from threading import Condition
class Singleton(type):
    '''Metaclass for the singleton'''
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class EncryptorData(metaclass=Singleton):
    '''
    Data to be shared with all the encryptor modules
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.ut=Queue(0)            #display
        self.good_ut=Queue(0)       #display
        self.good_utsend=Queue(0)   #send processor
        self.received_data=Queue(0) #receiver and processor
        self.hash_queue=Queue(0)    #hasher
        self.send_data=Queue(0)     #for tcp sending
        self.save_data=Queue(0)     #queue to save data
        self.displaysent=Queue(0)
        self.displayreceived=Queue(0)
        self.encrypt_socket=""      #our socket
        self.tdc_serial=""          #Serial object to read data
        self.tdc_reader=""          #thread to read the serial data
        self.receiver=""            #thread to receive from TCP
        self.sender=""              #Thread to send the data TO TCP
        self.saver=""               #thread to save data
        self.sendprocessor=""       #thread process the sending
        self.receivedprocessor=""   #thread to process the received data
        self.displaymessage=Queue(0) #to display message
        self.key={"0":0}
        self.messenger=""
        self.hasher=""
        self.goodkey=""
        self.encrypt_key="74"
        self.encryptor=""
        self.ui=""
        self.gpstime=""
        self.gps_reader=""             #thread to read the gps time
        self.mt_console=None
        self.goodt_console=None
        self.sent_console=None
        self.received_console=None
        self.filename=None         #to save file name
        self.gpstime_lock=RLock()  # lock for accessing the gps time
        self.gpstime_condi=Condition(lock=self.gpstime_lock) # condition for accessing the gps time
