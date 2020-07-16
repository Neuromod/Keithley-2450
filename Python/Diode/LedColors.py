import numpy
import matplotlib.pyplot as pyplot
import matplotlib.lines as lines


# Settings

input  = ['LED IR ({:d}).csv', 'LED Red ({:d}).csv', 'LED Orange ({:d}).csv', 'LED Yellow ({:d}).csv', 'LED Green ({:d}).csv', 'LED White ({:d}).csv']
output = 'LedColors.png'
nLed   = 8

inputLabel = ['IR', 'Red', 'Orange', 'Yellow', 'Green', 'White']
inputColor = ['k', 'tab:red', 'tab:orange', 'y', 'tab:green', 'grey']


# Code

color = []

for filename in input:
    run = []

    start  = None
    stop   = None
    points = None
    limit  = None

    for i in range(nLed):
        led = []
        with open(filename.format(i + 1)) as file:
            for line in file:
                split = line.split(',')

                if len(split) == 2:
                    if split[0] == '\t...Start':
                        value = float(split[1].replace('V', ''))
                        if start == None:
                            start = value
                        else:
                            if start != value:
                                print('Start parameter mismatch: {:g} != {:g}'.format(value, start))
                                quit()

                    if split[0] == '\t...Stop':
                        value = float(split[1].replace('V', ''))
                        if stop == None:
                            stop = value
                        else:
                            if stop != value:
                                print('Stop parameter mismatch: {:g} != {:g}'.format(value, stop))
                                quit()

                    if split[0] == '\t...Points':
                        value = float(split[1])
                        if points == None:
                            points = value
                        else:
                            if points != value:
                                print('Start parameter mismatch: {:g} != {:g}'.format(value, points))
                                quit()

                    if split[0] == '\t...Limit':
                        value = float(split[1].replace('A', ''))
                        if limit == None:
                            limit = value
                        else:
                            if limit != value:
                                print('Start parameter mismatch: {:g} != {:g}'.format(value, limit))
                                quit()

                if len(split) >= 3 and split[0] != 'Index':
                    V = float(split[2].replace('"', ''))
                    I = float(split[3].replace('"', ''))

                    if (limit - I) < limit * 0.0001:
                        break

                    led.append([V, I])

        run.append(numpy.array(led))
    color.append(run)


for c in range(len(input)):
    for i in range(nLed):
        pyplot.semilogy(color[c][i][:, 0], color[c][i][:, 1], color = inputColor[c])

pyplot.grid(True, axis = 'y', which = "both", ls="-", color = '0.75')


tickValues = [1, 100e-3, 10e-3, 1e-3, 100e-6, 10e-6, 1e-6, 100e-9, 10e-9, 1e-9, 100e-12, 10e-12, 1e-12, 100e-15, 10e-15, 1e-15]
tickUnits  = ['1A', '100 mA', '10 mA', '1 mA', '100 \u00B5A', '10 \u00B5A', '1 \u00B5A', '100 nA', '10 nA', '1 nA', '100 pA', '10 pA', '1 pA', '100 fA', '10 fA', '1 fA']
pyplot.yticks(tickValues, tickUnits)

pyplot.ylim([1E-11, 0.1])
pyplot.xlim([0, 3.25])
        
pyplot.xlabel('Voltage (V)')
pyplot.ylabel('Current')

pyplot.legend([lines.Line2D([0], [0], color = c, lw = 1.5) for c in inputColor], inputLabel, frameon = False)

pyplot.gcf().set_size_inches(12, 9)
pyplot.savefig(output, dpi = 150)
