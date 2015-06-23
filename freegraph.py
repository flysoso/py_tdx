#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx
import random
import math

FG_LINE = 1001
FG_RECT = 1002

class axisUtil():
	def __init__(self):
		pass
		self.screenPixTuple = (640, 480)
		self.screenPixOffset = (0,0)
	def setScreenPixRange(self, scrTuple = (640,480)):
		# something like (640, 480), pixel
		self.screenPixTuple = scrTuple
	def setRealArea(self, realTuple):
		'''
			# this is, the Area that is about to display
			# realTuple(xmin,ymin,xmax,ymax)
			# or (xmax,ymax) will keep min still in the class
		'''
		if len(realTuple) == 2:
			pass
		else:
			# len==4
			pass
		pass
	def setScreenPixOffset(self, pixOffsetTup):
		self.screenPixOffset = tupFlip(pixOffsetTup)
	def turnToScreen(self, tup):
		t1 = tupPlus(tup, self.screenPixOffset)
		return t1
	def turnToReal(self, tup):
		pass
	def FlipAndCenter(self, tp4):
		t1 = tupFlip(tp4)
		t2 = tupMul(self.screenPixTuple, (.5,.5))*2
		t1 = tupPlus(t1, t2)
		return t1

def tupFlip(tup1):
	ttup = []
	for k in range(len(tup1)):
		ttup.append(tup1[k] * ((k%2)*-2+1))
	return tuple(ttup)
	
def tupMul(tup1, tup2):
	ttup = []
	for k in range(len(tup1)):
		ttup.append(tup1[k]*tup2[k])
	return tuple(ttup)
		
def tupPlus(tup1, tup2):
	ttup = []
	for k in range(len(tup1)):
		ttup.append(tup1[k]+tup2[k])
	return tuple(ttup)
		
def disGraph(dc, theGraph, offsetTuple, axisUtilInst = 0):
	for k in theGraph:
		if k[0] == 'backColor':
			dc.SetBackground(wx.Brush( wx.ColorRGB(k[1]) ))
		elif k[0] == 'foreColor':
			pen = wx.Pen( wx.ColorRGB( k[1] ), 1, wx.SOLID)
			dc.SetPen(pen)
		elif k[0] == 'rect':
			pass
		elif k[0] == 'line' or k[0] == FG_LINE:
			tpu = k[1]
			ut = axisUtil()
			ut.setScreenPixOffset( offsetTuple )
			tpu = ut.turnToScreen(tpu[0:2])+ut.turnToScreen(tpu[2:4])
			dc.DrawLine(*ut.FlipAndCenter(tpu))

def getFirstOffset(theGraph, axisUtilInst):
	for k in theGraph:
		if k[0] == 'line' or k[0] == FG_LINE:
			tp = k[1][:2]
			tp= axisUtilInst.turnToScreen(tp)
			tp = tupMul(tp, (-1, 1))
			print 'first tp' ,tp
			return tp
			
class PaintWindow(wx.Window):
	def __init__(self, parent, id, theGraph):
		wx.Window.__init__(self, parent, id)
		self.SetBackgroundColour("Black")
	
		self.lines = []
		self.curGraph = []
		self.pos = (0, 0)
		
		self.theGraph = theGraph
		self.axisUtil = axisUtil()
		self.offsetTuple = (0,0)
		self.offsetTupleOld = (0,0)

		self.curPosAtDown = 0
		self.curPosAtUp = 0
		
		self.InitBuffer()
	
		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
		self.Bind(wx.EVT_MOTION, self.OnMotion)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_IDLE, self.OnIdle)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		
	def tryDraw(self):

		# this function is called by class 'self.usergraph'
		
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		dc.SetBackground(wx.Brush( wx.ColorRGB(0x000000) ))
		dc.Clear()
		pen = wx.Pen( wx.ColorRGB(0xffffff), 1, wx.SOLID)
		dc.SetPen(pen)

		disGraph(dc, self.theGraph, self.offsetTuple)
		
	def InitBuffer(self):
		size = self.GetClientSize()
		self.axisUtil.setScreenPixRange(size)
		
		self.buffer = wx.EmptyBitmap(size.width, size.height)
		dc = wx.BufferedDC(None, self.buffer)
		
		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
		dc.Clear()
		self.reInitBuffer = False
		
		self.offsetTuple  = getFirstOffset(self.theGraph, self.axisUtil)
		
	def OnLeftDown(self, event):
		
		self.curPosAtDown = event.GetPositionTuple()
		self.curPosAtUp = event.GetPositionTuple()
		self.offsetTupleOld = self.offsetTuple
		
	def OnLeftUp(self, event):

		self.curPosAtDown = 0
		print self.offsetTuple
		
	def OnMotion(self, event):
	
		if self.curPosAtDown != 0:
			self.offsetTuple = (self.curPosAtUp[0] - self.curPosAtDown[0] + self.offsetTupleOld[0],\
								self.curPosAtUp[1] - self.curPosAtDown[1] + self.offsetTupleOld[1])
		self.curPosAtUp = event.GetPositionTuple()
		
		self.tryDraw()
	
	def drawMotion(self, dc, event):

		newPos = event.GetPositionTuple()
		coords = self.pos + newPos
		
		#self.curLine.append(coords)
		if 1:
			dc.DrawLine(*coords)
			# format: dc.DrawLine( tuple1 ); tuple1 = (x1,y1,x2,y2)
		self.pos = newPos
		
	def OnSize(self, event):
		self.reInitBuffer = True
	
	def OnIdle(self, event):
		if self.reInitBuffer:
			self.InitBuffer()
			self.Refresh(False)
			self.reInitBuffer = False
			self.tryDraw()
	
	def OnPaint(self, event):
		dc = wx.BufferedPaintDC(self, self.buffer)
			
class PaintFrame(wx.Frame):
	def __init__(self, parent, theGraph):
		wx.Frame.__init__(self, parent, -1, "Panit Frame", size = (1200, 800))
		self.paint = PaintWindow(self, -1, theGraph)

def genBigGraph():
	bgra = []
	pstep = 252
	cir = 12
	rad = 200
	stx = 100
	sty = 0
	ax = stx
	ay = sty
	for k in range(0,pstep):
		arc = 2*3.1415926 * cir / pstep * k
		x = math.cos(arc) * rad / pstep * k + stx
		y = math.sin(arc) * rad / pstep * k + sty
		qclr = int(255*float(k) / pstep)
		bgra.append(['foreColor',-qclr * 0x000100 + 0x00ffff])
		bgra.append([FG_LINE, (x,y, ax, ay)])
		ax = x
		ay = y
	return bgra
		
def display(theGraph):
	app = wx.PySimpleApp()
	frame = PaintFrame(None, theGraph)
	frame.theGraph = theGraph
	frame.Show(True)
	app.MainLoop()
		
if __name__ == '__main__':
	
	#theGraph = [['backColor',0xffffff], ['foreColor',0x0000ff],['rect', (1,1,10,10)], ['line',(20,20,30,30)]]
	theGraph = genBigGraph()
	
	display(theGraph)
