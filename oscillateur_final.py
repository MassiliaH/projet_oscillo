# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 19:23:22 2017

@author: DUALCOMPUTER
"""

from matplotlib.pyplot import *
import visa
import numpy as np
from pylab import *
import time
from decimal import *

class RigolDS1052E(object):
    """ 
        Classe pilote de l'oscilloscope RigolDS1052E
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
      
    def get_timebase(self):
        # Retourne la base de temps'
        timebase = self.ask_for_value(':TIMebase:SCALe?' + ':SCAle?')
        #print ('Time = ' , timebase,'s')
        return timebase
        
    def set_timebase(self,value):
        # Définit la base de temps de la voie  'channel' en 'value'
        self.instr.write(':TIMebase:SCALe ' + str(Decimal(value)))
        return str(value)
        
    def get_curve(self,channel):
        #Renvoie la courbe de la voie courante
        self.instr.write(':WAV:DATA? CHAN' + str(channel))
        #val contient des bytes
        val = self.instr.read_raw()
        
        #Transformer les bytes en Short et les places dans un tableau
        return np.array([ord(b) for b in val[10:]])
        
        
    def plot_curve(self, channel):
        data = self.get_curve(channel)
        plot(data)

        
    def get_freq(self,channel):
         #Retourne la fréquence de la voie 'channel' 
        print ("freq =" ,self.ask_for_value(':MEASure:FREQuency?'+' ' +':CHANnel'+str(channel)),'Hz')
 
    def get_ampl(self,channel):
        if str(channel)=='1':
            vpp=self.ask_for_value(':MEAS:VAMP? CHAN1')
            return vpp/2        
        elif str(channel)=='2':
            vpp=self.ask_for_value(':MEAS:VAMP? CHAN2')
            return vpp/2
           
        else:
            print('check your Channel')
            
    def get_volt(self,channel):
        print ("Vmax =", self.ask_for_value(':MEASure:VMAX?'+' '+':CHAN' + str(channel)))
        print ("Vmin =", self.ask_for_value(':MEASure:VMIN?'+' '+':CHAN' + str(channel)))
        print ("Vpp =" , self.ask_for_value(':MEASure:VPP?'+' ' + ':CHAN' + str(channel)))
        print ("Vtop =", self.ask_for_value(':MEASure:VTOP?'+' ' + ':CHAN' + str(channel)))
        print ("Vrms =", self.ask_for_value(':MEASure:VRMS?'+' '+ ':CHAN' + str(channel)))
        print ("Vbas =", self.ask_for_value(':MEASure:VBASe?'+' '+ ':CHAN' + str(channel)))
        print ("Vmoy =", self.ask_for_value(':MEASure:VAVerage?'+' '+ ':CHAN' + str(channel)))

        

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
         print("freq_CH1 =",self.instr.ask_for_value('FREQ?'),'Hz')
        elif str(channel) == '2':
            #Affiche la freq génerée sur ch2
             print('freq_CH2 =',self.ask_for_value('FREQuency:CH2?'),'Hz')
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
              

class Transfert(object):
    
    def __init__(self):
        self.signal = Generator('USB0::0x1AB1::0x0588::DG1D120300068::INSTR')
        self.oscillo = RigolDS1052E('USB0::0x1AB1::0x0588::DS1ED122206267::INSTR')
        
        
    def dephasage_gain(self,amp):
        liste_gain = []
        liste_phase = []
        liste_freq = [10**i for i in np.linspace(2,5,20)]  
        
        for f in liste_freq:
            # signal de Ref signal d'entrée A(t) / Ch 1
            self.signal.set_sinus(1,f,amp,0)
            time.sleep(0.2)
            # changer la base de temps pour visualiser le signal àl'ecran
            #l'avantage c'est pouvoir acquérir plus de data sur N oscillations
            self.oscillo.set_timebase(1/f)
            #Set the initial phase = 0°
            self.signal.instr.write('PHASe 0')
            time.sleep(30/f + 1)
            
            amp_sortie  = self.oscillo.get_ampl(2)
            gain = abs(amp/amp_sortie)
            print amp_sortie
            
            curve_a = self.oscillo.get_curve(1)
            curve_b = self.oscillo.get_curve(2)
            position = np.argmax(abs(np.fft.fft(curve_a)[1:-10])) + 1 
            B_w= np.fft.fft(curve_b)
            A_w = np.fft.fft(curve_a)
            #gain=abs((B_w[position]/A_w[position]))
            phase = (180/np.pi)*np.arctan(B_w[position]/A_w[position])
            liste_phase.append(phase)
            print phase
            liste_gain.append(gain)
            
            
        figure("Diagramme de Bode ")
        #self.liste_A = liste_A  
        #self.liste_B = liste_B
        #clf()
        subplot(2,1,1)
        title('Diagramme de Bode')#($\omega_c$={0} Hz , Gain_0={1})'.format(omega_c,gain))
        #grid(True, which='both')
        loglog(liste_freq, liste_gain)
        ylabel('Amplitude')
        #grid(True, which='both')
        subplot(2,1,2)
        semilogx(liste_freq, liste_phase)
        ylabel(u'Phase [°]')
        xlabel(u'frequence $\omega/2 \pi$ en [Hz]')
        #grid(True, which='both')              
      
            
            
            
oscillo = RigolDS1052E('USB0::0x1AB1::0x0588::DS1ED122206267::INSTR')
signal = Generator('USB0::0x1AB1::0x0588::DG1D120300068::INSTR')
transf = Transfert()
transf.dephasage_gain(6)

        