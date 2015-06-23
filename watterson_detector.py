import time  
import thread
import urllib

def DetectThread(args):
    urll = args[0]
    callbackFunc = args[1]
    urlstream = urllib.urlopen(urll)
    udata = urlstream.read()
    callbackFunc(udata)
    thread.exit_thread()

def printData(dt):
    print dt

class ThreadManager():
    def __init__(self):
        self.pool = []
    def addDetect(self, args):
        thread.start_new_thread(DetectThread, (1,1))
   
if __name__=='__main__':  
    tManager = ThreadManager()
    tManager.addDetect(['http://www.baidu.com', printData])  
