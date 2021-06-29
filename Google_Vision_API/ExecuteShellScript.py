import subprocess
import os
import sys
import time
from threading import Thread


def init_capture():
    subprocess.call(['sh', '/home/pi/guvc_force_capture.sh'])
    
    
def stop_capture():
    #time.sleep(3)
    subprocess.call(['sh', '/home/pi/stop_capture.sh'])


def start_process():
    Thread(target = init_capture).start()
    Thread(target = stop_capture).start()
    

if __name__ == '__main__':
    start_process()
    #sys.exit()