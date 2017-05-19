'''
Created on Apr 29, 2017

@author: jee11
'''

import pyaes
import math
from twofish import Twofish

class Encryptor(object):
    '''
    classdocs
    '''


    def __init__(self, key):
        '''
        Constructor
        '''
        self.key=b'7774'
        #self.encoder=pyaes.AESModeOfOperationCTR(self.key)
        #self.decoder=pyaes.AESModeOfOperationCTR(self.key)
        self.tfh=Twofish(self.key)
        
    def encode(self,message):
        times=math.ceil(len(message)/16)
        counter=1
        enc=b''
        while(times>0):
            times=times-1        
            block=message[((counter-1)*16):(counter*16)]
            #print(len(block))
            #print(block)
            
            try:
                if(counter==1):
                    enc = self.tfh.encrypt(block.encode())
                    #print(enc)
                else:    
                    enc=enc + b' ' + self.tfh.encrypt(block.encode())
                    #print(enc)
            except ValueError:
                block=block.ljust(16)
                enc=enc + b' ' + self.tfh.encrypt(block.encode()) 
                #print(enc)      
            counter=counter+1
        return enc
    
    def decod(self,bytedata):
        '''code for the aes not used
        '''
        
        try:
            print("inside decoder")
            print(bytedata)
            data= self.decoder.decrypt(bytedata)
            print(data)
            return data
        except:
            pass
        finally:
            return ""
    def decode(self, bytedata):
        print(bytedata)
        message=b''
        splitted=bytedata.split(b' ')
        for blocks in splitted:
            try:
                message = message + self.tfh.decrypt(blocks)
            except ValueError:
                message = message +self.tfh.decrypt(splitted)
        return message