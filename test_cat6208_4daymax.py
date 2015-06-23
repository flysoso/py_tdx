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

class cat6208:
	def __init__(self, initTup, cfgTup = (1, 0.005), extTrader = 0):
		self.tup = initTup
		self.cfgTup = cfgTup
		self.tt = [initTup[1]]
	def run(self,tup):
		self.tt.append(tup[1])
		if len(self.tt) > 6: self.tt = self.tt[1:]
		newTup = tup[0], max(self.tt)
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
tg.append(['foreColor',0x0000ff])

tg.extend(AutoCreateLine(dline, lambda x:x))

tg.append(['foreColor',0xffffff])

k = dline[0]
initTup = (k.ftime * zoom, k.op * zoom)

animal = cat6208(initTup, (5,)) ; tg.extend(AutoCreateLine(dline, animal.run))

freegraph.display(tg)