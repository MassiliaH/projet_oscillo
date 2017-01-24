# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 13:52:48 2017

@author: DUALCOMPUTER
"""


import visa

class RIGOLDS1052E(object):
    """ 
        Classe pilote du RIGOLDS1052E
    """
    
    def __init__(self):
        self.res_mag = visa.ResourceManager()
        self.res_mag.list_resources()
        
        #création de l'instrument
        self.instr = self.res_mag.get_instrument('USB0::0x1AB1::0x0588::DS1ED122206267::INSTR')
        
        
        print(self.get_idn())
        
    def get_idn(self):
        return self.instr.ask("*IDN?")

    def get_curve(self):
        """should take a curve"""
        return [1,5,6]
        
# Utilisation
oscillo = RIGOLDS1052E()

