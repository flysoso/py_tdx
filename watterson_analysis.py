#coding: utf8

import matplotlib
import matplotlib.pyplot as plt
from numpy import *
import watterson_analysis_echo as WAE

def getFrequencyPlot(arrPl, average, wat_dta = 5, restrict_cl = (0,9999)):
    print arrPl.shape
    # define
    
    rng = (-2000,2000)
    st = rng[0] / wat_dta
    en = rng[1] / wat_dta
    arrlength = int(en - st)
    
    # get frequency array
    
    q = [[0,0] for k in range(arrlength)]
    cl_sum = [0 for k in range(arrlength)]
    cl_count = [0 for k in range(arrlength)]
    is_bigger = 0
    
    for k in arrPl:
        wat, dt, cl = k
        if cl < restrict_cl[0]: continue
        if cl > restrict_cl[1]: continue
        if dt > 19: continue # 忽略涨停

        ind = int((wat - rng[0])/wat_dta)
        q[ind][is_bigger]+=1
        cl_sum[ind] += dt
        cl_count[ind] += 1
    
    # frequency to array
    
    xArr, yArr = [], []
    y2Arr = []
    for k in range(len(q)):
        x = (k + st) * wat_dta
        a,b = q[k]
        
        '''
        if a+b == 0:
            y = 0
        else:
            y = (a/float(a+b) - 0.5) * 10
        y += average
        '''
        
        if cl_count[k] != 0:
            y = cl_sum[k] / float(cl_count[k])
        else:
            y = average
        y2 = cl_count[k]
        
        xArr.append(x)
        yArr.append(y)
        y2Arr.append(y2)
        
    return xArr, yArr, y2Arr

def getAveragePlot(arrPl):
    count = 0
    sum = 0
    for k in arrPl:
        sum += k
        count += 1
    average = sum / count
    return average

def showPlot(arr, ddta = 5):
    fig =  plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(arr[:,0], arr[:,1], 20, arr[:,2])
    average = getAveragePlot(arr[:,1])
    ax.plot([-2000, 2000],[average, average], 'Green')
    tar = getFrequencyPlot(arr[:,0:2], average, wat_dta = ddta)
    ax.plot(tar[0], tar[1])
    plt.show()

def showPlotExtend(arr, ddta = 5, hideDot = 0, restrict_cl = (0,9999)):
    fig =  plt.figure()
    ax = fig.add_subplot(111)
    if not hideDot:
        ax.scatter(arr[:,0], arr[:,1], 20, arr[:,2])
    average = getAveragePlot(arr[:,1])
    ax.plot([-2000, 2000],[average, average], 'Green')
    x, y1, y2 = getFrequencyPlot(arr, average, wat_dta = ddta, restrict_cl = restrict_cl)
    ax.plot(x, y1)
    ax.plot(x, y2)
    plt.show()

    
if __name__=='__main__':
    WAE.echoGraph()