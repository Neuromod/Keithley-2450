local V_charge     = {:g}                                  -- Capacitor charging voltage
local I_charge     = {:g}                                  -- Capacitor charging limit
local t_charge     = {:g}                                  -- Charged time
local t_discharge  = {:g}                                  -- Discharged time
local t_recover    = {:g}                                  -- Voltage recovery time
local autorangeLow = {:g}                                  -- Minimum current range
local filterCount  = {:d}                                  -- Parameter filter count


local function loopPrint(buffer, loopDelay)
    local index = 0
    while true
    do
        if index < buffer.n
        then
            index = index + 1
            print(string.format("%g,%g,%g,%s", defbuffer1.relativetimestamps[index], defbuffer1.sourcevalues[index], buffer.readings[index], defbuffer1.units[index]))
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

local iLimit

if V_charge <= 20.0
then
    iLimit = 1.0
else
    iLimit = 0.1
end

smu.measure.configlist.create("Measure")
smu.source.configlist.create("Source")

smu.measure.filter.count = filterCount                               -- default: 10
smu.measure.filter.enable = smu.ON                                   -- default: smu.OFF
smu.measure.autorangelow = autorangeLow                              -- default: 10e-9 (current)

smu.source.offmode = smu.OFFMODE_HIGHZ                               -- default: smu.OFFMODE_NORMAL
smu.source.highc = smu.ON                                            -- default: smu.OFF
smu.source.level = V_charge                                          -- default: 0
smu.source.ilimit.level = I_charge                                   -- default: 105 uA

smu.measure.configlist.store("Measure")                              -- Charge / discharge phases
smu.source.configlist.store("Source")                                -- Charge Phase

smu.source.level = 0
smu.source.ilimit.level = iLimit

smu.source.configlist.store("Source")                                -- Discharge Phase

smu.measure.func = smu.FUNC_DC_VOLTAGE                               -- default: smu.FUNC_DC_CURRENT
smu.source.func = smu.FUNC_DC_CURRENT                                -- default: smu.FUNC_DC_VOLTAGE

smu.measure.filter.count = filterCount                               -- default: 10
smu.measure.filter.enable = smu.ON                                   -- default: smu.OFF

smu.source.offmode = smu.OFFMODE_HIGHZ                               -- default: smu.OFFMODE_NORMAL
smu.source.highc = smu.ON                                            -- default: smu.OFF

smu.measure.configlist.store("Measure")                              -- Recover phase
smu.source.configlist.store("Source")                                -- Recover Phase


trigger.timer[1].delaylist = {{t_charge, t_discharge, t_recover}}    -- Default: 10e-6
trigger.timer[1].start.stimulus = trigger.EVENT_NOTIFY1              -- Default: trigger.EVENT_NONE
trigger.timer[1].count = 3                                           -- Default: 1 
trigger.timer[1].enable = trigger.ON                                 -- Default: trigger.OFF

trigger.model.setblock(1, trigger.BLOCK_CONFIG_RECALL, "Measure", 1, "Source", 1)
trigger.model.setblock(2, trigger.BLOCK_SOURCE_OUTPUT, smu.ON)
trigger.model.setblock(3, trigger.BLOCK_NOTIFY, trigger.EVENT_NOTIFY1)
trigger.model.setblock(4, trigger.BLOCK_MEASURE_DIGITIZE, defbuffer1, trigger.COUNT_INFINITE)
trigger.model.setblock(5, trigger.BLOCK_WAIT, trigger.EVENT_TIMER1, trigger.CLEAR_ENTER)

trigger.model.setblock(6, trigger.BLOCK_MEASURE_DIGITIZE, defbuffer1, trigger.COUNT_STOP)
trigger.model.setblock(7, trigger.BLOCK_CONFIG_RECALL, "Source", 2)
trigger.model.setblock(8, trigger.BLOCK_MEASURE_DIGITIZE, defbuffer1, trigger.COUNT_INFINITE)
trigger.model.setblock(9, trigger.BLOCK_WAIT, trigger.EVENT_TIMER1, trigger.CLEAR_ENTER)

trigger.model.setblock(10, trigger.BLOCK_MEASURE_DIGITIZE, defbuffer1, trigger.COUNT_STOP)
trigger.model.setblock(11, trigger.BLOCK_SOURCE_OUTPUT, smu.OFF)
trigger.model.setblock(12, trigger.BLOCK_CONFIG_RECALL, "Measure", 2, "Source", 3)
trigger.model.setblock(13, trigger.BLOCK_SOURCE_OUTPUT, smu.ON)
trigger.model.setblock(14, trigger.BLOCK_MEASURE_DIGITIZE, defbuffer1, trigger.COUNT_INFINITE)
trigger.model.setblock(15, trigger.BLOCK_WAIT, trigger.EVENT_TIMER1, trigger.CLEAR_ENTER)

trigger.model.setblock(16, trigger.BLOCK_MEASURE_DIGITIZE, defbuffer1, trigger.COUNT_STOP)
trigger.model.setblock(17, trigger.BLOCK_SOURCE_OUTPUT, smu.OFF)

trigger.model.initiate()
loopPrint(defbuffer1, 0.25)