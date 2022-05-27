from google_speech import Speech
from image_processing import *
from gpiozero import Button
from gtts import gTTS
import random
import os


def text_recognition():
    
    os.system("pkill mpg321")

    language = ''
    os.environ['OMP_THREAD_LIMIT'] = '1'
    IMAGE_PATH = "/home/pi/Desktop/output-1.jpg"
    os.system("mpg321 /home/pi/please_wait.mp3 &")

    
    print("pre-processing...")
    # Deskew the given image after the
    # Preprocessing stage is done
    modified_img = process_image(IMAGE_PATH)
    deskew('/home/pi/processed_image.jpg')
    
    print("pre-processing finished...")
    # Check the processed image for
    # Any text that is upside down
    
    osd = ''
    try:
        osd = pytesseract.image_to_osd('/home/pi/deskewed_image.jpg', config='--psm 0 -c min_characters_to_try=30')
        print(osd)
    except:
        pass
        
        
    index = osd.find("Script confidence:")
    script_confidence = float(index)
    script_confidence = int(script_confidence)
    
    script_confidence = float(osd[script_confidence+19:script_confidence+23])

        
    if "Script: Cyrillic" in osd and script_confidence > 0.50:
        language = 'bul'
    elif "Script: Latin" in osd and script_confidence > 0.50:
        language = 'eng'
    else:
        language = 'eng'
    # Dewarp code goes here...
    
    text = ''
    
    index = osd.find("Orientation confidence:")
    orientation_confidence = float(index)
    orientation_confidence = int(orientation_confidence)
    #print(orientation_confidence)
    #print(osd[orientation_confidence+24:orientation_confidence+28])
    orientation_confidence = float(osd[orientation_confidence+24:orientation_confidence+28])
    
    # Flip the image case
    if "Orientation in degrees: 180" in osd and orientation_confidence > 0.50:
        
        im = Image.open('/home/pi/deskewed_image.jpg')
        angle = 90
        out = im.rotate(angle)
        out.save("/home/pi/flipped_image.jpg")
        text = text_extraction('/home/pi/flipped_image.jpg', language)
    
    elif "Orientation in degrees: 90" in osd and orientation_confidence > 0.50:
        im = Image.open('/home/pi/deskewed_image.jpg')
        angle = 90
        out = im.rotate(angle)
        out.save("/home/pi/flipped_image.jpg")
        text = text_extraction('/home/pi/flipped_image.jpg', language)

    elif "Orientation in degrees: 270" in osd and orientation_confidence > 0.50:
        im = Image.open('/home/pi/deskewed_image.jpg')
        angle = 90
        out = im.rotate(angle)
        out.save("/home/pi/flipped_image.jpg")
        text = text_extraction('/home/pi/flipped_image.jpg', language)
        
    else:
        text = text_extraction('/home/pi/deskewed_image.jpg', language)
    
    text = mistake_removal(text)
    
    if 'bul' in language:
        language = 'bg'
    elif 'eng' in language:
        language = 'en'
        
    gtts_speak(str(text), language)
    

def kill_mpg():
    os.system("pkill mpg321")
    
    
def gtts_speak(text, language):
    
    if text != "":
        speech = Speech(text, language)
        speech.save("page.mp3")
        os.system('mpg321 page.mp3 &')

    else:
        errorMessages = ["ocr_error_1.mp3",
                         "ocr_error_2.mp3",
                         "ocr_error_3.mp3"]

        chosen_message = random.choice(errorMessages)
        print(chosen_message)

        os.system('mpg321 ' + '/home/pi/error_messages/' + chosen_message + ' &')

#text_recognition()