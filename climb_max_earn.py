import tdx2
from climb_func import trader

dlist = tdx2.get_dayline_by_fid('sh000001')

def climb_max_earn():

	tr1 = trader()

	r_op = dlist[0].op

	for k in dlist:
	
		if(k.op > r_op):
			tr1.buy(1, r_op)
			tr1.sell(1,k.op)
		r_op = k.op

	return tr1.state_list[0]

print
print
print climb_max_earn()
	
raw_input()