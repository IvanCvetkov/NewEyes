import os
from SupportMethods import *
from string import digits
import cv2
from textblob import TextBlob
import numpy as np
import pytesseract
import sys


def modifyImage(imageUrl):
    image = cv2.imread(imageUrl)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 87, 13)
    showImg(adaptive_threshold)
    return image

def extractText(image, language):
    # --psm1
    config = '-l eng --oem 1 --psm 3'
    text = pytesseract.image_to_string(image, config=config, lang=language)
    print(text)
    return text

def removeMistakes(input):
    text = text.strip()
    text = text.replace("©", "")
    text = text.replace("|", "I")
    text = text.replace("1", "I")
    text = text.replace("[", "")
    text = text.replace("]", "")
    text = text.replace("{", "")
    text = text.replace("}", "")
    text = text.replace("\n", " ")
    text = ''.join(c if c not in map(str, range(0, 10)) else "" for c in text)
    textBlob = TextBlob(text)
    return textBlob

def textToSpeech(text):
    engine = pyttsx3.init()

    # rate = engine.getProperty('rate')
    engine.setProperty('rate', 140)
    engine.setProperty('volume', 0.8)

    if text != "":
        message = "In front of you is: "
        engine.say(message + str(text))
        engine.runAndWait()

    else:
        errorMessage = "There is nothing in front of you!"
        engine.say(errorMessage)
        engine.runAndWait()