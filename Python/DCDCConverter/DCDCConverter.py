import numpy
import matplotlib.pyplot as pyplot


# Settings

dmmInput = 'DMM-DCDC.csv'
smuInput = 'SMU-DCDC.csv'
output   = 'DCDC.png'

loadResistance = 8.292  # Unit: Ohms


# Integrate data

dmm = []

with open(dmmInput) as file:
    for line in file:
        split = line.split(',')

        if len(split) >= 3 and split[0] != 'Index':
            t = float(split[1].replace('"', ''))
            V = float(split[2].replace('"', ''))
            dmm.append([t, V])

dmm = numpy.array(dmm)

smu = []

with open(smuInput) as file:
    for line in file:
        split = line.split(',')

        if len(split) >= 4 and split[0] != 'Index':
            t = float(split[1].replace('"', ''))
            V = float(split[2].replace('"', ''))
            I = float(split[3].replace('"', ''))
            smu.append([t, V, I])

smu = numpy.array(smu)

smuV = smu[:, 1]
smuI = smu[:, 2]
smuP = smuV * smuI

dmmV = []
dmmI = []

for i in range(smu.shape[0]):
    idx = numpy.argmin(numpy.abs(dmm[:, 0] - smu[i, 0]))
    dmmV.append(dmm[idx, 1])

dmmV = numpy.array(dmmV)
dmmI = dmmV / loadResistance
dmmP = dmmV * dmmI


# Plot

fig, ax1 = pyplot.subplots()
ax1.set_xlabel('Vin (V)')
ax1.set_ylabel('Efficiency (%)')
p1 = ax1.plot(smuV, 100. * dmmP / smuP)
ax1.set_xlim([4., 20.])
ax1.set_ylim([88., 93.])

ax2 = ax1.twinx()
ax2.set_ylabel('Voltage (V)')
p2 = ax2.plot(smuV, dmmV, 'C2')
ax2.set_ylim([0., 5.4])

ax1.legend(p1 + p2, ['Efficiency', 'Vout'], frameon = False)

pyplot.gcf().set_size_inches(12, 9)
pyplot.savefig(output, dpi = 300)

