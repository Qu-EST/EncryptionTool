
'''
Created on Apr 13, 2017

@author: jee11
'''
import os
os.chdir(r'C:\Users\jee11\Documents\new_28-4\EncryptionTool\QuestProject ')
#print(os.getcwd())

from QuEST.UI.EncryptionUI import EncryptionUI
from QuEST import EncryptorData
all_data=EncryptorData.EncryptorData()
ui=EncryptionUI()
all_data.ui=ui
ui.mainloop()

