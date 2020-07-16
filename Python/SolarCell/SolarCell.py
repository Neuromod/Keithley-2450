import visa
import numpy

from RunScript import *
from Metric import *


# Settings
resource = 'TCPIP0::192.168.0.30::inst0::INSTR'
step = 10

# Run script
keithley = runScript(resource, 'SolarCell.tsp', step)

# Retrieve values
voc = float(keithley.read())
isc = float(keithley.read())
vmax = float(keithley.read())
imax = float(keithley.read())
pmax = vmax * imax

# Disconnect from the instrument
keithley.close()

# Print values
print('Voc:  {:s}'.format(metric(voc, 5, 'V')))
print('Isc:  {:s}'.format(metric(isc, 5, 'A')))
print('Pmax: {:s}'.format(metric(pmax, 5, 'W')))
print('Vmax: {:s}'.format(metric(vmax, 5, 'V')))
print('Imax: {:s}'.format(metric(imax, 5, 'A')))
