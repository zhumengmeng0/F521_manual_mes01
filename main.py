from ui import *
from scanner_reader import *
import threading
from serial_read import *
if __name__ == '__main__':
    t1 = threading.Thread(target=scanner_read, args=())
    t1.setDaemon(True)
    t1.start()
    t2 = threading.Thread(target=serial_read, args=())
    t2.setDaemon(True)
    t2.start()
    t3 = threading.Thread(target=ui, args=())
    t3.start()
