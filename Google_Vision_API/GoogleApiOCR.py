#!/usr/bin/env python3
from google.oauth2 import service_account
from google.cloud import vision
from pygame.locals import * 
import subprocess
from gpiozero import Button
from signal import pause
import pygame.camera
import ExecuteShellScript
import TestGoogleAPI
import pytesseract
from threading import Thread
import subprocess
import random
import numpy as np
"""import pyttsx3"""
from gtts import gTTS
import argparse
import time
import cv2
import sys
"""import playsound"""
import io
import os


def init_capture():
    subprocess.call(['sh', '/home/pi/guvc_force_capture.sh'])
    
    
def stop_capture():
    time.sleep(3)
    subprocess.call(['sh', '/home/pi/stop_capture.sh'])


def start_process():
    Thread(target = init_capture).start()
    Thread(target = stop_capture).start()
    
    
def gtts_speak(text):

    if text != "":
        tts = gTTS(text)
        tts.save('page.mp3')
        os.system('mpg321 page.mp3 &')

    else:
        errorMessages = ["There is nothing in front of you!",
                         "Sorry, but there is nothing to read!",
                         "There is nothing to read, try taking a picture again!"]

        chosen_message = random.choice(errorMessages)
        print(chosen_message)

        tts = gTTS(chosen_message)
        tts.save('error.mp3')
        os.system('mpg321 error.mp3 &')

def start():
    imageUrl = "/home/pi/Desktop/output-1.jpg"
    client = "/home/pi/client_id.json"
    print('start method initiated')
        
    #start_process()

    TestGoogleAPI.call_google_api()
     
def start_pressed():
    try:
        if os.path.exists("/home/pi/Desktop/output-1.jpg"):
            os.remove("/home/pi/Desktop/output-1.jpg")
        
        print("Start button pressed!")
        start_process()
        start()
    except Exception:
        pass

if __name__ == '__main__':
    
    #ExecuteShellScript.start_process()
    #sys.exit()
    counter = 0
    if counter == 0:
        os.system('mpg321 program.mp3 &')
    counter+=1

    try:
        startButton = Button(2)
        startButton.when_pressed = start_pressed

        pause()

    except Exception as e:
        print(e)

    finally:
        sys.exit()