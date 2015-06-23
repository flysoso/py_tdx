#coding: utf8

import wx
import random
import watterson_lib
import tdx2
import afunc
import watterson_analysis
from numpy import *
import math

import pickle
import sys

class ConfigureManager:
    def __init__(self):
        self.configDict = {}
    def getConfig(self, para):
        return self.configDict[para]
    def setConfig(self, para, val):
        self.configDict[para] = val

cm = ConfigureManager()

cm.setConfig('INIT_POW',                [1000,100] + [0 for k in range(36)])
cm.setConfig('MAX_LOAD_ITEM',           7777)
cm.setConfig('FILTER1',                 1)
cm.setConfig('FILTER2',                 1)
cm.setConfig('FILTER3',                 1)
cm.setConfig('TEST_MODE',               1)
cm.setConfig('PRE_DAY',                 2)
cm.setConfig('PRE_DAY_CHECK_DAY',       2)


class MessageManager:
    def __init__(self, lbl):
        self.lbl = lbl
    def ShowMessage(self, str):
        self.lbl.SetLabel(str)

def arr_save_to_file(arr, filename):
    outputfile = open(filename, 'wb')
    pickle.dump(arr, outputfile, -1)
    outputfile.close()

def load_arr_from_file(filename):
    outputfile = open(filename, 'rb')
    arr = pickle.load(outputfile)
    outputfile.close()
    return arr

for k in sys.argv:
    if k=='-full':
        cm.setConfig('MAX_LOAD_ITEM',       7777)
    if k=='-test':
        cm.setConfig('TEST_MODE',           1)
    if k=='-real':
        cm.setConfig('TEST_MODE',          0)
    if k[:5] == '-pre=':
        cm.setConfig('PRE_DAY',             float(k[5:]))

varname = ['ID', 'd5', 'd10','d15', 'd1', 'ma20', 'last_cl', \
           'wattIndex','rd1','lastTime', 'name', 'd30',\
            'variance', 'd180', 'fast_grow', 'fast_fall', 'tdx_delta', 'delta_d1']
cm.setConfig('varname', varname)

def config_varfunc():

    if cm.getConfig('TEST_MODE'):
        PRE_DAY = cm.getConfig('PRE_DAY')
    else:
        PRE_DAY = 0
    
    varname = cm.getConfig('varname')
    
    varfunc = [lambda dl, sfid: sfid,                                                   \
            lambda dl, sfid: watterson_lib.delta_ratio_reverse(dl, 5, PRE_DAY),         \
            lambda dl, sfid: watterson_lib.delta_ratio_reverse(dl, 10,PRE_DAY),         \
            lambda dl, sfid: watterson_lib.delta_ratio_reverse(dl, 15,PRE_DAY),         \
            lambda dl, sfid: watterson_lib.delta_ratio_reverse(dl, 1,PRE_DAY),          \
            lambda dl, sfid: float('%.2f'%watterson_lib.average(dl, 20, PRE_DAY)),      \
            lambda dl, sfid: dl[-1-PRE_DAY].cl,                                         \
            lambda dl, sfid: 'LV2 ratio',                                               \
            lambda dl, sfid: get_rd1(dl, sfid),                                         \
            lambda dl, sfid: watterson_lib.get_last_dline_ftime(dl,PRE_DAY),            \
            lambda dl, sfid: watterson_lib.get_stname(sfid),                            \
            lambda dl, sfid: watterson_lib.delta_ratio_reverse(dl, 30, PRE_DAY),        \
            lambda dl, sfid: watterson_lib.variance(dl, 30, PRE_DAY),                   \
            #lambda dl, sfid: watterson_lib.delta_ratio_reverse(dl, 180, PRE_DAY),      \
            lambda dl, sfid: 0,                                                         \
            lambda dl, sfid: watterson_lib.fast_grow(dl, 30, PRE_DAY),                  \
            lambda dl, sfid: watterson_lib.fast_fall(dl, 30, PRE_DAY),                  \
            lambda dl, sfid: watterson_lib.tdx_delta(sfid, PRE_DAY),\
            lambda dl, sfid: watterson_lib.delta_d1(dl,4,PRE_DAY)]
    
    cm.setConfig('varname', varname)
    cm.setConfig('varfunc', varfunc)


'''
    dratio(dl,time1, time2) = op(time2) - op(time1+time2)
    (x1,y1) = op(-5) - op(-5-15)
    (x,y) = op(-5+PRD) - op(-5)
          = op(y) - op(x+y)
          
    -5 = -PRE_DAY-1    # PRE_DAY = 4, MEAN -1,-2,-3,-4

'''


def get_rd1(dl ,sfid):
    if cm.getConfig('TEST_MODE'):
        PD = cm.getConfig('PRE_DAY')
        PRD = cm.getConfig('PRE_DAY_CHECK_DAY')
        return watterson_lib.delta_ratio_reverse(dl,PRD,PD-PRD)
    else:
        return '_'

def strr(k):
    if type(k) is str:
        return k
    else:
        try:
            return str(k)
        except:
            return 'ERR'

