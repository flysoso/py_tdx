
import wx
import random
import watterson_lib
import tdx2
import afunc
import watterson_analysis
from numpy import *

import pickle

def arr_save_to_file(arr, filename):
    outputfile = open(filename, 'wb')
    pickle.dump(arr, outputfile, -1)
    outputfile.close()

def load_arr_from_file(filename):
    outputfile = open(filename, 'rb')
    arr = pickle.load(outputfile)
    outputfile.close()
    return arr

wordlist = []

INIT_POW = [100,200,300]
MAX_LOAD_ITEM = 3000
FILTER1 = 1     # filename head excepting: sh0 sh1 sh2 sh5 sh8
FILTER2 = 1     # last date is max
FILTER3 = 1     # dline[-1].op < 60

varlist = ['d5', 'd10','d15', 'd1', 'ma20']
varfunc = [ lambda dl: watterson_lib.delta_ratio(dl, -5), \
        lambda dl: watterson_lib.delta_ratio(dl, -10), \
        lambda dl: watterson_lib.delta_ratio(dl, -15), \
        lambda dl: watterson_lib.delta_ratio(dl, -1), \
        lambda dl: float('%.2f'%afunc.average(dl, 20))]
varfunc_testMode = [ lambda dl: watterson_lib.delta_ratio(dl, -5, -3), \
        lambda dl: watterson_lib.delta_ratio(dl, -10,-3), \
        lambda dl: watterson_lib.delta_ratio(dl, -15,-3), \
        lambda dl: watterson_lib.delta_ratio(dl, -1,-3), \
        lambda dl: float('%.2f'%afunc.average(dl, 20))]

TESTMODE=1

if TESTMODE:
    varfunc = varfunc_testMode

def extendColumn(vName, vFunc):
    print 'ext'
    global varlist, varfunc
    varlist.append(vName)
    varfunc.append(vFunc)

def strr(k):
    if type(k) is str:
        return k
    else:
        return str(k)

def insertItem(lc, arr):
    index = lc.InsertStringItem(555, strr(arr[0]))
    for k in range(1, len(arr)):
        lc.SetStringItem(index, k, strr(arr[k]))
        
def CalculateLv2Extend(k, pow = 0):
    '''
    This is the KEY !!!!!!
        # struct of dataList[i], i=0,1,2...
        # (0)name(1)d5(2)d10,(3)d15,(4)d1,(5)ma20,(6)lastCL,(7)watIndex,(8)Last
    '''
    if pow==0: pow=INIT_POW
    if k[5] == 0: return 0,0,0
    dm = (k[5] - k[6])/k[5] * pow[0]
    rm = -k[4]/10           * pow[1]
    um = (-k[1]/10/5 * 5 -k[2]/10/10 - k[3]/10/15 )* pow[2]
    return dm+um, '\n\md20_dec',dm, 'd1', um, 'd5,d10,d15', rm

class CommonFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Watterson the Manager', 
                size=(1900, 1000),
                style = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX  |wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        
        MVW = 100
        MTH = 0
        lc = wx.ListCtrl(panel, -1, size=(1000 + MVW,900), pos=(30,20),style=wx.LC_REPORT)
        self.pageScroll     = wx.ScrollBar(panel, -1, size = (300, 30), pos=(1060 + MVW, 20))
        self.pageLabel      = wx.StaticText(panel, -1, "PAGE=",  size=(300,30), pos=(1060 + MVW,60))
        self.sText          = wx.TextCtrl(panel, -1, "", size=(600,400 + MTH), pos=(1060 + MVW, 100), style = wx.TE_MULTILINE)
        self.btnAnalysis    = wx.Button(panel, -1, "PLOT", size=(120,40), pos = (1060+MVW, 520+MTH))
        self.btnExportData    = wx.Button(panel, -1, "EXPORT_FORM", size=(120,40), pos = (1200+MVW, 520+MTH))
        
        self.btnApply       = wx.Button(panel, -1, "ApplyPow", size=(120,40), pos=(1060+MVW+200, 580+MTH))
        self.textPow        = wx.TextCtrl(panel, -1, str(INIT_POW), size=(180, 40), pos=(1060+MVW, 580+MTH))
        
        self.btnAnalysis.Bind(wx.EVT_BUTTON, self.OnAnalysisClick)
        self.btnExportData.Bind(wx.EVT_BUTTON, self.OnExportClick)
        self.btnApply.Bind(wx.EVT_BUTTON, self.OnApplyPowClick)
        
        self.pageScroll.SetScrollbar(0,100,1100,50)
        self.pageScroll.Bind(wx.EVT_SCROLL_CHANGED, self.OnScrollMove)
        
        tdx2.SetPath('Z:\\vipdoc', 'tdxpath')
        
        extendColumn('lastCL' ,lambda dline: dline[-1].cl)
        extendColumn('wattIndex' ,lambda dl: watterson_lib.wattIndex(dl))
        extendColumn('lastTime' ,lambda dl: watterson_lib.get_last_dline_ftime(dl))
        
        if TESTMODE:
            extendColumn('rd1' ,lambda dl: watterson_lib.delta_ratio(dl,-2,-1))
        
        lc.InsertColumn(9999, "ID");
        for i in varlist:
            lc.InsertColumn(9999, i);
        
        lc.SetColumnWidth(0, 140)
        lc.SetColumnWidth(lc.GetColumnCount()-2, 140)
        lc.SetColumnWidth(lc.GetColumnCount()-1, 140)
            
        lc.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)
        lc.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.OnItemClick)
        
        self.lc = lc
        
        self.powConfig = INIT_POW
        self.isReverse = True
        
        self.LoadFile()
        self.ListControlRefresh()
        self.Center()
    
    def OnExportClick(self, event):
        arr_save_to_file(self.dataList, 'temp.arr')
        
    def OnApplyPowClick(self, event):
        sr = self.textPow.GetValue().replace('[', '').replace(']','')
        sr = sr.split(',')
        if len(sr)<3:
            print 'Not Enough RR'
            return
        for k in range(len(sr)):
            sr[k] = float(sr[k])
        self.powConfig = sr
        
        self.CalculateLv2(self.dataList)
        self.ListControlRefresh()
    
    def OnAnalysisClick(self, event):
        arr = []
        for k in self.dataList:
            arr.append([k[7], k[9]])
        arr = array(arr)
        watterson_analysis.showPlot(arr)
    def LoadFile(self):
        flist = tdx2.get_file_list()
        print 'total file count:', len(flist)
        flist = flist[:MAX_LOAD_ITEM]
        
        # filter 2
        rflist = []
        for k in flist:
            if FILTER1:
                if k[:3] == "sh0": continue
                if k[:3] == "sh1": continue
                if k[:3] == "sh2": continue
                if k[:3] == "sh3": continue
                if k[:3] == "sh5": continue
                if k[:3] == "sh8": continue
            #if k[:3] == "sh5": continue
            rflist.append(k)
            
        flist = rflist
        
        datalist = []
        dataItem = []
        for k in flist:
            dline = tdx2.get_dayline_by_fid(k, restrictSize = 30)
            if FILTER3:
                if dline[-1].op > 60: continue
            if len(dline) < 30: continue
            print 'loading', k
            dataItem = [k] + [k(dline) for k in varfunc]
            datalist.append(dataItem)

        self.CalculateLv2(datalist)
        
        print 'data loading finished'
        self.unfilteredList = datalist
    def CalculateLv2(self, dataList):
  
        for k in dataList:
            condata = CalculateLv2Extend(k, self.powConfig)
            k[7] = condata[0]
            
    def OnColClick(self,event):
        self.pageScroll.SetThumbPosition(0)
        srtIndex = event.GetColumn()
        self.isReverse = not self.isReverse
        self.unfilteredList.sort(key = lambda x: x[srtIndex], reverse = self.isReverse)
        self.ListControlRefresh()
    def OnItemClick(self, event):
        print self.lc.GetFocusedItem()
        for k in self.dataList:
            if k[0] == self.lc.GetItemText(self.lc.GetFocusedItem()):
                mstr = k[0] + '\n'
                ls = CalculateLv2Extend(k)
                for u in ls:
                    if type(u) is str:
                        mstr += u + '\n'
                    else:
                        mstr += '   ' + str(u) + '\n'
                self.sText.SetValue(mstr)
        #print self.lc.getitem
    def ListControlRefresh(self):
        print 'ref'
        self.lc.DeleteAllItems()
        p=self.pageScroll.GetThumbPosition()
        self.pageLabel.SetLabel("PAGE=%d"%p)
        
        rlist = self.unfilteredList
        # filter
        maxd = 0
        for k in range(min(100,len(rlist))): maxd = max(rlist[k][8], maxd)
        filteredList = []
        for k in rlist:
            if FILTER2:
                if k[8] != maxd: continue
            filteredList.append(k)
        for k in filteredList[p*36:36+p*36]:
            insertItem(self.lc, k)
        
        self.unfilteredList = rlist
        self.dataList = filteredList
        #wx.Event().GetEventObject()
    def OnScrollMove(self, event):
        print event.GetEventObject().GetThumbPosition()
        self.ListControlRefresh()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    CommonFrame().Show()
    app.MainLoop()  