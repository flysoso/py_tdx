
#coding: utf8

import tdx2
import math

qlist = []

def wattIndex(dline):
    return 0

def delta_d1(dline, pd, preday=0):
    ud = [0 for k in range(pd)]
    for k in range(pd):
        ud[k] = dline[-1-preday -pd+k].cl
    for k in range(pd-1):
        ud[k] = ud[k+1]-ud[k]
    for k in range(pd-1):
        if ud[k] > ud[k+1]: return 0
    return 1

def variance(dline, tlength, preday=0):
    st = len(dline) - preday - tlength
    en = len(dline) - preday
    avrg = average(dline, tlength, preday)
    ssum = 0
    for k in dline[st:en]:
        ssum += math.pow(k.cl - avrg,2)
    ssum = math.sqrt(ssum / (en-st))
    return ssum

def average(dline, tlength, preday=0):
    sum = 0
    st = len(dline) - preday - tlength
    en = len(dline) - preday
    for k in dline[st:en]:
        sum += k.cl
    return float(sum) / tlength

def tdx_delta(fid, preday):
    return snm.get_tdx_delta(fid)

def fast_grow(dline, daylength, preday):
    st = len(dline) - daylength - preday
    en = len(dline) - preday
    maxr = -9999
    for k in range(st+3,en):
        a = dline[k].cl 
        b = dline[k-3].cl
        if (a-b)/b > maxr:
            maxr = (a-b)/b
    return maxr*100

def fast_fall(dline, daylength, preday):
    st = len(dline) - daylength - preday
    en = len(dline) - preday
    minr = 9999
    for k in range(st+3,en):
        a = dline[k].cl 
        b = dline[k-3].cl
        if (a-b)/b < minr:
            minr = (a-b)/b
    return minr*100

def delta_ratio_reverse(dline, daylength, preday):
    
    # delta_ratio(-30, -1)
    a = dline[-1-preday].cl
    if -1-preday-daylength < -len(dline): return 0
    b = dline[-1-preday-daylength].cl
    return (float(a-b)/b*100)

def get_last_dline_ftime(dline, preday=0):
    return tdx2.parse_time_reverse(dline[-1-preday].ftime+1)

def reInit():
    snm.reInit()


class StNameManager():
    def __init__(self):
        self.reInit()
    def reInit(self):
        f = open(u'C:\\new_tdx\\T0002\\export\\深沪Ａ股.TXT', 'r')
        qlist = []
        for k in range(9999):
            s = f.readline()
            if not s: break
            s = s.split('\t')
            qlist.append(s)
        self.qlist = qlist
            
    def get_stname(self, fid):
        if len(fid)==12: fid = fid[2:8]
        for k in self.qlist:
            if k[0] == fid:
                return k[1] + ('=' + k[3]).encode('utf8')
        return 'na'
    def get_tdx_delta(self, fid):
        if len(fid)==12: fid = fid[2:8]
        for k in self.qlist:
            if k[0] == fid:
                try:
                    return float(k[2])
                except:
                    print 'tdx_data,', k[2],'not float'
                    return -99
        return -99
            
def get_stname(fid):
   return snm.get_stname(fid)

snm = StNameManager()

if __name__ == '__main__':
    #print get_stname('sh000001.day')
    dl = tdx2.get_dayline_by_fid('sz002245', restrictSize=30)
    print len(dl)
    print fast_fall(dl, 30, 0)