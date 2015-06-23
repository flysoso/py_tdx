#coding: utf8

execfile('E:\\dev\\dev_eclipse\\libqda\\src\\_reg.py')

import struct
import os
import libqda_struct
import time

tdxpath = "C:\\new_tdx\\vipdoc"
america_path = "\\ds\\lday\\"
sh_path = "\\sh\\lday\\"
sz_path = "\\sz\\lday\\"

def change_path( pval, pname = 'tdxpath'):
	global tdxpath
	if pname == 'tdxpath':
		tdxpath = pval
		print 'tdx2.change.tdxpath =', pval
	# below is not used mostly
	if pname == 'america_path':
		america_path = pval
	if pname == 'sh_path':
		sh_path = pval
	if pname == 'sz_path':
		sz_path = pval

SetPath = change_path

def parse_time_reverse( ft):
	# 418x turn into 20101007
	s = ft
	s = (s + 10956) * 86400
	s -= 1000*60*60*6
	s = time.gmtime(s)
	s = time.strftime('%Y%m%d', s)
	s = int(s)
	return s
def parse_time( ft):
	# 20101007 turn into 418x
	s = str(ft)
	s = time.strptime(s,'%Y%m%d')
	s = time.mktime(s)
	s += 1000*60*60*6
	s = s / 86400 - 10956
	s = int(s)
	return s

	
def get_dayline_by_fid_america(str_fid = '74#AA-b', seekPoint = 0, readLength = 0):

	str_fid = str_fid.replace('.day','')

	str_tdx_dayline_format_america = "iffffiii"
	size_of_tdx_dayline = 32

	spath = tdxpath + america_path
	
	f = open(spath + str_fid + ".day", 'rb')
	
	#for i in range(0,9999):
	dayline = []
	
	#skip is ok
	f.seek(seekPoint)
	
	rlength = 0
	
	while 1:
		rd = f.read(32)
		
		if not rd: break
		#print i, len(rd)
		st = struct.unpack(str_tdx_dayline_format_america, rd)
		#print st
		
		q = libqda_struct.fdaydata()
		q.pars(	parse_time(st[0]),
				st[1],st[2],st[3],st[4],
				int(st[5]),
				int(st[6]),
				int(st[7])	)
				
		dayline.append(q)
		
		rlength+=1;
		if rlength == readLength: break

	return dayline
		
	f.close()

def get_dayline_by_fid(str_fid = 'sh000001', restrictSize = 0):

	str_fid = str_fid.replace('.day','')

	str_tdx_dayline_format = "iiiiifii"
	size_of_tdx_dayline = 32	#32 bytes per struct
	
	if str_fid[0:2] == 'sh':
		spath = tdxpath + sh_path
	else:
		spath = tdxpath + sz_path
	
	filename = spath + str_fid + ".day"
	f = open(filename, 'rb')

	if restrictSize != 0:
		fsize = os.path.getsize(filename)
		sr = fsize - 32 * restrictSize
		if sr < 0: sr = 0
		f.seek(sr)

	#for i in range(0,9999):
	dayline = []
	while 1:
		rd = f.read(32)
		if not rd: break
		#print i, len(rd)
		st = struct.unpack(str_tdx_dayline_format, rd)
		#print st
		
		q = libqda_struct.fdaydata()
		q.pars(	parse_time(st[0]),
				int(st[1]) / 100.,
				int(st[2]) / 100.,
				int(st[3]) / 100.,
				int(st[4]) / 100.,
				float(st[5]),
				int(st[6]),
				int(st[7])	)
		
		dayline.append(q)

	return dayline
		
	f.close()



def get_file_list(isAmerica = 0):
	
	print 'tdxpath is ', tdxpath
	
	listfile = []
	if isAmerica:
		fdir = tdxpath + america_path
		listfile = os.listdir(fdir)
		return listfile
	else:
		fdir = tdxpath + sh_path
		listfile = os.listdir(fdir)
		fdir = tdxpath + sz_path
		listfile += os.listdir(fdir)	
	
	return listfile
	

# 读一个明码的信息表，由通达信导出
def get_stock_data_list():
	
	f = open("sh_sz_data.txt", 'r')
	#while 1:
	for m in range(0,25):
		rd = f.readline()
		if not rd: break
		rd = rd.split('\t')
		for i in range(0, len(rd)):
			print rd[i],
		print
	
	
if __name__ == '__main__':
	if 1:
		print 'sh demo'
		dlist = get_dayline_by_fid('sh000001')
		print 'dlist_length:', len(dlist)
		dlist[0].display()
		dlist[-1].display()
		print
		print
	else:
		print 'america demo'
		dlist = get_dayline_by_fid_america()
		dlist[-1].display()
		
		s = get_file_list(isAmerica = 0)
		print s[0:5]
	
	raw_input()
	