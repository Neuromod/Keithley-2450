local I_overdrive = {:g}
local t_overdrive = {:g}
local t_cooling   = {:g}
local dV          = {:g}
local I_limit     = {:g}
local dt_sweep    = {:g}
local filterCount = {:d}


local function loopPrint(buffer, loopDelay)
    local index = 0
    while true
    do
        if index < buffer.n
        then
            index = index + 1
            print(string.format("%g,%g,%g", buffer.relativetimestamps[index], buffer.sourcevalues[index], buffer.readings[index]))
        else
            delay(loopDelay)
            if trigger.model.state() == trigger.STATE_IDLE
            then
               print("")
               break
            end
        end
    end
end


reset()

if I_overdrive != 0 and t_overdrive > 0
then
    smu.measure.func = smu.FUNC_DC_VOLTAGE                     -- default: smu.FUNC_DC_CURRENT
    smu.source.func = smu.FUNC_DC_CURRENT                      -- default: smu.FUNC_DC_VOLTAGE

    smu.source.level = I_overdrive                             -- default: 0

    trigger.model.setblock(1, trigger.BLOCK_SOURCE_OUTPUT, smu.ON)
    trigger.model.setblock(2, trigger.BLOCK_MEASURE_DIGITIZE, defbuffer1, trigger.COUNT_INFINITE)
    trigger.model.setblock(3, trigger.BLOCK_DELAY_CONSTANT, t_overdrive)
    trigger.model.setblock(4, trigger.BLOCK_MEASURE_DIGITIZE, defbuffer1, trigger.COUNT_STOP)
    trigger.model.setblock(5, trigger.BLOCK_SOURCE_OUTPUT, smu.OFF)
    trigger.model.initiate()
    loopPrint(defbuffer1, 0.25)

    defbuffer1.clear()
end

delay(t_cooling)

if dt_sweep < 0 
then
    dt_sweep = smu.DELAY_AUTO
end

local V_limit

if smu.interlock.tripped == smu.ON
then
    V_limit = 200
else
    V_limit = 20
end

smu.measure.func = smu.FUNC_DC_CURRENT
smu.source.func = smu.FUNC_DC_VOLTAGE

smu.measure.filter.count = filterCount                     -- default: 10
smu.measure.filter.enable = smu.ON                         -- default: smu.OFF
smu.measure.autorangelow = 100e-9                          -- default: 10e-9 A (for current)
smu.source.ilimit.level = I_limit                          -- default: 0
smu.source.sweeplinearstep("Sweep", 0, V_limit, dV, dt_sweep)

trigger.model.initiate()
loopPrint(defbuffer1, 0.25)
