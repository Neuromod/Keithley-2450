local step = {:d}                                          -- Number of steps

reset()

smu.measure.func = smu.FUNC_DC_VOLTAGE                     -- override smu.FUNC_DC_CURRENT
smu.source.func = smu.FUNC_DC_CURRENT                      -- override smu.FUNC_DC_VOLTAGE

smu.source.output = smu.ON
local voc = smu.measure.read()
smu.source.output = smu.OFF

defbuffer1.clear()

smu.measure.func = smu.FUNC_DC_CURRENT
smu.source.func = smu.FUNC_DC_VOLTAGE
smu.source.ilimit.level = 1                                -- override the 100uA default
smu.source.sweeplinear("SolarCell", 0, voc, step)

trigger.model.initiate()
waitcomplete()

local voltage = defbuffer1.sourcevalues
local current = defbuffer1

local isc = current[1]
local pmax = voltage[1] * current[1]
local vmax = voltage[1]
local imax = current[1]

for i = 1, step 
do
    if voltage[i] * current[i] < pmax
    then
        pmax = voltage[i] * current[i]
        imax = current[i]
        vmax = voltage[i]
    end
end

print(voc)
print(math.abs(isc))
print(vmax)
print(math.abs(imax))
