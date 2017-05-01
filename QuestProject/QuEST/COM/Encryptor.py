'''
Created on Apr 29, 2017

@author: jee11
'''

import pyaes

class Encryptor(object):
    '''
    classdocs
    '''


    def __init__(self, key):
        '''
        Constructor
        '''
        self.key=key
        self.encoder=pyaes.AESModeOfOperationCTR(self.key)
        self.decoder=pyaes.AESModeOfOperationCTR(self.key)
        
    def encode(self,string):
        return self.encoder.encrypt(string)
    
    def decode(self,bytedata):
        return self.decoder.decrypt(bytedata).decode('utf-8')
    
        