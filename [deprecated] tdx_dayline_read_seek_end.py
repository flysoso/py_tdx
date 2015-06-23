import struct
import os

str_tdx_dayline_format = "iiiiifii"
size_of_tdx_dayline = 32

f = open("C:\\new_tdx\\vipdoc\\sh\\lday\\sh000001.day", 'rb')

f.seek(-32*100, os.SEEK_END)
print f.tell()

for i in range(0,100):
	rd = f.read(32)
	if not rd: break
	print i, len(rd)
	st = struct.unpack(str_tdx_dayline_format, rd)
	print st
	
f.close()
	
raw_input()