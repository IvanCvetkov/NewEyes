from google.oauth2 import service_account
from google.cloud import vision
#from pygame.locals import * 
from subprocess import call
from gpiozero import Button
import sys
from translator import translate
from google_speech import Speech
from signal import pause
#import pygame.camera
from langdetect import detect
import multiprocessing
#from pygame import *
from threading import Thread
#from main import *
import subprocess
import random
import numpy as np
#import pyttsx3
from gtts import gTTS
#import argparse
import time
import cv2
import io
import os


def gtts_speak(text):
    
    #text = text.replace("- ", "-")
    #blob = TextBlob(text)
    
    if text != "":
        #translator = Translator()
        #translated = translator.translate(text, src='en', dest='bg')
        language = 'en'
        tts = gTTS(text, lang=language)
        tts.save('/home/pi/yolo_objects.mp3')
        os.system("mpg321 /home/pi/yolo_objects.mp3 &")

    else:
        errorMessages = ["obj_error_1.mp3",
                         "obj_error_2.mp3",
                         "obj_error_3.mp3"]

        chosen_message = random.choice(errorMessages)
        print(chosen_message)

        os.system('mpg321 ' + '/home/pi/error_messages/' + chosen_message + ' &')


def call_object_recognition(path):
    # informs the customer to anticipate a delay
    os.system('mpg321 /home/pi/please_wait.mp3 &')
    # load the COCO class labels our YOLO model was trained on
    LABELS = open("/home/pi/yolo/darknet/data/coco.names").read().strip().split("\n")

    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet("/home/pi/yolo/darknet/cfg/yolov4-tiny.cfg", "/home/pi/yolo/darknet/weights/yolov4-tiny.weights")


    #yolo-coco/yolov3.cfg
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
    
    image = cv2.imread(path)
    resized = cv2.resize(image, (416, 416))
    (H, W) = resized.shape[:2]
    blob = cv2.dnn.blobFromImage(resized, 1 / 255.0, (416, 416),
        swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []
    centers = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > 0.5:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
                centers.append((centerX, centerY))

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

    texts = []

    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # find positions
            centerX, centerY = centers[i][0], centers[i][1]
            
            if centerX <= W/3:
                W_pos = "left "
            elif centerX <= (W/3 * 2):
                W_pos = "center "
            else:
                W_pos = "right "
            
            if centerY <= H/3:
                H_pos = "top "
            elif centerY <= (H/3 * 2):
                H_pos = "mid "
            else:
                H_pos = "bottom "

            texts.append(H_pos + W_pos + LABELS[classIDs[i]])
    if len(idxs) == 0:
        gtts_speak("")
    print(texts)
    
    if texts:
        description = ', '.join(texts)
        
        # translate to bulgarian
        #translator = Translator()
        #translated = translator.translate(description, src='en', dest='bg')
    
        # Translate contents
        translation = translate(description)
   
        
        # create sound file in bulgarian
        language = "bg"
        speech = Speech(translation, language)
        speech.save("yolo_objects.mp3")
        os.system('mpg321 yolo_objects.mp3 &')
        print(translation)
        

#call_object_recognition('/home/pi/Desktop/output-1.jpg')
