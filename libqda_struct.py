class fdata:
	def pars(self, ffid, ffname, ddaycount):
		self.fid = ffid;
		self.fname = ffname;
		self.daycount = ddaycount;
	def print_str(self):
		return "this data"
		#return "  ID: " + self.fid + "\n" \
		#		+ "  NAME:" + self.fname + "\n" \
		#		+ "  DAYC:" + self.ddaycount
	def __init__(self):
		self.fid = '';
		self.fname = '';
		self.daycount = 0;
		self.fcursor = 0;

class fdaydata:
	def pars(self, fftime, oop, hhig, llow, ccl, vvol, aamount, ddealcount):
		self.ftime = fftime;
		self.op = oop;
		self.hig = hhig;
		self.low = llow;
		self.cl = ccl;
		self.vol = vvol;
		self.amount = aamount;
		self.dealcount = ddealcount;
	def __init__(self):
		self.ftime = 0;
		self.op = 0.0;
		self.hig = 0.0;
		self.low = 0.0;
		self.cl = 0.0;
		self.vol = 0.0;
		self.amount = 0.0;
		self.dealcount = 0.0;
	def time2000(self):
		return self.ftime / 86400 - 10956
	def display(self):
		print "fdata display,"
		print '  time_   ', self.ftime
		print '  op_'    , self.op
		print '  last-cl_', self.cl
		print '  highest_', self.hig
		print '  lowest_ ', self.low
		print '  dvol_   ', self.vol
		print '  damount_', self.amount
		print '  dcount_ ', self.dealcount