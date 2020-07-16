import numpy
import matplotlib.pyplot as pyplot


# Settings

input  = '18650_SetupAndRawData.csv'
output = '18650.png'


# Code

battery = []

with open(input) as file:
    for line in file:
        split = line.split(',')

        if len(split) >= 2 and split[0] == 'TEST_PARAM.discharge_current:':
            dischargeCurrent = float(split[1])

        if len(split) >= 6 and split[0] == 'BATT_MODEL_RAW:' and split[1] != 'Index':
            battery.append([float(split[2]), float(split[3]), float(split[4]), float(split[5])])
        
battery = numpy.array(battery)

fig, ax1 = pyplot.subplots()
ax1.set_xlabel('Capacity (mAh)')
ax1.set_ylabel('Voltage (V)')
p1 = ax1.plot(battery[:, 0] * dischargeCurrent / 3.6, battery[:, 1])
p2 = ax1.plot(battery[:, 0] * dischargeCurrent / 3.6, battery[:, 2])

ax2 = ax1.twinx()
ax2.set_ylabel('Resistance (m$\Omega$)')
p3 = ax2.plot(battery[:, 0] * dischargeCurrent / 3.6, battery[:, 3] * 1000., 'C3')

ax1.legend(p1 + p2 + p3, ['$V_{oc}$', '$V_{load}$', 'ESR'], frameon = False)

pyplot.gcf().set_size_inches(12, 9)
pyplot.savefig(output, dpi = 300)
pyplot.clf()
