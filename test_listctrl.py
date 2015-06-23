
import wx
import random

wordlist = []

def strr(k):
    if type(k) is str:
        return k
    else:
        return str(k)

def insertItem(lc, arr):
    index = lc.InsertStringItem(555, strr(arr[0]))
    for k in range(1, len(arr)):
        lc.SetStringItem(index, k, strr(arr[k]))

class CommonFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'commframe', 
                size=(800, 800),
                style = wx.MINIMIZE_BOX  |wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        lc = wx.ListCtrl(panel, -1, size=(720,720), pos=(30,20),style=wx.LC_REPORT)
        lc.InsertColumn(9999, "ID");
        for i in range(1,12):
            lc.InsertColumn(9999, "VAR"+str(i));
        for k in range(0,101):
            insertItem(lc, ("haha", k, random.randint(100,9999), 123))
        self.Center()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    CommonFrame().Show()
    app.MainLoop()  