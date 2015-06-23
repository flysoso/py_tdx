#coding: utf8

import tdx2
import freegraph
import math

def list_average(dlist):
	if len(dlist) == 0: return 0
	ssum=0.
	for k in dlist:
		ssum+=k[1]
	return ssum/len(dlist)
def list_variance(dlist):
	if len(dlist) == 0: return 1
	ssum = 0.
	for k in dlist:
		ssum += k[1]*k[1]
	return math.sqrt(ssum / len(dlist))

def list_vda(dlist):	# variance div average
	if len(dlist) == 0: return 0
	return list_variance(dlist) / list_average(dlist)

class cow6208:
	# 计算N日方差比均值，N在cfgTup里
	def __init__(self, initTup, cfgTup = (30), extTrader = 0):
		self.tup = initTup
		self.cfgTup = cfgTup
		self.memList = []
		self.extTrader = extTrader
	def run(self, tup):
		N = self.cfgTup[0]
		self.memList.append(tup)
		if self.memList.__len__() < N:
			return (tup[0], 0 + self.tup[1])
		else:
			dlist = self.memList[-N:]
			k = (list_vda(dlist)-1)*100000
			print k
			return (tup[0], k + self.tup[1])
			
			
class mice6208:
	def __init__(self, initTup, cfgTup = (1, 0.005), extTrader = 0):
		self.tup = initTup
		self.cfgTup = cfgTup
		self.extTrader = extTrader
	def run(self,tup):
		deltaFallT, deltaRiseT = self.cfgTup
		
		newP = self.tup[1]
		tarP = tup[1]
		ftime = tup[0]
		
		if newP < tarP: newP += (tarP - newP) * deltaRiseT
		elif newP > tarP: newP += (tarP - newP) * deltaFallT
		
		newTup = (ftime, newP)
		self.tup = newTup
		
		if self.extTrader != 0:
			self.extTrader.run(tup)
		
		return newTup
		
	def getExtTrader(self):
		return self.extTrader



#theGraph = [['backColor',0xffffff], ['foreColor',0x0000ff],['rect', (1,1,10,10)], ['line',(20,20,30,30)]]

def AutoCreateLine(dline, func):
	k = dline[0]
	tup = (k.ftime * zoom, k.op * zoom)
	#tup = (0,0)
	tg = []
	for k in dline:
		tup1 = (k.ftime * zoom, k.op * zoom)
		tup1 = func(tup1)
		tg.append(['line', tup+tup1])
		tup = tup1	
	return tg

dline = tdx2.get_dayline_by_fid();
zoom = 1

tg = []

tg.extend(AutoCreateLine(dline, lambda x:x))

tg.append(['foreColor',0x0000ff])

k = dline[0]
initTup = (k.ftime * zoom, k.op * zoom)

animal = mice6208(initTup, (0.8, 0.01))
tg.extend(AutoCreateLine(dline, animal.run))

tg.append(['foreColor',0x00ffff])

animal = mice6208(initTup, (0.01, 0.8))
tg.extend(AutoCreateLine(dline, animal.run))

tg.append(['foreColor',0x800000])

#animal = cow6208(initTup, (30,)); tg.extend(AutoCreateLine(dline, animal.run))

animal = cow6208(initTup, (5,)) ; tg.extend(AutoCreateLine(dline, animal.run))

freegraph.display(tg)