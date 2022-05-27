import os
from string import digits
import cv2
# from wand.image import Image
from textblob import TextBlob
import numpy as np
import image_processing
from PIL import Image
from imutils.perspective import four_point_transform
import imutils
from autocorrect import Speller
from skimage.segmentation import clear_border
import pytesseract
import sys

import numpy as np
from skimage import io
from skimage.color import rgb2gray
from skimage.transform import rotate

from deskew import determine_skew


os.environ['OMP_THREAD_LIMIT'] = '1'

def get_grayscale(image):
    images = np.array(Image.open(image))

    gray = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('/home/pi/grayscale.jpg', gray)
    return gray


def remove_noise(image):
    return cv2.medianBlur(image, 1)


def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def dilate(image):
    kernel = np.ones((1, 1), np.uint8)
    return cv2.dilate(image, kernel, iterations=3)


def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=3)


def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


def closing(image):
    kernel = np.ones((1, 1), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)


def canny(image):
    return cv2.Canny(image, 100, 200)


def process_image(image_url):
    image = cv2.imread(image_url)

    # image.despeckle() # Reduces Noise Levels
    
    # Higher image resolution leads to slower
    # Processing, but better results, consider carefully
    #image = cv2.resize(image, (3350, 2280))
    
    # IMAGE PROCESSING
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Binarization
    
    #image = closing(image)
    
    image = dilate(image)
    image = remove_noise(image)

    adaptive_threshold = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 87, 13)

    # SHOW IMAGE
    # img_show(adaptive_threshold)

    cv2.imwrite('/home/pi/processed_image.jpg', adaptive_threshold)

    return image


def text_extraction(image, language):
    # --psm1
    print("extraction...")

    img = cv2.imread(image)

    config = '-l ' + language + ' --oem 3 --psm 3'
    text = pytesseract.image_to_string(img, config=config, lang=language)

    spell = Speller()
    text = spell(text)
    print("Extraction finished...")
    return text


def receipt_text_extraction(image, language):
    img = cv2.imread(image)
    text = pytesseract.image_to_string(img, lang=language)
    
    print("Extraction finished...")
    return text


def img_show(image):
    image = cv2.resize(image, (1200, 1000))
    cv2.imshow('page', image)
    cv2.waitKey(0)  # waits until a key is pressed
    cv2.destroyAllWindows()  # destroys the window showing image


def mistake_removal(input):
    text = input.strip()
    text = text.replace("©", "")
    text = text.replace("|", "I")
    text = text.replace("1", "I")
    text = text.replace("[", "")
    text = text.replace("]", "")
    text = text.replace("{", "")
    text = text.replace("<", "")
    text = text.replace(">", "")
    text = text.replace("-", "")
    text = text.replace("}", "")
    text = text.replace("\n", " ")
    text = ''.join(c if c not in map(str, range(0, 10)) else "" for c in text)
    textBlob = TextBlob(text)
    print(str(textBlob))
    return textBlob


def deskew(image):
    try:
        image = io.imread(image)
        angle = determine_skew(image)
        rotated = rotate(image, angle, resize=True) * 255
        io.imsave('/home/pi/deskewed_image.jpg', rotated.astype(np.uint8))
    except:
        pass
#gray = get_grayscale('/home/pi/Desktop/cornershop.jpg')
#cv2.imwrite('processed.jpg', gray)
#deskew('/home/pi/processed.jpg')

#process_image('/home/pi/Desktop/output-1.jpg')