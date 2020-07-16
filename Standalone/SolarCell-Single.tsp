-- Convert numbers to metric notation
local function metric(value, digit, unit)
    value = math.abs(value)

    local prefix = ""

    if value < 1
    then 
        if value >= 1E-3
        then
            value = value * 1E3
            prefix = "m"
        elseif value >= 1E-6
        then
            value = value * 1E6
            prefix = "\20"
        elseif value >= 1E-9
        then
            value = value * 1E9
            prefix = "n"
        elseif value >= 1e-12
        then
            value = value * 1E12
            prefix = "p"
        elseif value >= 1e-15
        then
            value = value * 1E15
            prefix = "f"
        end
    end

    local floatFormat

    if value >= 100
    then
        floatFormat = string.format("%%.%if", digit - 3) 
    elseif value >= 10
    then
        floatFormat = string.format("%%.%if", digit - 2)
    else
        floatFormat = string.format("%%.%if", digit - 1)
    end

    return string.format(floatFormat..prefix..unit, value)
end

reset()
display.clear()

local step = display.input.number("Sweep steps", display.NFORMAT_INTEGER, 100, 10, 1000)

if step != nil 
then
    smu.measure.func = smu.FUNC_DC_VOLTAGE                 -- override smu.FUNC_DC_CURRENT
    smu.source.func = smu.FUNC_DC_CURRENT                  -- override smu.FUNC_DC_VOLTAGE

    smu.source.output = smu.ON
    local voc = smu.measure.read()
    smu.source.output = smu.OFF

    defbuffer1.clear()

    smu.measure.func = smu.FUNC_DC_CURRENT
    smu.source.func = smu.FUNC_DC_VOLTAGE

    smu.source.ilimit.level = 1                            -- override the 100uA default
    smu.source.sweeplinear("SolarCell", 0, voc, step)

    trigger.model.initiate()

    while defbuffer1.n < step
    do
        delay(0.2)
        display.settext(display.TEXT1, string.format("Sample: %i / %i", defbuffer1.n, step))
    end

    waitcomplete()

    local voltage = defbuffer1.sourcevalues
    local current = defbuffer1.readings

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
   
    display.changescreen(display.SCREEN_USER_SWIPE)
    display.settext(display.TEXT1, string.format("OC %s, SC %s", metric(voc, 3, "V"), metric(isc, 3, "A")))
    display.settext(display.TEXT2, string.format("Max %s (%s x %s)", metric(pmax, 3, "W"), metric(vmax, 3, "V"), metric(imax, 3, "A")))
end
