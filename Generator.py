#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 19:04:40 2017

@author: alibeydoun
"""

from matplotlib.pyplot import *
import visa
import numpy as np 
class Generator(object):
    """
    class pilote of the Waveform Generator
        
    """  
    def __init__(self,num_id):
        self.res_mag = visa.ResourceManager()
        self.res_mag.list_resources()
        #création de l'instrument
        self.instr = self.res_mag.get_instrument(num_id)
        # Affichage du numéro d'identification
        #return self.get_idn()
    
    def ask_for_value(self, command):
        # Transforme la fonction 'ask' pour qu'elle retourne un float
        # plutôt qu'une string (à utiliser lorsque c'est pertinent)
        return float(self.instr.ask(command))    
        
    def get_idn(self):
        # Retourne le numéro d'identification de l'instrument
        return self.instr.ask("*IDN?")
        
    def get_freq(self,channel):  
        if  str(channel) == '1':
        #Affiche la freq génerée sur Ch1
         print("freq_CH1 =",self.instr.ask('FREQ?'))
        elif str(channel) == '2':
            #Affiche la freq génerée sur ch2
             print("freq_CH2 =",self.instr.ask('FREQuency:CH2?'))
        else:
             print('check the channel')
             
         
    def set_freq(self,channel,frequency):
        if  str(channel) == '1':
            #changer la frequence de ch1
            self.instr.write('FREQuency'+ ' '+str(frequency))
        elif str(channel) == '2':
            #Changer la freq de ch2
            self.instr.write('FREQuency:CH2'+ ' '+str(frequency))
        else:
            print('check the channel')
        
    def set_function(self,):
        #Select the output function for CH1
        self.instr.write('FUNCtion {SINusoid|SQUare|RAMP|PULSe|NOISe|DC|USER}')
        
    def set_sinus(self,channel,frequency,amplitude,offset):
        if  str(channel) == '1':
            #Generate a sine wave with specific frequency, amplitude and DC offset via CH1. 
            self.instr.write('APPLy:SINusoid'+' '+str(frequency)+','+str(amplitude)+','+str(offset))
        elif str(channel)=='2':
            #Generate a sine wave with specific frequency, amplitude and DC offset via CH2. 
            self.instr.write(' APPLy:SINusoid:CH2'+' '+str(frequency)+','+str(amplitude)+','+str(offset))
        else:
             print('check the channel')
                  
    def set_square(self,channel,frequency,amplitude,offset):
        if  str(channel) == '1':
            #Generate a square wave with specific frequency, amplitude and DC offset via CH1. 
            self.instr.write('APPLy:SQU'+' '+str(frequency)+','+str(amplitude)+','+str(offset))
        elif str(channel)=='2':
            #Generate a square wave with specific frequency, amplitude and DC offset via CH2. 
            self.instr.write(' APPLy:SQU:CH2'+' '+str(frequency)+','+str(amplitude)+','+str(offset))
        else:
             print('check the channel')
        
    def set_ramp(self,channel,frequency,amplitude,offset):
        if  str(channel) == '1':
            #Generate a ramp wave with specific frequency, amplitude and DC offset via CH1. 
            self.instr.write('APPLy:RAMP'+' '+str(frequency)+','+str(amplitude)+','+str(offset))
        elif str(channel)=='2':
            #Generate a ramp wave with specific frequency, amplitude and DC offset via CH2. 
            self.instr.write('APPLy:RAMP:CH2'+' '+str(frequency)+','+str(amplitude)+','+str(offset))
        else:
             print('check the channel')
        
    def set_pulse(self,channel,frequency,amplitude,offset):
        #Generate a pulse wave with specific frequency, amplitude and DC
        #offset via CH1
        if  str(channel) == '1':
            #Generate a ramp wave with specific frequency, amplitude and DC offset via CH1. 
            self.instr.write('APPLy:PULS'+' '+str(frequency)+','+str(amplitude)+','+str(offset))
        elif str(channel)=='2':
            #Generate a ramp wave with specific frequency, amplitude and DC offset via CH2. 
            self.instr.write('APPLy:PULS:CH2'+' '+str(frequency)+','+str(amplitude)+','+str(offset))
        else:
             print('check the channel')
        
    def set_noise(self,channel,frequency,amplitude,offset):
        #Generate a pulse wave with specific frequency, amplitude and DC
        #offset via CH1
        if  str(channel) == '1':
            #Generate a ramp wave with specific frequency, amplitude and DC offset via CH1. 
            self.instr.write('APPLy:NOIS'+' '+str(frequency)+','+str(amplitude)+','+str(offset))
        elif str(channel)=='2':
            #Generate a ramp wave with specific frequency, amplitude and DC offset via CH2. 
            self.instr.write('APPLy:NOIS:CH2'+' '+str(frequency)+','+str(amplitude)+','+str(offset))
        else:
             print('check the channel')
              
     
signal = Generator('USB0::0x1AB1::0x0588::DG1D120300068::INSTR')
