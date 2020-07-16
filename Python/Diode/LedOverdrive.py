import numpy
import time
import matplotlib.pyplot as pyplot

from Keithley import *
from Metric import *


# Settings
resource = 'TCPIP0::192.168.0.30::inst0::INSTR'
filename = 'LedOverdrive2.npz'

overdriveCurrent = numpy.concatenate((numpy.zeros(5), numpy.linspace(0., 200., 21))) / 1000.

t_overdrive = 60
t_cooling   = 120
dV          = 0.1
I_limit     = 0.020
dt_sweep    = 10
filterCount = 100


# TSP script output parser
def parse(keithley, I_overdrive, t_overdrive, t_cooling, t_start):
    def scan(vSource):
        buffer = []
        while True:
            line = keithley.read()
            if line == "\n":
                break
            else:
                t, v, i = [float(x) for x in line.split(',')]
                if not vSource:
                    v, i = i, v
                buffer.append([t, v, i])
                print('[{:.3f}] Pulse: {:s} @ {:s}, t: {:.3f} s, V: {:s}, I: {:s}, P: {:s}, R: {:s}'.format(time.time() - t_start, metric(I_overdrive, 3, 'A'), metric(t_overdrive, 3, 's'), t, metric(v, 5, 'V'), metric(i, 5, 'A'), metric(v * i, 5, 'W'), metric(v / i, 5, '\u03A9')))
        print('')
        return numpy.array(buffer)

    if I_overdrive != 0 and t_overdrive != 0:
        print('Overdriving...')
        tVI_overdrive = scan(False)

    else:
        tVI_overdrive = numpy.array([])

    print('Cooling for {:.3f} s...'.format(t_cooling))
    print('')

    time.sleep(t_cooling)

    print('I-V tracing...')
    tVI_characteristic = scan(True)

    return tVI_overdrive, tVI_characteristic


# Probe
t_start = time.time()

script = file('LedOverdrive.tsp')

metadata = {}
metadata['t_overdrive'] = t_overdrive
metadata['t_cooling']   = t_cooling
metadata['dV']          = dV
metadata['I_limit']     = I_limit
metadata['dt_sweep']    = dt_sweep
metadata['filterCount'] = filterCount

overdrive = []
characteristic = []

keithley = Keithley(resource, 180_000)

for I_overdrive in overdriveCurrent:
    keithley.runScript(script.format(I_overdrive, t_overdrive, t_cooling, dV, I_limit, dt_sweep, filterCount))
    tVI_overdrive, tVI_characteristic = parse(keithley, I_overdrive, t_overdrive, t_cooling, t_start)

    overdrive.append(tVI_overdrive)
    characteristic.append(tVI_characteristic)

    numpy.savez(filename, metadata = metadata, overdrive = overdrive, characteristic = numpy.array(characteristic), overdriveCurrent = overdriveCurrent[:len(overdrive)])
