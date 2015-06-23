import tdx2

import random
import time

dlist = []

class trader:
	def __init__(self):
		# [cur, stoc]
		self.state_list = [10000, 0]
		
	def buy(self, dd, pric):
		
		cur, stoc = self.state_list
		
		ct = cur*dd / pric
		stoc += ct
		cur = cur * (1-dd)
		
		self.state_list = [cur, stoc]

	def sell(self, dd, pric):
	
		cur, stoc = self.state_list
		
		ct = stoc*dd * pric
		cur += ct
		stoc = stoc * (1-dd)
		
		self.state_list = [cur, stoc]

def climb(x = 1, y = 5, z = -3, buy_co = 0.5, sell_co = 0.5):

	decline_degree = x
	exception_valve1 = y
	exception_valve2 = -z

	tr1 = trader()
	exc = 0

	r_op = dlist[0].op
	rr_op = dlist[0].op
	
	for k in dlist:
	
		delta_exc = -(r_op / rr_op - 1) * 100
		exc += delta_exc
		exc = exc / decline_degree
		
		if exc > exception_valve1:
			#exc = exception_valve1
			tr1.buy(buy_co, k.op)
		if exc < exception_valve2:
			tr1.sell(sell_co, k.op)
		
		rr_op = r_op
		r_op = k.op

	tr1.sell(1, k.op)

	return tr1.state_list[0]

if __name__ == '__main__':
		
	dlist = tdx2.get_dayline_by_fid('sh000001')

	print 'days:', len(dlist)

	print
	print
	
	rlist = []
	
	'''
	for x in range(6,7):
		for y in range(-1, 0):
			for z in range(86,100, 1):
				fr = climb(1 + float(z)/10000,x,y)
				rlist.append([x,y,z,fr])
	'''
	
	toplist = []
	for k in range(0,4):
		toplist.append([0,0,0,0])
	currmax = 0
	
	while (1):
		
		random.seed(time.time())
		rlist = []
		
		for k in range(0,100):
			x = random.randint(3, 13)
			y = random.randint(-10,2)
			z = 1.0 * random.randint(0,120)
			br = random.randint(0,10) / 10.0
			sr = random.randint(0,10) / 10.0
			result = climb(1 + float(z)/10000,x,y, br, sr)
			rlist.append([result,z,x,y, br, sr])
			
		rlist.sort(key = lambda x: x[0])
		
		t = rlist[-1]
		for k in range(3,-1,-1):
			if t[0] > toplist[k][0]:
				toplist[k] = t
				print '__refresh_toplist'
				for i in toplist:
					print i
			if t == toplist[k]: break

		
		if 0:
			for k in rlist:
				print k		
			print 'input q to quit'
			q = raw_input()
			if q == 'q': break
		
	raw_input()