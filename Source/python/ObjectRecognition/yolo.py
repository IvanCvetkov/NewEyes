import os
import numpy as np
# import pyrealsense2 as rs
from gtts import gTTS
import time
import cv2

yolo_coco_labels = os.path.join(
    "/home/pi/yolo/darknet/data/coco.names")
yolo4tiny_cfg = os.path.join(
    "/home/pi/yolo/darknet/cfg/yolov4-tiny.cfg")
yolo4tiny_weights = os.path.join(
    "/home/pi/yolo/darknet/weights/yolov4-tiny.weights")

#yolo4_cfg = os.path.join("detectors/yolo_detector/weights/yolo4coco/yolo4.cfg")
#yolo4_weights = os.path.join(
#    "detectors/yolo_detector/weights/yolo4coco/yolo4.weights")


class Yolo:
    def __init__(self, config=yolo4tiny_cfg,
                 weights=yolo4tiny_weights,
                 labels=yolo_coco_labels,
                 confidence_param=0.3, thresh_param=0.25, use_cuda=False):
        print("[INFO] loading YOLO from disk...")
        self.net = cv2.dnn.readNetFromDarknet(
            os.path.join(config), os.path.join(weights))
        if use_cuda:
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.LABELS = open(os.path.join(labels)).read().strip().split("\n")
        np.random.seed(42)
        self.COLORS = np.random.randint(
            0, 255, size=(len(self.LABELS), 3), dtype="uint8")
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1]
                   for i in self.net.getUnconnectedOutLayers()]
        self.confidence_param = confidence_param
        self.thresh_param = thresh_param

    def detect(self, input_image, verbose=False):
        blob = cv2.dnn.blobFromImage(
            input_image, 1 / 255.0, (640, 480), swapRB=True, crop=False)
        self.net.setInput(blob)
        start = time.time()
        layerOutputs = self.net.forward(self.ln)
        end = time.time()
        # show timing information on YOLO
        if verbose:
            print("[INFO] YOLO took {:.6f} seconds".format(end - start))
        return layerOutputs

    def draw_results_no_depth(self, layerOutputs, input_image):
        return self.draw_results(layerOutputs, input_image)

    def draw_results(self, layerOutputs, input_image, aligned_depth_frame=None, depth_scale=None, verbose=None):
        (H, W) = input_image.shape[:2]
        boxes = []
        confidences = []
        classIDs = []
        items = ''
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
                if confidence > self.confidence_param:
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
                    if verbose:
                        print([x, y, int(width), int(height)])
                        print(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_param,
                                self.thresh_param)
        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                distance = None
                distance_center = None
                if aligned_depth_frame and depth_scale:
                    # Good accuracy
                    distance_center = self.get_distance_center(
                        aligned_depth_frame, depth_scale, x, y, w, h, self.LABELS[classIDs[i]])
                    # Better accuracy for objects that completely fill the bounding box, otherwise distance becomes inaccuraty
                    # distance = self.get_distance_bounding_box(
                    #     aligned_depth_frame, depth_scale, x, y, w, h, self.LABELS[classIDs[i]])
                # draw a bounding box rectangle and label on the image
                col = [int(c) for c in self.COLORS[classIDs[i]]]
                cv2.rectangle(input_image, (x, y), (x + w, y + h), col, 2)
                # add dot at center
                cv2.circle(input_image, (int((x + (x + w))/2),
                                         int((y + (y + h))/2)), radius=3, color=col, thickness=3)
                if distance_center:
                    text = "{}: {:.4f} : distance {:.4f}m".format(
                        self.LABELS[classIDs[i]], confidences[i], distance_center)
                else:
                    text = "{}: {:.4f}".format(
                        self.LABELS[classIDs[i]], confidences[i])
                    items = items + 'a ' + self.LABELS[classIDs[i]] + ", "
                    
                cv2.putText(input_image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, col, 2)
            
            print(items)
            
            if items != '':
                tts = gTTS(items)
                tts.save('yolo_objects.mp3')


        # Compute distance to center of img
        if aligned_depth_frame and depth_scale:
            col_center = (0, 0, 255)

            height, width, channels = input_image.shape
            upper_left = ((width // 4) + 200, (height // 4))
            bottom_right = ((width * 3 // 4) - 200, (height * 3 // 4)+100)
            # draw in the image

            # dist = self.get_distance(aligned_depth_frame, depth_scale, x,y,w,h, 'center')
            cv2.rectangle(input_image, upper_left, bottom_right,
                          (0, 255, 0), thickness=1)

            # cv2.rectangle(input_image, (x,y), (x + w, y + h), col_center, 2)
            # add dot at center
            cv2.circle(input_image,  (int(width/2), int(height/2)),
                       radius=3, color=col_center, thickness=3)
            # cv2.putText(input_image, 'Frame  center: : distance {:.4f}m'.format(dist), (center_coordinates[0], center_coordinates[1] - 5), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.5, col_center, 2)

        return input_image

    # Calculates the distance to the center of the bounding box
    # Good accuracy in general, not big deviations from ground truth
    def get_distance_center(self, aligned_depth_frame, depth_scale, x, y, w, h, label, verbose=False):
        # center distance measurement
        cx = int((x + (x + w))/2)
        cy = int((y + (y + h))/2)

        dist = aligned_depth_frame.get_distance(int(cx), int(cy))
        if verbose:
            print("Distance measurement Realsense... Detected {} {} meters away".format(
                label, dist))
        return dist

    # Help method to compute distance from depth for bounding box
    # Good accuracy for objects that completely fill the bounding box, otherwise there are inaccuracies
    def get_distance_bounding_box(self, aligned_depth_frame, depth_scale, x, y, w, h, label, verbose=False):
        return self.get_distance(aligned_depth_frame, depth_scale, x, y, w, h, label, verbose=False)

    # Calculates distance based on mean of all the values in the cropped from the depth image segment

    def get_distance(self, aligned_depth_frame, depth_scale, x, y, w, h, label, verbose=False):
        xmin_depth = int(x)
        ymin_depth = int(y)
        xmax_depth = int(x + w)
        ymax_depth = int(y + h)

        xmin_depth, ymin_depth, xmax_depth, ymax_depth

        depth = np.asanyarray(aligned_depth_frame.get_data())

        # Crop depth data:
        depth = depth[xmin_depth:xmax_depth,
                      ymin_depth: ymax_depth].astype(float)

        # Get data scale from the device and convert to meters
        depth = depth * depth_scale
        dist, _, _, _ = cv2.mean(depth)

        if verbose:
            print("Detected a {0} {1:.3} meters away.".format(label, dist))

        return dist
