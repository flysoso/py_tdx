# coding: utf8

import pickle
import matplotlib
import matplotlib.pyplot as plt
import numpy

def arr_save_to_file(arr, filename):
    outputfile = open(filename, 'wb')
    pickle.dump(arr, outputfile, -1)
    outputfile.close()

def load_arr_from_file(filename):
    outputfile = open(filename, 'rb')
    arr = pickle.load(outputfile)
    outputfile.close()
    return arr

def showPlot(arr):
    x = numpy.linspace(0, 10, 1000)
    y = numpy.sin(x)
    
    plt.plot(x,y)
    plt.show()

def loadArr():
    arr = load_arr_from_file('temp.arr')
    print arr[0]
    list1 = []
    for k in arr:
        list1.append([k[1],k[5],10])
    list1 = numpy.array(list1)
    print list1
    #showPlot(list1)


