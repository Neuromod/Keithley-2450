-- Reset environment variables to the default
reset()

-- Set instrument as a voltage source (can be omitted as this is the default value)
smu.source.func = smu.FUNC_DC_VOLTAGE

-- Set the current limit to 1 A
smu.source.ilimit.level = 1

-- Set the source voltage to 10 V
smu.source.level = 10

-- Set measurement to current (can be omitted as this is the default value)
smu.measure.func = smu.FUNC_DC_CURRENT

-- Turn SMU output on
smu.source.output = smu.ON

-- Perform a single measurement
smu.measure.read()

-- Turn SMU output off
smu.source.output = smu.OFF

-- Read the measured voltage value
v = defbuffer1.sourcevalues[1]

-- Read the measured current value
i = defbuffer1.readings[1]

-- Print voltage in the first line of the user tab
display.settext(display.TEXT1,  string.format("Voltage: %.4f V", v))

-- Print resistance and power in the second line of the user tab 
display.settext(display.TEXT2,  string.format("R: %.3f \018, P: %.3f W", v / i, v * i))
