from pygame.locals import *
from subprocess import call
from gpiozero import Button
from signal import pause
import pygame.camera
import pytesseract
import subprocess
import pygame, sys
import numpy as np
import pyttsx3
import time
import cv2
import os
#import wordninja


def start():
    
    # Initialise image size
    width = 600
    height = 600

    # Initialise pygame
    pygame.init()
    pygame.camera.init()
    cam = pygame.camera.Camera("/dev/video0", (width, height))
    cam.start()
    time.sleep(1)
    
    # Setup window
    windowSurfaceObj = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Camera')

    # Take a picture
    capture = cam.get_image()

    # Display the picture
    windowSurfaceObj.blit(capture, (0, 0))
    pygame.display.update()

    # Save picture
    pygame.image.save(windowSurfaceObj, 'picture.jpg')
    cam.stop()

    #image = np.asarray(imageUrl)
    image = cv2.imread('picture.jpg')
    #image = cv2.resize(image, None, fx=0.6, fy=0.9)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)


    #config = "--psm 1", r'--oem 3 --psm 6'
    language = "en"
    config = '-l eng --oem 1 --psm 3'
    text = pytesseract.image_to_string(adaptive_threshold, config=config, lang=language)
    
    
    # Delete the useless characters | Abbreviations
    text = text.strip()
    text = text.replace("\n", " ")
    print(text)

    # Write the recognized text to the text_result.txt
    #result = str(text)
    #with open("text_result.txt", mode ='w') as file:
    #    file.write(result)
    #    print("Recognized text Saved!")

    # Convert the result text to an mp3 file

    engine = pyttsx3.init()
    
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 140)
    engine.setProperty('volume', 0.8)
    

    if text != "":
        message = "In front of you is: "
        engine.say(message + text)
        engine.runAndWait()

    else:
        errorMessage = "There is nothing in front of you!"
        engine.say(errorMessage)
        engine.runAndWait()
        
    # Play the mp3 file
    #espeak.synth("output.mp3")
    #while espeak.is_playing:
        #pass

# GPIO Functionalities
def button_pressed():
    print("Button was pressed")
    start()


def manual_started():
    print("Manual started playing...")
    
    #Play manual mp3 file
    #...


def reserved_pressed():
    print("Reserved for other purposes button pressed...")
    
    #do whatever...


#def button_held():
#    print("Button was held")
#    call("sudo shutdown -h now", shell=True)


if __name__ == "__main__":
    try:
        startButton = Button(2)
        #reservedButton = Button(3)
        manualButton = Button(4)
        manualButton.when_pressed = manual_started
        #reservedButton.when_pressed = reserved_pressed
        startButton.when_pressed = button_pressed
        #start()
        pause()
        
    except Exception as e:
        print(e)
        
    finally:
        pygame.quit()
        sys.exit()



