import cv2
import numpy as np
from pyzbar.pyzbar import decode
from tldextract import extract
from gpiozero import Button
import multiprocessing
from google_speech import Speech
from pygame import mixer
import pyttsx3
import RPi.GPIO as GPIO  
from threading import Thread
import time
from textblob import TextBlob
from langdetect import detect
import os
import signal


Flag = 0
stop_btn = Button(4)
        

def domain_extractor(urlName):
    tsd, td, tsu = extract(urlName)  # prints abc, hostname, com
    url = td + '.' + tsu  # will print as hostname.com
    return url


def stop_qr():
    print("Stopping qr and barcode detection...")
    global Flag
    Flag = 1
    print(Flag)
    
    
def start_qr_barcode_recognition():
    global Flag
    global stop_btn
    
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    
    while True:
        
        stop_btn.when_pressed=stop_qr
        
        if Flag == 1:
            break
        
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
    
        data = domain_extractor(data)
        
        if len(data) < 5:
            data = ""
        
        if data:
            
            os.system("mpg321 qr_detected.mp3 &")
    
            time.sleep(2)
    
            print("data found: ", data)
            speech = Speech(data, 'en')
            speech.save("qr_code.mp3")
            os.system('mpg321 qr_code.mp3 &')
            time.sleep(1.7)
            continue
            
        cv2.imshow("code detector", img)
        
        code = cv2.waitKey(10)
        
            
    with open('process_pid.txt') as f:
        pid = f.readline()
    qr = int(pid)
    os.kill(qr, signal.SIGKILL)
    
    cap.release()
    cv2.destroyAllWindows()
        
        
if __name__ == "__main__":
    start_qr_barcode_recognition()
    