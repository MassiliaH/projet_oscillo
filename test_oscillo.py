# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 15:35:00 2017

@author: DUALCOMPUTER
"""

import visa
from numpy import *
import matplotlib.pyplot as plot

res_mag = visa.ResourceManager()
res_mag.list_resources()

test = res_mag.get_instrument('USB0::0x1AB1::0x0588::DS1ED122206267::INSTR')
print test.ask("*IDN?")
print test.ask(":CHAN1:SCAL?")


test.write('WAVeform:DATA? CHAN1')