import numpy
import time
import matplotlib.pyplot as pyplot

from Keithley import *
from Metric import *


# Settings

resource = 'TCPIP0::192.168.0.30::inst0::INSTR'
filename = 'Tantalum.npz'

V_charge     = 12.5
I_charge     = 0.050
t_charge     = 60. * 60.
t_discharge  = 10.
t_recover    = 15. * 60.
autorangeLow = 100e-9
filterCount  = 10


# Measure

t_start = time.time()

metadata = {}
metadata['V_charge']     = V_charge
metadata['I_charge']     = I_charge
metadata['t_charge']     = t_charge       
metadata['t_discharge']  = t_discharge  
metadata['t_recover']    = t_recover    
metadata['autorangeLow'] = autorangeLow 
metadata['filterCount']  = filterCount  

script = file('Capacitor.tsp').format(V_charge, I_charge, t_charge, t_discharge, t_recover, autorangeLow, filterCount)

keithley = Keithley(resource, 180_000)
keithley.runScript(script)

tVI = []

while True:
    line = keithley.read()
    
    if line == "\n":
        break
    else:
        t, v, i, unit = line.split(',')
        
        t = float(t)
        v = float(v)
        i = float(i)
        
        if unit == 'Amp DC\n':
            if v > 0.5 * V_charge:
                phase = 0
                phaseString = 'Charge'
            else:
                phase = 1
                phaseString = 'Discharge'
        else:
            i, v = v, i
            phase = 2
            phaseString = 'Recover'

        tVI.append([t, v, i, phase])
       
        print('[{:.3f}] Phase: {:s}, V: {:s}, I: {:s}'.format(t, phaseString, metric(v, 3, 'V'), metric(i, 3, 'A', True)))

tVI = numpy.array(tVI)

numpy.savez(filename, metadata = metadata, tVI = tVI)

print('Test complete.')





