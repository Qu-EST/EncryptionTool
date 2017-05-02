'''
Created on Apr 21, 2017

@author: jee11
'''
from threading import Thread, Lock
from queue import Queue
from QuEST.COM.Encryptor import Encryptor

class ReceivedProcessor(Thread):
    '''
    classdocs
    '''


    def __init__(self, alldata, lock=Lock()):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.received=alldata.received_data
        self.lock=lock
        self.key=alldata.key
        self.goodkey=alldata.goodkey
        self.send_queue=alldata.send_data
        self.xor_switch="True"
        self.message=alldata.displaymessage
        self.processor_switch=1
        #self.counter=0
        self.alldata=alldata
        self.value1=0
        self.value2=0
        
    def run(self):
        self.process()
        
    def process(self):
        while(self.processor_switch):
            if(~self.received.empty()):
                bytedata=self.received.get()
                if(self.alldata.encrypt_key==""):                
                    data=bytedata.decode('utf-8')
                    print("Processing received data: "+data)
                    command=data.partition(" ")
                    if(command[0]=="goodut"):
                        pass
                        self.process_goodut(command[2])
                    elif(command[0]=="stop"):
                        print("about to call the stop processor")
                        self.process_stop()
                    elif(command[0]=="XOR"):
                        print("inside XOR")
                        if(self.xor_switch=="True"):
                            self.process_CRC(command[2])
                    elif(command[0]=="message"):
                        self.process_message(command[2])
                else:
                    pass
                    displaymessage=self.alldata.encryptor.decode(bytedata)
                    print("decoded message")
                    print(displaymessage)
                    self.process_message(displaymessage.decode('utf-8'))
    
    def process_goodut(self, mygooduts):
        decom=mygooduts.partition(" ")
        if(self.alldata.goodkey==""):
            self.alldata.goodkey=(decom[0],decom[2])
        else:
            tempgoodkey=(decom[0],decom[2])
            self.alldata.goodkey=self.alldata.goodkey+tempgoodkey
        
    def process_stop(self):
        self.xor_switch="False"
        self.alldata.sendprocessor.off()
        self.set_encryptkey()
        self.set_keylabel()
        self.encryptor=Encryptor(self.alldata.encrypt_key)
        self.alldata.encryptor=self.encryptor
    def process_CRC(self,mycrcdata):
        decom=mycrcdata.partition(" ")
        key1=decom[0]
        decom=decom[2].partition(" ")
        key2=decom[0]
        xor=int(decom[2].strip(" "))
        print("printing the decoded xor: "+key1+key2+str(xor))
        try:
            self.value1=self.alldata.key[key1]
            self.value2=self.alldata.key[key2]
            self.keypresent="True"
        except:
            print("values not in dictionary")
            self.keypresent="False"
        if(self.keypresent):
            print("printing the xored value in this machine: "+str(self.value1^self.value2))
            if((self.value1^self.value2)==xor):
                if(self.alldata.goodkey==""):
                    self.alldata.goodkey=(key1,key2)
                else:
                    tempgoodkey=(key1,key2)
                    self.alldata.goodkey=self.alldata.goodkey+tempgoodkey
                send_data="goodut " + key1+ " "+ key2
                self.send_queue.put(send_data)
                #self.counter=self.counter+1
                if(len(self.alldata.goodkey)==8):
                    self.send_queue.put("stop")
                    self.xor_switch="False"
                    self.set_encryptkey()
                    self.set_keylabel()
                    self.encryptor=Encryptor(self.alldata.encrypt_key)
                    #print(self.encryptor)
                    self.alldata.encryptor=self.encryptor
                    
            
        
    def process_message(self,enc_message):
        print("inside message processor! queueing to display: "+enc_message)
        if(self.alldata.encrypt_key!=""):
            self.message.put("Sender: " + enc_message) 
        else:
            pass
            
    def off(self):
        self.processor_switch=0
        
    def set_encryptkey(self):
        temp_key=""
        for key in self.alldata.goodkey:
            temp_key=temp_key+str(self.alldata.key[key])
        self.alldata.encrypt_key=temp_key.encode('utf-8')
        
    def set_keylabel(self):
        if(self.alldata.messenger!=""):
            self.alldata.messenger.setkey()          
        
        