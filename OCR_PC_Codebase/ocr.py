import os
import subprocess
import time
# from signal import pause
from subprocess import call
from SupportMethods import *
from InitialSetup import *
from string import digits
import cv2
from textblob import TextBlob
import numpy as np
import pygame
import pygame.camera
import pytesseract
import pyttsx3
import sys
# from gpiozero import Button
from pygame.locals import *


def start():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    language = "en"

    """IMAGE PREPROCESSING STAGE"""
    imageUrl = "C:\\Users\\ivan-\\Desktop\\Envision\\NewCameraTests\\secondImageTest.jpg"
    modifiedImg = modifyImage(imageUrl)
    text = extractText(modifiedImg, language)
    textBlob = removeMistakes(text)
    textToSpeech(str(textBlob))


if __name__ == "__main__":
    start()
    pygame.quit()
    sys.exit()
