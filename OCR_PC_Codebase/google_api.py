# Command in Terminal 
# python Scripts/google_ocr.py --image Images/hobbit.jpg --client Scripts/client_id.json

from google.oauth2 import service_account
from google.cloud import vision
import argparse
import cv2
import io

def draw_ocr_results(image, text, rect, color=(0, 255, 0)):
    (startX, startY, endX, endY) = rect
    cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
    cv2.putText(image, text, (startX, startY - 10),
    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    return image


if __name__ == '__main__':

    # Line Arguments Initialization
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="path to input image that we'll submit to Google Vision API")

    ap.add_argument("-c", "--client", required=True,
    help="path to input client ID JSON configuration file")
    args = vars(ap.parse_args())

    # Connecting to the Google Vision API
    credentials = service_account.Credentials.from_service_account_file(
    filename = args["client"],
    scopes = ["https://www.googleapis.com/auth/cloud-platform"])

    client = vision.ImageAnnotatorClient(credentials=credentials)
    with io.open(args["image"], "rb") as f:
        byteImage = f.read()


    # Sending Image as ByteImage to the API
    print("Making request to Google Vision API...")
    image = vision.Image(content=byteImage)
    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on errors, check:\n"
            "https://cloud.google.com/apis/design/errors".format(
            response.error.message))


    # Load returned text
    image = cv2.imread(args["image"])
    final = image.copy()

    for text in response.text_annotations[1::]:

        ocr = text.description
        print(ocr)

        startX = text.bounding_poly.vertices[0].x
        startY = text.bounding_poly.vertices[0].y
        endX = text.bounding_poly.vertices[1].x
        endY = text.bounding_poly.vertices[2].y
        rect = (startX, startY, endX, endY)


    # Show final image
    output = image.copy()
    output = draw_ocr_results(output, ocr, rect)
    final = draw_ocr_results(final, ocr, rect)

    #cv2.imshow("Output", output)
    #cv2.waitKey(0)

    #cv2.imshow("Final Output", final)
    #cv2.waitKey(0)

    print("OCR Finished Executing!")
