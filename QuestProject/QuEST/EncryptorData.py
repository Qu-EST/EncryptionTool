'''
Created on Apr 19, 2017

@author: jee11
'''
from queue import Queue
from _overlapped import NULL
from QuEST.TDC.TDCReaderThread import TDCReaderThread

class EncrptorData(object):
    '''
    classdocs
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
        self.encrypt_key=""
        self.encryptor=""
        
        