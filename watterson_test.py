import watterson_lib
import tdx2

dline = tdx2.get_dayline_by_fid('sh000001', 5)

a = 1
for k in dline:
    a = a + 1
    k.cl=a

for k in dline:
    print k.ftime,k.cl    

pd = 3
prd = 2
d1 = watterson_lib.delta_ratio_reverse(dline, 1, 1)
d2 = watterson_lib.delta_ratio_reverse(dline, 1, 0)
d3 = watterson_lib.average(dline, 2, 0)
d4 = watterson_lib.variance(dline, 2, 0)
print d1, d2, d3, d4