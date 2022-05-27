import speech_recognition as sr
import realtime_yolo_obj_recog
from datetime import datetime
from datetime import date
from threading import *
from gtts import gTTS
from pygame import *
import wikipedia
import start_ocr
import start_obj_recog
from book_ocr import *
import _thread
import subprocess
from text_recognition import *
#import yolo_object_recog 
import pygame
import main
import time
import re
import os


def take_picture():
    def init_capture():
        subprocess.call(['sh', '/home/pi/guvc_force_capture.sh'])

    def stop_capture():
        time.sleep(4.5)
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


def read():
    take_picture()
    time.sleep(3)
    #start_ocr.call_google_api_ocr()
    print("chetene brat")
    text_recognition()


def detect_objects():
    
    path = '/home/pi/Desktop/output-1.jpg'
    main.take_picture()
    time.sleep(3)
    start_obj_recog.call_object_recognition(path)


def realtime_detect_objects():
    realtime_yolo_obj_recog.realtime_yolo_object_recognition()
   

def remove_parentheses(text):
    result = ''
    skip1c = 0
    skip2c = 0
    
    for i in text:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            result += i
    return result


def speech_recog():
    while True:
        r = sr.Recognizer()
        #r.energy_threshold = 300
        
        try:
            # card 2 | device 0 | microphone
            # card 1 | device 0 | headphones
            with sr.Microphone() as source:
                audio = r.listen(source,timeout=3)
                
            text = r.recognize_google(audio, language="bg-BG")
            text = text.lower()
            
            print("Text: " + text)
            
            if "hey glasses" in text or "glasses" in text or "ses" in text or "sses" in text or "ess" in text or "хей очила" in text or "здравей" in text or "хей" in text or "очила" in text:

                flag = 1
                
                # Play sound indicating reaction from the glasses
                
                # CHANGE MP3 FILE | THIS ONE WAS ADDED FOR TESTING PURPOSES ONLY!!!
                mixer.init()
                mixer.music.load('/home/pi/glasses_sound.wav')
                mixer.music.play()
                ###################################################################
                continue

            elif flag == 1:
                if "reed" in text or "read" in text or "breathe" in text or "tell me what is written" in text or "чети" in text or "прочети" in text or "изчети" in text or "четете" in text:
                    print("Reading Mode!")
                    read()

                elif "detect" in text or "objects" in text or "detect objects" in text or "tell me what is in front of me" in text or "tell me what's in front of me" in text or "обекти" in text:
                    print("Object Recognition Mode!")
                    realtime_detect_objects()

                elif "time" in text:
                    h_m_time = datetime.now().strftime('%I:%M')
                    curr = "The current time is " + str(h_m_time)
                    current_time = gTTS(text=curr, lang='en', slow=False)
                    current_time.save('/home/pi/voice_assistant_files/time.mp3')

                    mixer.init()
                    mixer.music.load('/home/pi/voice_assistant_files/time.mp3')
                    mixer.music.play()

                    print(curr)

                elif "date" in text:
                    today = date.today()
                    curr = "The current date is " + str(today);
                    current_date = gTTS(text=curr, lang='en', slow=False)
                    current_date.save('/home/pi/voice_assistant_files/date.mp3')

                    mixer.init()
                    mixer.music.load('/home/pi/voice_assistant_files/date.mp3')
                    mixer.music.play()

                    print(curr)

                elif "day" in text:
                    day = date.today().strftime("%A")
                    curr = "The current day is " + str(day)
                    current_day = gTTS(text=curr, lang='en', slow=False)
                    current_day.save('/home/pi/voice_assistant_files/day.mp3')

                    mixer.init()
                    mixer.music.load('/home/pi/voice_assistant_files/day.mp3')
                    mixer.music.play()

                    print(curr)

                elif "search for" in text or "search" in text or "for" in text:
                    text = text.replace('search ', '')
                    text = text.replace('for ', '')

                    curr = str(wikipedia.summary(text, sentences=1))

                    curr = remove_parentheses(curr)
                    text = "Searching for " + text + "..."

                    print(text)
                    print(curr)

                    # Says whrealtime_detect_objectsat the user is searching for
                    search_content = gTTS(text=text, lang='en', slow=False)
                    search_content.save('/home/pi/voice_assistant_files/search_content.mp3')

                    mixer.init()
                    mixer.music.load('/home/pi/voice_assistant_files/search_content.mp3')
                    mixer.music.play()

                    import time
                    time.sleep(1.5)

                    # Provides info about the searched topic
                    current_info = gTTS(text=curr, lang='en', slow=False)
                    current_info.save('/home/pi/voice_assistant_files/wikipedia.mp3')

                    mixer.init()
                    mixer.music.load('/home/pi/voice_assistant_files/wikipedia.mp3')
                    mixer.music.play()

                elif "who is" in text:
                    text = text.replace('who ', '')
                    text = text.replace('is ', '')
    
                    curr = str(wikipedia.summary(text, sentences=1))
                    curr = remove_parentheses(curr)
                    print(curr)
    
                    # Provides info about the searched topic
                    current_info = gTTS(text=curr, lang='en', slow=False)
                    current_info.save('/home/pi/voice_assistant_files/wikipedia.mp3')
    
                    mixer.init()
                    mixer.music.load('/home/pi/voice_assistant_files/wikipedia.mp3')
                    mixer.music.play()
                elif  "stop" in text:
                    flag = 0
                else:
                    os.system('mpg321 repeat.mp3 &')
                    continue
            flag = 0
                
        except:
            pass


if __name__ == "__main__":
    print("speech recognition...")
    speech_recog()