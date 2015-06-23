import math

def delta_rate(dline, dday = 0):
    if dday == 0: dday = len(dline) + 1
    t1 = (dline[-1].op - dline[-dday].op) / dline[-dday].op
    return t1

def average(dline, dday = 0):
    if dday == 0: dday = len(dline) + 1
    sum = 0
    for k in dline[-dday-1:-1]:
        sum += k.op
    return sum / dday

def variance(dline, dday = 0):
    if dday == 0: dday = len(dline) + 1
    average1 = average(dline, dday)
    for k in dline[-dday-1: -1]:
        sumSquare = (k.op - average1) * (k.op - average1)
    sumSquare = sumSquare / dday
    return math.sqrt(sumSquare)

def delta_line(dline, dday = 0):
    if dday==0: dday = len(dline) + 1
    deltaline = []
    for k in range(-dday, -2):
        deltaline.append(dline[k] / dline[k+1])
    deltaline.append(1)
    return deltaline