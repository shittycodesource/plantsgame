import threading

def set_timeout(func, sec):     
    timer = None
    
    def func_wrapper():
        func()  
        timer.cancel()

    timer = threading.Timer(sec, func_wrapper)
    timer.start()

# never actually used this