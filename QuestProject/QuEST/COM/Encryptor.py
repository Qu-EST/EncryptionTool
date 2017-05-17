'''
Created on Apr 29, 2017

@author: jee11
'''

import pyaes
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
        padded=message.ljust(16)
        #return self.encoder.encrypt(string)
        return self.tfh.encrypt(padded.encode('utf-8'))
    
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
        try:
            return self.tfh.decrypt(bytedata)    
        except:
            return bytedata