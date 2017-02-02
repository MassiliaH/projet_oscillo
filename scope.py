#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 12:03:19 2017

@author: alibeydoun
"""
from matplotlib.pyplot import *
import visa
import numpy as np 
class RigolDS1052E(object):
    """ 
        Classe pilote du RigolDS1052E
    """
    
    def __init__(self,num_id):
         
        self.res_mag = visa.ResourceManager()
        self.res_mag.list_resources()
        #création de l'instrument
        self.instr = self.res_mag.get_instrument(num_id)
        # Affichage du numéro d'identification
        print(self.get_idn())
        
    def get_idn(self):
        # Retourne le numéro d'identification de l'instrument
        return self.instr.ask("*IDN?")
   
    def reset(self):
        # Restaure les paramètres d'usine de l'instrument
        self.instr.write('*RST') 
        
    def ask_for_value(self, command):
        # Transforme la fonction 'ask' pour qu'elle retourne un float
        # plutôt qu'une string (à utiliser lorsque c'est pertinent)
        return float(self.instr.ask(command))
        
    def get_vert_scale(self, channel):
        # Retourne l'échelle vertical de la voie 'channel' 
        print (self.ask_for_value(':CHAN' + str(channel) + ':SCAle?'))
        
    def set_vert_scale(self, channel, value):
        # Change l'échelle verticale de la voie 'channel' en 'value'
        self.instr.write(':CHAN' + str(channel) + ':SCALE ' + str(value))
      
    def get_timebase(self,channel):
        # Retourne la base de temps de la voie 'channel'
        print (self.ask_for_value(':TIMebase:SCALe?' + str(channel) + ':SCAle?'))
        
    def set_timebase(self, channel ,value):
        # Définit la base de temps de la voie  'channel' en 'value'
        self.instr.write(':CHAN' + str(channel) + ':TIMebase:SCALe ' + str(value))
        
    def get_curve(self,channel):
        #Renvoie la courbe de la voie courante
        self.instr.write(':WAVeform:DATA? ' + ‘CHANnel’ + str(channel))
        #val contient des bytes
        val = self.instr.read_raw()
        #Transformer les bytes en Short et les places dans un tableau
        return np.array([short(b) for b in val[10:]])

        
    def get_freq(self,channel):
         #Retourne la fréquence de la voie 'channel' 
        print ("freq =" ,self.ask_for_value(':MEASure:FREQuency?’+’:CHAN' + str(channel)))

    
    def get_ampl(self,channel):
        print ( self.ask_for_value(':CHAN' + str(channel) + ':MEASure:VAMPlitude?'))
        
    def get_volt(self,channel):
        print ("Vmax =" , self.ask_for_value(':CHAN' + str(channel) + ':MEASure:VMAX?'))
        print ("Vmin =" , self.ask_for_value(':CHAN' + str(channel) + ':MEASure:VMIN?'))
        print ("Vpp =" , self.ask_for_value(':CHAN' + str(channel) + ':MEASure:VPP?'))
        print ("Vtop =", self.ask_for_value(':CHAN' + str(channel) + ':MEASure:VTOP?'))
        print ("Vrms =" , self.ask_for_value(':CHAN' + str(channel) + ':MEASure:VRMS?'))
        print ("Vmoy =", self.ask_for_value(':CHAN' + str(channel) + ':MEASure:VAVerage?'))
        print ("Vbas =", self.ask_for_value(':CHAN' + str(channel) + ':MEASure:VBASe?'))
        
        
   
    def get_params(self, channel):
        # Retrourne les paramètres de l'oscillo
        # nécessaires au dimensionnement des données
        self.set_channel(1)
        self.vscale = self.get_
        vert_scale(channel)
        self.hscale = self.get_timebase()
        
        
    #def get_encoding(self):
     #   return self.instr.ask('DATa:ENCdg?')
        
 



# Utilisation
oscillo = RigolDS1052E('USB0::0x1AB1::0x0588::DS1ED122206267::INSTR')
#oscillo.set_vert_scale(1,3)
#oscillo.get_vert_scale(1)
#oscillo.set_timebase(1,0.02)
#oscillo.get_timebase()
#oscillo.reset()
oscillo.get_curve(1)
#oscillo.get_freq(1)
#oscillo.get_voffset(1)

