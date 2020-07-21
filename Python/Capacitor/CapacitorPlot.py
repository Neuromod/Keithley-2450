import numpy
import matplotlib.pyplot as pyplot
import scipy.signal as signal
import scipy

from Metric import *


# Settings

input = ['Aluminum.npz', 'Ceramic.npz', 'Film.npz', 'Tantalum.npz', 'SuperCapacitor.npz']
outputVoltage = 'CapacitorVoltage.png'

inputLabel = ['Aluminum', 'Ceramic', 'Film', 'Tantalum', 'Supercapacitor']


# Read files

tVIlist = []
metadataList = []

for file in input:
    file = numpy.load(file,  allow_pickle = True)

    metadata = file['metadata'][()]

    metadataList.append(metadata)

    tVI = file['tVI']

    tVI[:, 1] = tVI[:, 1] / metadata['V_charge']
    tVI[:, 0] -= tVI[numpy.argmin(numpy.diff(tVI[:, 1])), 0]

    tVIlist.append(tVI)


# Plot voltage

for tVI in tVIlist:
    pyplot.semilogy(tVI[:, 0] / 60., tVI[:, 1])

pyplot.grid(True, axis = 'y', which = "both", ls="-", color = '0.75')

tickValues = [1E0, 1E-1, 1E-2, 1E-3]
pyplot.yticks(tickValues, [str(v) for v in tickValues])

pyplot.xlim([0, 15])
pyplot.ylim([0.001, 2])

pyplot.xlabel('Time (min)')
pyplot.ylabel('Voltage (Vcharge)')

pyplot.legend(inputLabel, frameon = False)

pyplot.gcf().set_size_inches(12, 9)
pyplot.savefig(outputVoltage, dpi = 300)
pyplot.clf()


# Print values

print('Dielectric absorption')

for i in range(len(input)):
    slice = tVIlist[i][:, 0] > 10.
    print('{:<15}: {:.2f} %'.format(inputLabel[i], 100. * tVIlist[i][slice, 1].max()))

print()

print('Leakage after 5 min')

for i in range(len(input)):
    f = scipy.interpolate.interp1d(tVIlist[i][:, 0], tVIlist[i][:, 2], kind = 'linear')
    t = numpy.arange(-330., -270., .05)
    I = numpy.mean(f(t))

    print('{:<15}: {:>6}, {:>7}'.format(inputLabel[i], metric(metadataList[i]['V_charge'], 3, 'V'), metric(I, 3, 'A')))