def insertItem(lc, arr):
    index = lc.InsertStringItem(555, strr(arr[0]))
    for k in range(0, len(arr)):
        lc.SetStringItem(index, k, strr(arr[k]))

def CreateDataList(dlinelist):
    config_varfunc()
    datalist = []
    for item in dlinelist:
        dline = item[1]
        k = item[0]
        if cm.getConfig('FILTER3'):
            if dline[-1].op > 60: continue
        if len(dline) < 30: continue
        dataItem = [func(dline,k) for func in cm.getConfig('varfunc')]
        datalist.append(dataItem)
    return datalist


def expd_func(k):
    if k<0: return math.exp(k)
    else: return k+1
def expd_closeTo0(k):
    return math.exp(-abs(k))

def CalculateLv2Extend(k, pow = 0):
    '''
    This is the KEY !!!!!!
varname = ['ID', 'd5', 'd10','d15',
             'd1', 'ma20', 'last_cl', \
           'wattIndex','rd1','lastTime', 'name',
            'd30','variance', 'd180', 'fast_grow',
             'fast_fall', 'tdx_delta', 'delta_d1']
    '''
    if pow==0: pow=cm.getConfig('INIT_POW')
    if k[6] == 0: return 0,0,0
    expd = lambda x:x
    #expd = expd_func
    d = [0 for t in range(10)]
    
    # ma20 - cl
    d[0] = expd((k[5] - k[6])/k[5]) * pow[0]
    # 势能
    d[1] = expd((-k[1]/10.0/5 * 5 -k[2]/10.0/10.0 - k[3]/10.0/15 ))* pow[1]
    # 一日势能
    d[2] = expd(-k[4]/10) * pow[2]
    # 波动股接近度
    d[3] = expd( expd_closeTo0(k[11]) * k[12] ) * pow[3]
    # 变权势能 1,2,3
    d[4] = expd(  -k[1]/5 -k[2]/10*2 -k[3]/15*3   ) * pow[4]/10
    # d30 势能
    d[5] = expd(  -k[11]/30   ) * pow[5]
    # 涨幅微分
    d[6] = k[17] * pow[6]
    
    ssum = 0
    sstr = ''
    ind = 0
    for k in d:
        ssum += k
        ind += 1
        sstr += str(ind) + '\n\t' + str(k) + '\n'
    sstr += 'Total=' + repr(ssum)
    return ssum, sstr

