import pytesseract
import numpy as np
import argparse
import os
import cv2
from google_speech import Speech
from utils import forward_passer, box_extractor
from text_detection import resize_image
from imutils.object_detection import non_max_suppression
from image_processing import *


url = '/home/pi/Desktop/output-1.jpg'

osd = ''
try:
    osd = pytesseract.image_to_osd(url, config='--psm 0 -c min_characters_to_try=4')
except:
    pass

print(osd)

def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', type=str,
                    help='path to image', default=url)
    ap.add_argument('-east', '--east', type=str,
                    help='path to EAST text detection model', default='/home/pi/frozen_east_text_detection.pb')
    ap.add_argument('-c', '--min_confidence', type=float, default=0.5,
                    help='minimum confidence to process a region')
    ap.add_argument('-w', '--width', type=int, default=320,
                    help='resized image width (multiple of 32)')
    ap.add_argument('-e', '--height', type=int, default=320,
                    help='resized image height (multiple of 32)')
    ap.add_argument('-p', '--padding', type=float, default=0.0,
                    help='padding on each ROI border')
    arguments = vars(ap.parse_args())

    return arguments


def gtts_speak(text, language):
    if 'bul' in language:
        language = 'bg'
    elif 'eng' in language:
        language = 'en'
        
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



def main(image, width, height, detector, min_confidence, padding):

    # reading in image
    image = cv2.imread(image)
    orig_image = image.copy()
    orig_h, orig_w = orig_image.shape[:2]

    # resizing image
    image, ratio_w, ratio_h = resize_image(image, width, height)

    # layers used for ROI recognition
    layer_names = ['feature_fusion/Conv_7/Sigmoid',
                   'feature_fusion/concat_3']

    # pre-loading the frozen graph
    print("[INFO] loading the detector...")
    net = cv2.dnn.readNet(detector)

    # getting results from the model
    scores, geometry = forward_passer(net, image, layers=layer_names)

    # decoding results from the model
    rectangles, confidences = box_extractor(scores, geometry, min_confidence)

    # applying non-max suppression to get boxes depicting text regions
    boxes = non_max_suppression(np.array(rectangles), probs=confidences)

    results = []
    res = ''
    # text recognition main loop
    for (start_x, start_y, end_x, end_y) in boxes:
        start_x = int(start_x * ratio_w)
        start_y = int(start_y * ratio_h)
        end_x = int(end_x * ratio_w)
        end_y = int(end_y * ratio_h)

        dx = int((end_x - start_x) * padding)
        dy = int((end_y - start_y) * padding)

        start_x = max(0, start_x - dx)
        start_y = max(0, start_y - dy)
        end_x = min(orig_w, end_x + (dx*2))
        end_y = min(orig_h, end_y + (dy*2))

        # ROI to be recognized
        roi = orig_image[start_y:end_y, start_x:end_x]

        # recognizing text
        language = ''
        if "Script: Cyrillic" in osd:
            language = 'bul'
        elif "Script: Latin" in osd:
            language = 'eng'
        else:
            language = 'eng'
            
        config = '--oem 1 --psm 7'
        text = pytesseract.image_to_string(roi, config=config, lang=language)
        res = res + text + " "
        # collating results
        results.append(((start_x, start_y, end_x, end_y), text))
        
    res.rstrip()
    print(res)
    gtts_speak(res, language)
    # sorting results top to bottom
    results.sort(key=lambda r: r[0][1])

    # printing OCR results & drawing them on the image
    for (start_x, start_y, end_x, end_y), text in results:

        print(f'{text}\n')

        # stripping out ASCII characters
        text = ''.join([c if ord(c) < 128 else "" for c in text]).strip()
        output = orig_image.copy()
        cv2.rectangle(output, (start_x, start_y), (end_x, end_y), (0, 0, 255), 2)
        cv2.putText(output, text, (start_x, start_y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        #cv2.imshow('Detection', output)
        #cv2.waitKey(0)


def street_ocr():

    args = get_arguments()

    main(image=args['image'], width=args['width'], height=args['height'],
         detector=args['east'], min_confidence=args['min_confidence'],
         padding=args['padding'])
    

#if __name__ == '__main__':
#   street_ocr()