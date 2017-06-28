'''
Created on Apr 21, 2017

@author: jee11
'''
from threading import Thread, Lock
from queue import Queue, Empty
from QuEST.COM.Encryptor import Encryptor
from twofish import Twofish
from QuEST.EncryptorData import EncryptorData
import threading

class ReceivedProcessor(Thread):
    '''
    classdocs
    '''


    def __init__(self, lock=Lock()):
        '''
        Constructor
        '''
        Thread.__init__(self)
        self.alldata=EncryptorData()
        self.received=self.alldata.received_data
        self.lock=lock
        self.key=self.alldata.key
        self.goodkey=self.alldata.goodkey
        self.send_queue=self.alldata.send_data
        self.xor_switch="True"
        self.message=self.alldata.displaymessage
        self.processor_switch=1
        #self.counter=0
        self.value1=0
        self.value2=0
        
    def run(self):
        self.process()
        
    def process(self):
        while(self.processor_switch):
            try:
                bytedata=self.received.get(timeout=1)
            except Empty: pass#print("queue timeout from receivevd processor")
            else:
                if(bytedata==b''): 
                    threading.Thread(target=self.alldata.ui.setting_frame.disconnect.invoke).start()
                
                elif(self.alldata.encrypt_key==""):                
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
                    index=int(bytedata[:2])
                    print(index)
                    print(self.alldata.key)
                    self.alldata.encrypt_key=self.alldata.key[index]
                    tfh=Twofish((self.alldata.key[index]).encode())
                    try:                
                        displaymessage=self.alldata.encryptor.decode(bytedata[2:], tfh)
                    except AttributeError:
                        self.alldata.encryptor=Encryptor(b'7774')
                        displaymessage=self.alldata.encryptor.decode(bytedata[2:], tfh)
                    print("decoded message")
                    print(displaymessage)
                    self.process_message(displaymessage.decode('utf-8'))
                    self.set_keylabel()
    
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
            print("inside xor_processor: printing the value1 and value2")
            print(self.value1)
            print(self.value2)
            if((self.value1^self.value2)==xor):
                if(self.alldata.goodkey==""):
                    self.alldata.goodkey=(key1,key2)
                else:
                    tempgoodkey=(key1,key2)
                    self.alldata.goodkey=self.alldata.goodkey+tempgoodkey
                send_data="goodut " + key1+ " "+ key2
                self.send_queue.put(send_data)
                #self.counter=self.counter+1
                if(len(self.alldata.goodkey)==2):
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
        for gkey in self.alldata.goodkey:
            #try:
            #    key_success="True"
            keypart=self.alldata.key[gkey]
            #except:
            #    print("Error unable to read the correct key form the key dictionary")
            #    key_success="False"
            #if(key_success):
            temp_key=temp_key+str(keypart)
        self.alldata.encrypt_key=temp_key.encode('utf-8')
        
    def set_keylabel(self):
        if(self.alldata.messenger!=""):
            self.alldata.messenger.setkey()          
        
        
