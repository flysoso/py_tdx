import threading  
import time
import urllib

class timer(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, num, interval, callback = lambda x:1):  
        threading.Thread.__init__(self)  
        self.thread_num = num  
        self.interval = interval  
        self.callback = callback
        self.thread_stop = False  

    def run(self): #Overwrite run() method, put what you want the thread do here  
        p = urllib.urlopen('http://hq.sinajs.cn/list=sh601006').read()
        self.callback(p)
        print p

'''
        self.stop()
    def stop(self):  
        self.thread_stop = True
        self.callback()'''
        
def test_urllib():
    p = urllib.urlopen('http://hq.sinajs.cn/list=sh601006').read()
    print p
   
def test():  
    thread1 = timer(1, 1)  
    thread2 = timer(2, 2)  
    thread1.start()  
    thread2.start()  
    time.sleep(10)  
    thread1.stop()  
    thread2.stop()  
    return  
   
if __name__ == '__main__':  
    #test()
    test_urllib()