class CommonFrame(wx.Frame):
    def __init__(self):
        
        # Generate Frame
        
        wx.Frame.__init__(self, None, -1, 'Watterson the Manager', 
                size=(1900, 1000),
                style = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX  |wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        
        MVW = 100
        MTH = 0
        
        listctrl = wx.ListCtrl(panel, -1, size=(1000 + MVW,920), pos=(30,20),style=wx.LC_REPORT)
        self.pageScroll     = wx.ScrollBar(panel, -1, size = (300, 30), pos=(1060 + MVW, 20))
        self.pageLabel      = wx.StaticText(panel, -1, "PAGE=",  size=(300,30), pos=(1060 + MVW,60))
        self.sText          = wx.TextCtrl(panel, -1, "", size=(600,400 + MTH), pos=(1060 + MVW, 100), style = wx.TE_MULTILINE)
        self.btnAnalysis    = wx.Button(panel, -1, "PLOT", size=(120,40), pos = (1060+MVW, 520+MTH))
        self.btnExportData  = wx.Button(panel, -1, "EXPORT_DATA", size=(120,40), pos = (1200+MVW, 520+MTH))
        if cm.getConfig('TEST_MODE'): s='toREAL'
        else: s='toTEST'
        self.btnTurnMode    = wx.Button(panel, -1, s, size=(120,40), pos = (1400+MVW,20))
        
        self.btnApply       = wx.Button(panel, -1, "ApplyPow", size=(120,40), pos=(1060+MVW+200, 580+MTH))
        self.textPow        = wx.TextCtrl(panel, -1, str(cm.getConfig('INIT_POW')), size=(180, 40), pos=(1060+MVW, 580+MTH))
        self.lblMsg         = wx.StaticText(panel, -1, 'HAHA', size=(600,40), pos=(1060+MVW, 650+MTH))
        
        self.btnAnalysis.Bind(wx.EVT_BUTTON, self.OnAnalysisClick)
        self.btnExportData.Bind(wx.EVT_BUTTON, self.OnExportClick)
        self.btnApply.Bind(wx.EVT_BUTTON, self.OnApplyPowClick)
        self.btnTurnMode.Bind(wx.EVT_BUTTON, self.OnTurnModeClick)
        
        self.pageScroll.SetScrollbar(0,100,1100,50)
        self.pageScroll.Bind(wx.EVT_SCROLL_CHANGED, self.OnScrollMove)
        
        varlist = cm.getConfig('varname')
        columnIndex = 0
        for i in varlist:
            listctrl.InsertColumn(9999, i + '_'+str(columnIndex));
            columnIndex+=1
        
        listctrl.SetColumnWidth(0, 140)
        listctrl.SetColumnWidth(listctrl.GetColumnCount()-2, 140)
        listctrl.SetColumnWidth(listctrl.GetColumnCount()-1, 140)
            
        listctrl.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)
        listctrl.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.OnItemClick)
        
        self.listctrl = listctrl
        
        self.powConfig = cm.getConfig('INIT_POW')
        self.isReverse = True
        
        # Push Data
        
        tdx2.SetPath('Z:\\vipdoc', 'tdxpath')
        
        self.msgManager = MessageManager(self.lblMsg)
        self.LoadFile()
        self.Center()
    
    def OnExportClick(self, event):
        arr_save_to_file(self.dataList, 'temp.arr')
        self.msgManager.ShowMessage('Exported.')
        
    def OnApplyPowClick(self, event):
        sr = self.textPow.GetValue().replace('[', '').replace(']','')
        sr = sr.split(',')
        qr = [0 for k in range(36)]
        for k in range(min(36,len(sr))):
            qr[k] = float(sr[k])
        self.powConfig = qr
        
        self.CalculateLv2(self.dataList)
        self.ListControlRefresh()
    
    def OnAnalysisClick(self, event):
        if not cm.getConfig('TEST_MODE'):
            self.msgManager.ShowMessage("THIS IS FOR TEST MODE ONLY") 
            return
        arr = []
        for k in self.dataList:
            # (0)id (1)d5 (2)d10 (3)d15 (4)d1 (5)ma20 (6)lastCL (7)watIndex (8)rd1 (9)lastTime (10) name
            arr.append([k[7], k[8], k[6]])
        arr = array(arr)
        watterson_analysis.showPlot(arr)
    def LoadFile(self):
        # get list
        flist = tdx2.get_file_list()
        self.msgManager.ShowMessage('total file count:'+ str(len(flist)))
        flist = flist[:cm.getConfig('MAX_LOAD_ITEM')]
        
        # filter_2
        rflist = []
        for k in flist:
            if cm.getConfig('FILTER1'):
                if k[:3] == "sh0": continue
                if k[:3] == "sh1": continue
                if k[:3] == "sh2": continue
                if k[:3] == "sh3": continue
                if k[:3] == "sh5": continue
                if k[:3] == "sh8": continue
            #if k[:3] == "sh5": continue
            rflist.append(k)
            
        flist = rflist
        
        # read file main
        gauage = 0
        dlinelist = []
        for k in flist:
            dline = tdx2.get_dayline_by_fid(k, restrictSize = 40)
            dlinelist.append([k,dline])
            gauage+=1
            if gauage%100 == 0: print gauage / 33, '%'
        self.dlinelist = dlinelist
        self.LoadProcess()
    def LoadProcess(self):
        datalist = CreateDataList(self.dlinelist)
        # filter
        maxd = 0
        for k in range(min(999,len(datalist))): maxd = max(datalist[k][9], maxd)
        if cm.getConfig('FILTER2'):
            filteredList = []
            for k in datalist:
                if k[9] != maxd: continue
                if k[10] == 'na': continue
                filteredList.append(k)
            datalist = filteredList

        self.dataList = datalist
        self.CalculateLv2(datalist)
        self.msgManager.ShowMessage('data loading finished')
        
        watterson_lib.reInit()

        self.ListControlRefresh()
        
    def CalculateLv2(self, dataList):
  
        for k in dataList:
            condata = CalculateLv2Extend(k, self.powConfig)
            k[7] = condata[0]
            
    def OnColClick(self,event):
        self.pageScroll.SetThumbPosition(0)
        srtIndex = event.GetColumn()
        self.isReverse = not self.isReverse
        self.dataList.sort(key = lambda x: x[srtIndex], reverse = self.isReverse)
        self.ListControlRefresh()
    def OnTurnModeClick(self, event):
        if cm.getConfig('TEST_MODE'):
            cm.setConfig('TEST_MODE', 0) # turn to real mode
            self.LoadProcess()
            self.btnTurnMode.SetLabel("toTEST")
        else:
            cm.setConfig('TEST_MODE', 1) # turn to test mode
            self.LoadProcess()
            self.btnTurnMode.SetLabel("toREAL")
    def OnItemClick(self, event):
        for k in self.dataList:
            if k[0] == self.listctrl.GetItemText(self.listctrl.GetFocusedItem()):
                ls, mstr = CalculateLv2Extend(k, self.powConfig)
                self.sText.SetValue(k[0] + '\n'+mstr)
    def ListControlRefresh(self):
        self.msgManager.ShowMessage('Refresh')
        self.listctrl.DeleteAllItems()
        p=self.pageScroll.GetThumbPosition()
        self.pageLabel.SetLabel("PAGE=%d"%p)
    
        for k in self.dataList[p*36:36+p*36]:
            insertItem(self.listctrl, k)

        #wx.Event().GetEventObject()
    def OnScrollMove(self, event):
        sstr= 'page=' + str(event.GetEventObject().GetThumbPosition())
        self.msgManager.ShowMessage(sstr)
        self.ListControlRefresh()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    CommonFrame().Show()
    app.MainLoop()  