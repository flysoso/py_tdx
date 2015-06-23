import pickle_util
import watterson_analysis
from numpy import array

def echoGraph():
    
    dataList = pickle_util.load_arr_from_file('temp.arr')
    arr = []
    for k in dataList:
        # (0)id (1)d5 (2)d10 (3)d15 (4)d1 (5)ma20 (6)lastCL (7)watIndex (8)rd1 (9)lastTime (10) name
        arr.append([k[7], k[8], k[6]])
    arr = array(arr)
    watterson_analysis.showPlotExtend(arr, ddta = 5, hideDot = 1, restrict_cl = (0,9999))
    
if __name__ == '__main__':
    echoGraph()