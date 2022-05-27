#!/usr/bin/env python3
#from google.oauth2 import service_account
#from google.cloud import vision
from threading import Thread
from gpiozero import Button
import signal
#from pygame.locals import *
#from pygame import mixer
#from signal import pause
#import multiprocessing
#from gtts import gTTS
#import pygame.camera
import webbrowser
import pyautogui
#from speech_recog import *
import start_obj_recog
#import process_checker
import start_ocr
#import numpy as np
import subprocess
#import duo_google
from receipt_scanner import *
from predominant_clr import *
from book_ocr import *
#from crnn_ocr import *
from text_recognition import *
import argparse
#import _thread
import random
import time
import cv2
import sys
import io
import os


# Global variables
mode = 0


def synchronize_time():
    subprocess.call(['sh', "/home/pi/run_sync.sh"])
        

    ###################################
    # Executables and scripts
def call_google_api_ocr():
    start_ocr.call_google_api_ocr()
    # subprocess.call(["python3", "/home/pi/start_ocr.py"])
def call_obj_recog(path):
    start_obj_recog.call_object_recognition(path)
    # subprocess.call(["python3", "/home/pi/start_obj_recog.py"])
def realtime_detect_objects():
    realtime_yolo_obj_recog.realtime_yolo_object_recognition()
def voice_assistant():
    speech_process = subprocess.Popen(['python3', '/home/pi/speech_recog.py'])
    pid = speech_process.pid;
    
    with open('/home/pi/speech_process_pid.txt', 'w') as f:
        f.write(str(pid))
        
    print(pid)
    
    speech_process.wait()
    ###################################


def take_picture():
    def init_capture():
        subprocess.call(['sh', '/home/pi/guvc_force_capture.sh'])

    def stop_capture():
        time.sleep(3)
        subprocess.call(['sh', '/home/pi/stop_capture.sh'])

    def start_process():
        Thread(target=init_capture).start()
        Thread(target=stop_capture).start()

    def start_pressed():
        try:
            if os.path.exists("/home/pi/Desktop/output-1.jpg"):
                os.remove("/home/pi/Desktop/output-1.jpg")

            os.system("mpg321 first_beep.mp3 &")
            start_process()
            time.sleep(5.0)
            os.system('mpg321 second_beep.mp3 &')

        except Exception:
            pass
        finally:
            print("Picture taken successfully!")

    start_pressed()


def increase_mode_value():
    global mode
    
    
    mode += 1
    os.system("pkill mpg321")
    
    if mode == 1:
        os.system('mpg321 /home/pi/book_ocr_read.mp3 &')
        print("book reading mode")
        
    elif mode == 2:
        os.system('mpg321 /home/pi/street_ocr_read.mp3 &')
        print("street reading mode")
        
    elif mode == 3:
        os.system("mpg321 /home/pi/obj_recog.mp3 &")
        print("object recognition mode")
        
    elif mode == 4:
        os.system("mpg321 /home/pi/continuous_obj_recog.mp3 &")
        print("continuous object recognition mode")
        
    elif mode == 5:
        os.system('mpg321 /home/pi/duo.mp3 &')
        print("Remote duo assistant")
        
    elif mode == 6:
        # Terminate all chromium processes in order to avoid possible bottleneck
        #os.system("pkill chromium")
        
        os.system('mpg321 /home/pi/qr_barcode_recog.mp3 &')
        print("QR and barcode recognition")
        
    elif mode == 7:
        os.system('mpg321 /home/pi/rec_scanner.mp3 &')
        print("Receipt scanner")
        
    elif mode == 8:
        os.system('mpg321 /home/pi/money_detection.mp3 &')
        print("Detect money")
        
    elif mode == 9:
        os.system('mpg321 /home/pi/predominant_color.mp3 &')
        print("Predominant color detection")
    elif mode > 9:
        mode = 1
        os.system("mpg321 /home/pi/book_ocr_read.mp3 &")
        print("loop and back to the first mode")


def execute_action():
    #with open('speech_process_pid.txt') as f:
    #    pid = f.readline()
    #speech_pid = int(pid)RaspberryDummy0
    
    #os.kill(speech_pid, signal.SIGKILL)
    
    global mode
    os.system("pkill mpg321")
    
    if mode == 1:
        take_picture()
        time.sleep(3)
        
        # Call book ocr
        text_recognition()

        
        # call_google_api_ocr()
    
    elif mode == 2:
        take_picture()
        time.sleep(3)
        
        # Call street ocr
        street_ocr()
    
    elif mode == 3:
        take_picture()
        time.sleep(3)
        
        # Call object recognition
        path = '/home/pi/Desktop/output-1.jpg'
        call_obj_recog(path)

    elif mode == 4:
        os.system('mpg321 ready_signal.mp3 &')
        realtime = subprocess.Popen(['python3', '/home/pi/realtime_yolo_obj_recog.py'])
        pid = realtime.pid;
        
        with open('/home/pi/process_pid.txt', 'w') as f:
            f.write(str(pid))
            
        print(pid)
        
        realtime.wait()
        
    elif mode == 5:
        duo_process = subprocess.Popen(['python3', '/home/pi/duo_google.py'])
        pid = duo_process.pid;
        
        with open('/home/pi/process_pid.txt', 'w') as f:
            f.write(str(pid))
            
        print(pid)
        
        duo_process.wait()
        
        # Call duo assistant
        #duo_google.make_call()
        #os.system('python3 duo_google.py')
    elif mode == 6:
        # Call qr and barcode recognition
        os.system('mpg321 ready_signal.mp3 &')
        qr = subprocess.Popen(['python3', '/home/pi/qr_barcode.py'])
        pid = qr.pid
        
        with open('/home/pi/process_pid.txt', 'w') as f:
            f.write(str(pid))
            
        print(pid)
        
        qr.wait()
    elif mode == 7:
        
        take_picture()
        time.sleep(3)
        
        # Call receipt scanner
        scan_receipt()
    elif mode == 8:
        # Call money recognition 
        
        print("Money detection mode")
    elif mode == 9:
        
        take_picture()
        time.sleep(3)
        
        # Get predominant color 
        get_colour()
        
    #Thread(target=voice_assistant).start()
    
        
def duo_init():
    
    webbrowser.open('www.google.com')
    time.sleep(5)
    pyautogui.keyDown("ctrl")
    pyautogui.keyDown("shift")
    pyautogui.press("n")

    pyautogui.keyUp("ctrl")
    pyautogui.keyUp("shift")
    
    time.sleep(5)
    pyautogui.typewrite('https://duo.google.com/?web&utm_source=marketing_page_button_main')
    pyautogui.press("enter")
    time.sleep(20)  

    pyautogui.typewrite('rpidummy0@gmail.com')
    pyautogui.press("enter")
    time.sleep(6)
    
    pyautogui.typewrite('RaspberryDummy0')
    pyautogui.press("enter")

        
if __name__ == '__main__':
    # Time synchronization to ntp servers
    # Necessary for using the google vision api(s)

    #synchronize_time()
    #voice_assistant()

    # Indicate that the device is ready
    # Initialize the main case buttons

    os.system('mpg321 startup_signal.mp3 &')
    
    
    actionBtn = Button(4)
    nextBtn = Button(2)
    ###################################

    
    # Start the smart voice assistant worker thread
    
    
    Thread(target=duo_init).start()
    #Thread(target=voice_assistant).start()
    
    ###################################
    while True:

    # switch the mode to a different action
        actionBtn.when_pressed = execute_action
        nextBtn.when_pressed = increase_mode_value

    ###################################
