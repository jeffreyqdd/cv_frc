import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os
import pickle
import cv2
import glob
import math
from variable import *







def rescale_frame(frame, width=IMAGE_SIZE):
    #print(frame.shape[1],frame.shape[0])
    ratio = width * 1.0 / frame.shape[1]
    height = int(frame.shape[0] * ratio)
    dim = (width, height)
    
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

def run_detection_on_frame(image):
    #crop
    image = rescale_frame(image)

    #blur the image
    blurred = cv2.GaussianBlur(image, (11, 11), 0)

    #convert to hsv
    hsv_blurred = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    #erode and dialate
    mask = cv2.inRange(hsv_blurred, YELLOW_MIN, YELLOW_MAX)
    mask = cv2.erode(mask, None, iterations=3)
    mask = cv2.dilate(mask, None, iterations=3)

    #find contours
    im2,contours,hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #create bounding circles
    bounding_circle = []
    for cnt in contours:
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        bounding_circle.append(  Circle(radius, x,y)  )

        #cv2.putText(imag, str(radius) + ": " + str(center), (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0), 2, cv2.LINE_AA)    
        #cv2.circle(imag,center,radius,(0,255,0),2)

    return bounding_circle, image


def run_largest_bounding_filter(bounding_circles):
    if len(bounding_circles) == 0:
        return []
   
    curr = Circle(0, 0, 0)
    for circle in bounding_circles:
        if circle.radius > curr.radius:
            curr = circle
   
    return [curr]



def run_location_prediction_filter(bounding_circles, is_seen, last_known_center):
    
    if len(bounding_circles) == 0:
        is_seen = False
        return [], is_seen, last_known_center
    
    if is_seen == False:
        bounding_circles = (run_largest_bounding_filter(bounding_circles))
        last_known_center = bounding_circles[0]
    else:
        best = bounding_circles[0]
        #print(bounding_circles)
        for circle in bounding_circles:
            #print(circle)
            best_error = (best.center[0]  - last_known_center.center[0]) ** 2  + (best.center[1] - last_known_center.center[1]) ** 2
            curr_error = (circle.center[0] - last_known_center.center[0]) ** 2  + (circle.center[1] - last_known_center.center[1]) ** 2
            print(best_error, curr_error)

            if (curr_error < best_error):
                last_known_center = circle

    is_seen = True

    
    return [last_known_center], is_seen, last_known_center


def predict_location(circle):

    # calculate distance of object
    # W * D / P
    predicted_distance = REAL_WIDTH * FOCAL_LENGTH / circle.radius 

	
    # calculate angle offset of an object
    x_value = circle.center[0] - (IMAGE_SIZE / 2)
    predicted_angle = math.atan(x_value / 100)
    #print(x_value / (REAL_WIDTH * FOCAL_LENGTH))
    #print(x_value)

    return predicted_distance, x_value * 0.2

