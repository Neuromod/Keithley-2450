def metric(value, digit, unit, plus = False):
    factor = [1E24, 1E21, 1E18, 1E15, 1E12, 1E9, 1E6, 1E3, 1, 1E-3, 1E-6, 1E-9, 1E-12, 1E-15, 1E-18, 1E-21, 1E-24]
    prefix = ['Y', 'Z', 'E', 'P', 'T', 'G', 'M', 'k', '', 'm', '\u00B5', 'n', 'p', 'f', 'a', 'z', 'y']

    if plus:
        plusString = '+'
    else:
        plusString = ''

    if value < 0:
        sign = -1.0
    else:
        sign = 1.0

    value = abs(value)

    if value == 0:
        i = 8
    else:
        for i in range(len(factor)):
            if value >= factor[i]:
                value /= factor[i]
                break

    if value >= 100.0:
        decimal = digit - 3
    elif value >= 10.0:
        decimal = digit - 2
    else:
        decimal = digit - 1

    return '{{:{:s}.{:d}f}} {{:s}}{{:s}}'.format(plusString, decimal).format(sign * value, prefix[i], unit)
