import numpy
import matplotlib.pyplot as pyplot
import matplotlib.pylab as pylab


# Settings

input = 'LedOverdrive2.npz'
outputLogVI = 'LedCharacteristicLog.png'
outputLinVI = 'LedCharacteristicLin.png'
outputTV = 'LedOverdrive.png'

sliceStart = 5
sliceEnd   = 30


# Functions

def plotIV(characteristic, overdriveCurrent, log, xlim):
    nCurve = overdriveCurrent.size
    colormap = pylab.cm.plasma(numpy.linspace(0, 1, nCurve))

    I_min = 1.
    I_max = 0.

    for i in range(nCurve):
        V = characteristic[i][:, 1]
        I = characteristic[i][:, 2]

        I_max = max(I_max, I.max())
        I_min = min(I_min, I.min())

        if log:
            pyplot.semilogy(V, I, color = colormap[i])
        else:
            pyplot.plot(V, I * 1000., color = colormap[i])

    pyplot.xlim(xlim)

    pyplot.xlabel('Voltage (V)')
    
    if log:
        tickValues = [1, 100e-3, 10e-3, 1e-3, 100e-6, 10e-6, 1e-6, 100e-9, 10e-9, 1e-9, 100e-12, 10e-12, 1e-12, 100e-15, 10e-15, 1e-15]
        tickUnits  = ['1A', '100 mA', '10 mA', '1 mA', '100 \u00B5A', '10 \u00B5A', '1 \u00B5A', '100 nA', '10 nA', '1 nA', '100 pA', '10 pA', '1 pA', '100 fA', '10 fA', '1 fA']
        pyplot.yticks(tickValues, tickUnits)

        I_min = 10. ** numpy.floor(numpy.log10(I_min))
        I_max = 10. ** numpy.ceil(numpy.log10(I_max))
        pyplot.ylim([I_min, I_max])
        
        pyplot.ylabel('Current')

        pyplot.grid(True, axis = 'y', which = "both", ls="-", color = '0.75')
    else:
        pyplot.ylabel('Current (mA)')

    pyplot.legend([str(round(x * 1000, 0)) + 'mA' for x in overdriveCurrent], frameon = False)


def plotTV(overdrive, overdriveCurrent, xlim, ylim):
    nCurve = overdriveCurrent.size
    colormap = pylab.cm.plasma(numpy.linspace(0, 1, nCurve))

    skip = 0
    
    for i in range(nCurve):
        if overdrive[i].size == 0:
            skip += 1
        else:
            pyplot.plot(overdrive[i][:, 0], overdrive[i][:, 1], color = colormap[i])

    pyplot.xlabel('Time (s)')
    pyplot.ylabel('Voltage (V)')
    
    pyplot.xlim(xlim)
    pyplot.ylim(ylim)

    pyplot.legend([str(round(x * 1000, 0)) + 'mA' for x in overdriveCurrent[skip : ]], frameon = False)



# Code

file = numpy.load(input, allow_pickle = True)

metadata         = file['metadata'].item()
overdrive        = file['overdrive'][sliceStart : sliceEnd]
overdriveCurrent = file['overdriveCurrent'][sliceStart : sliceEnd]
characteristic   = file['characteristic'][sliceStart : sliceEnd]

print('t_overdrive: {:g} s'.format(metadata['t_overdrive']))
print('t_cooling:   {:g} s'.format(metadata['t_cooling']))
print('dV:          {:g} dV/dt'.format(metadata['dV']))
print('I_limit:     {:g} A'.format(metadata['I_limit']))
print('dt_sweep:    {:g} s'.format(metadata['dt_sweep']))
print('filterCount: {:g}'.format(metadata['filterCount']))

plotIV(characteristic, overdriveCurrent, False, (0, 4))
pyplot.gcf().set_size_inches(12, 9)
pyplot.savefig(outputLinVI, dpi = 300)
pyplot.clf()

plotIV(characteristic, overdriveCurrent, True, (0, 4))
pyplot.gcf().set_size_inches(12, 9)
pyplot.savefig(outputLogVI, dpi = 300)
pyplot.clf()

plotTV(overdrive, overdriveCurrent, (-2, 77), (2.5, 6.5))
pyplot.gcf().set_size_inches(12, 9)
pyplot.savefig(outputTV, dpi = 300)
pyplot.clf()
