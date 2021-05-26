from imutils.perspective import four_point_transform
from textblob import TextBlob
import pytesseract
import argparse
import imutils
import cv2
import re


def parse_receipt(imageUrl, debug=False):
    # load receipt image
    orig = cv2.imread(imageUrl)
    image = orig.copy()
    image = imutils.resize(image, width=500)
    ratio = orig.shape[1] / float(image.shape[1])


    # edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
    edged = cv2.Canny(blurred, 75, 200)

    ##############################
    if debug > 0:
        cv2.imshow("Input", image)
        cv2.imshow("Edged", edged)
        cv2.waitKey(0)
    ##############################

    # find contours of receipt
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)


    # find largest contour
    receiptCnt = None

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            receiptCnt = approx
        break

    if receiptCnt is None:
        raise Exception("Could not find receipt outline. ")


    ##############################
    if debug > 0:
        output = image.copy()
        cv2.drawContours(output, [receiptCnt], -1, (0, 255, 0), 2)
        cv2.imshow("Receipt Outline", output)
        cv2.waitKey(0)
    ##############################


    # align receipt
    receipt = four_point_transform(orig, receiptCnt.reshape(4, 2) * ratio)
    cv2.imshow("Receipt Transform", imutils.resize(receipt, width=500))
    cv2.waitKey(0)


    # read text
    options = "--psm 4"
    text = pytesseract.image_to_string(
    cv2.cvtColor(receipt, cv2.COLOR_BGR2RGB),
    config = options)
    print(text)
    print("\n")


    #print prices
    pricePattern = r'([0-9]+\.[0-9]+)'
    print("[INFO] price line items:")
    print("========================")
    for r in text.split("\n"):
        if re.search(pricePattern, r) is not None:
            row = TextBlob(r)
            print(str(row))

