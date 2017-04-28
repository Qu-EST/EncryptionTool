'''
Created on Apr 13, 2017

@author: jee11
'''


from QuEST.UI.EncryptionUI import EncryptionUI
from QuEST import EncryptorData
all_data=EncryptorData.EncrptorData()
ui=EncryptionUI(all_data)
ui.mainloop()


