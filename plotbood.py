#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 17:29:42 2017

@author: Ali Beydoun et Massilia Hamdani
"""
from __future__ import division
from matplotlib.pyplot import *
import visa
import numpy as np
from pylab import *
import time
from decimal import *


#from PyQt4 import QtCore


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
            vpp=self.instr.ask(':MEAS:VAMP? CHAN1')
            return float(vpp)/2     
        elif str(channel)=='2':
            vpp=self.instr.ask(':MEAS:VAMP? CHAN2')
            return float(vpp)/2
           
        else:
            print('check your Channel')
            
    def rescale(self):
        self.instr.write(':CHAN2' + ':SCALe 2')
        time.sleep(1)
        V_ampl = self.instr.ask(':MEAS:VPP? CHAN2')
        #if V_ampl > 80 :
        self.instr.write(':CHAN2' + ':SCALe ' + str(float(V_ampl)/4))
            
    def get_volt(self,channel):
        print ("Vmax =", self.instr.ask_for_value(':MEASure:VMAX?'+':CHAN' + str(channel)))
        print ("Vmin =", self.instr.ask_for_value(':MEASure:VMIN?'+' '+':CHAN' + str(channel)))
        print ("Vpp =" , self.instr.ask_for_value(':MEASure:VPP?'+' ' + ':CHAN' + str(channel)))
        print ("Vtop =", self.instr.ask_for_value(':MEASure:VTOP?'+' ' + ':CHAN' + str(channel)))
        print ("Vrms =", self.instr.ask_for_value(':MEASure:VRMS?'+' '+ ':CHAN' + str(channel)))
        print ("Vbas =", self.instr.ask_for_value(':MEASure:VBASe?'+' '+ ':CHAN' + str(channel)))
        print ("Vmoy =", self.instr.ask_for_value(':MEASure:VAVerage?'+' '+ ':CHAN' + str(channel)))

        

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
    
    """créee des signaux sinusoidaux sur la voie 1 et 2 d'amplitude donnée , de fréquence variable et offeset nulle,
            de phase nulle.
            CH1 signal de Ref: signal d'entrée
            CH2 signal en sortie du filtre
        """
    def __init__(self):
        self.signal = Generator('USB0::0x1AB1::0x0588::DG1D120300068::INSTR')
        self.oscillo = RigolDS1052E('USB0::0x1AB1::0x0588::DS1ED122206267::INSTR')

       
        
    def dephasage_gain(self,amp):
        liste_phase = []
        liste_gain = []
        liste_A = []
        liste_B = []
        liste_freq = [10**i for i in np.linspace(1.5,6,20)]     
        #self.signal.set_sinus(1,10,amp,0)
        #time.sleep(0.2)
        
            
        
        for f in liste_freq:
            #initialise l echelle verticale de CH2 a 2mV
            #self.oscillo.set_vert_scale(2,0.002)
            #print(f)
            # signal de Ref signal d'entrée A(t) / Ch 1
            self.signal.set_sinus(1,f,amp,0)
            time.sleep(1)
            # signal de sortie B(t) / Ch 2
            #self.signal.set_sinus(2,f,amp,0)
            #time.sleep(0.2)
            # changer la base de temps pour visualiser le signal àl'ecran
            #l'avantage c'est pouvoir acquérir plus de data sur N oscillations
            self.oscillo.set_timebase(1/(f))
            #Set the initial phase = 0°
            time.sleep(1)
            #self.signal.instr.write('PHASe 0')
            #self.signal.instr.write('PHASe:CH2 0')
            #self.signal.get_freq(2)
            #mesurer l'amplitude du signal en sortie du filtre - CH2 
            self.oscillo.rescale()
           

    #instr.write(':CHAN2:OFFS 0') 
            # BREAK(PKKK?????)
            time.sleep(1)
            
            #Gain de la Fonction de transfert = module de rapport des amplitudes
            #amp_sortie  = self.oscillo.get_ampl(2)
            #1er méthode mesure le gain à l'aide de l'oscilloscope
            #gain = abs(amp/amp_sortie)
            
            # la position du max de B(w) signal de sortie / theorie de TiTus 
            #position = int(f*0.12*self.oscillo.get_timebase())
            #2eme methode pour déterminer la position de la pic en utilisant le signal d'entrée qui a une pic a la mêm freq que le signal du sortie qui est plus bruité,
            #la fonction argmax donne la position du max dans la liste, on commence à 1 pour enlever le pic a la position 0 et on termine à 600 - 10 pour eviter d'avoir des pics de HF
            curve_A = self.oscillo.get_curve(1)
            curve_B = self.oscillo.get_curve(2)
            position = np.argmax(abs(np.fft.fft(curve_A)[1:-10])) + 1 
            #print position
         
            #Liste la FT de sortie entrée 
            B_w = np.fft.fft(curve_B)
            A_w = np.fft.fft(curve_A)
            
        
            #phase = (np.pi/180)*np.angle((B_w[position]/A_w[position]),'deg')
        
            #print('phase= ',phase)
            #liste_phase.append(phase)
            #deuxieme methode pour le gain
            gain=abs((B_w[position]/A_w[position]))
            #print gain
              #print gain
            liste_gain.append(gain)
            liste_A.append(A_w[position])
            liste_B.append(B_w[position])
            
            
            phase = np.arctan(imag(B_w[position])/real(B_w[position])) - np.arctan(((imag(A_w[position]))/real(A_w[position])))
            #if phase < 0:
            phase = abs(phase)
            liste_phase.append(phase)
            time.sleep(0.2)
        print liste_phase            
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
        semilogx(liste_freq, np.unwrap(liste_phase, np.pi))
        #*1/(2*np.pi)*360)
        ylabel(u'Phase [rad]')
        xlabel(u'frequence $\omega/2 \pi$ en [Hz]')
        #grid(True, which='both')       
        





       
             
             
# Utilisation
oscillo = RigolDS1052E('USB0::0x1AB1::0x0588::DS1ED122206267::INSTR')
signal = Generator('USB0::0x1AB1::0x0588::DG1D120300068::INSTR')
essaye= Transfert()
essaye.dephasage_gain(5)
#oscillo.set_vert_scale(1,2)                     
#scillo.get_vert_scale(1)
#oscillo.set_timebase(0.001)
#oscillo.get_timebase()
#oscillo.reset()
#oscillo.plot_curve(2)
#oscillo.get_freq(1)
#oscillo.get_voffset(1)
#oscillo.get_curve(1)

#%%

# pour executer dans la console ipython n'oubliez pas %pylab qt

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

p1 = win.addPlot(title="Basic array plotting")
curve = p1.plot([], [])
curve.setData([4,7,8], [3,7,4])







             