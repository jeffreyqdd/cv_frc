import cv2
import math
from circle import *
from variable import *

'''
create a function that takes a input frame and scales it to the desired size

parameters:
    1) frame = image
    2) width = scaled_size
returns:
    1) resized image
'''

def rescale_frame(frame, width=IMAGE_SIZE):
    
    ratio = width * 1.0 / frame.shape[1]
    height = int(frame.shape[0] * ratio)

    dim = (width, height)
    
    return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)




'''
create a function that takes a imput frame and returns all possible balls
present in HSV color range [lower,upper]

parameters:
    1) image = image to analyze
    2) lower_bound = lower hsv bound
    3) upper_bound = upper hsv bound 

returns:
    1) list of Circle objects that are within hsv values [lower_bound, upper_bound]
    2) resized image
'''


def run_detection_on_frame(frame, lower_bound = YELLOW_MIN, upper_bound = YELLOW_MAX, is_debug = False):
    #crop
    frame = rescale_frame(frame)

    #blur the image
    blurred = cv2.GaussianBlur(frame, (1, 1), 0)

    #convert to hsv
    hsv_blurred = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    #erode and dialate
    mask = cv2.inRange(hsv_blurred, lower_bound, upper_bound)
    mask = cv2.erode(mask, None, iterations=3)
    mask = cv2.dilate(mask, None, iterations=3)

    #find contours
    im2,contours,hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #create bounding circles
    bounding_circle = []
    for cnt in contours:
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        bounding_circle.append(  Circle(radius, x,y)  )

        
    #only if debug
    if is_debug:
        cv2.imshow('hsv_blurred', hsv_blurred)
        cv2.imshow('mask', mask)

        for circle in bounding_circle:
            cv2.circle(frame, (circle.x, circle.y), circle.radius,(255,0,0),2)
    

    return bounding_circle, frame




'''
create a function takes a Circle object and predicts distance and angle offset

parameters:
    1) cicle = Circle object
    2) other parameters are default params and may be overridden for testing

returns:
    1) predicted distance (in)
    2) predicted angle offset (deg)
'''

def predict_location(circle, focal_length = FOCAL_LENGTH, object_width = REAL_WIDTH, focal_width = FOCAL_WIDTH):

    # calculate distance of object
    # W * D / P
    predicted_distance = object_width * focal_length / circle.radius 

	
    # calculate angle offset of an object
    # angular error is strictly proportional
    x_value = circle.x - (IMAGE_SIZE / 2)
    predicted_angle = x_value * focal_width
    #print(x_value / (REAL_WIDTH * FOCAL_LENGTH))
    #print(x_value)

    return predicted_distance, x_value * focal_width


'''
create a function that takes an array of circular objects and returns a circle object
closest to the object that is last seen. In the event that there is no last seen object
the function returns the closest ball. (tracking)

paramters:
    1) bounding_boxes = array of Circle objects
    2) last_circle = the circle that was last seen
    3) is_debugging = turns on or off print statements
returns:
    3) the circle believed to be the last seen circle

'''
def run_custom_tracking_filter(bounding_boxes, last_circle, is_debugging = False):
    if len(bounding_boxes) == 0:
        return None
    elif last_circle == None:
        bounding_boxes.sort(key=lambda x: x.radius, reverse=True)

        if is_debugging:
            print("first: ", bounding_boxes)
        #sorted(bounding_boxes, key = lambda x : x.radius)

        return bounding_boxes[0]
    else:
        best_circle = bounding_boxes[0]

        for curr_circle in bounding_boxes:
            
            best_error = (best_circle.x - last_circle.x) ** 2 + (best_circle.y - last_circle.y)**2 + (best_circle.radius - last_circle.radius) ** 2
            curr_error = (curr_circle.x - last_circle.x) ** 2 + (curr_circle.y - last_circle.y)**2 + (curr_circle.radius - last_circle.radius) ** 2

            if curr_error < best_error:
                best_circle = curr_circle
            
        if is_debugging:
            predicted_distance, predicted_angle = predict_location(best_circle)
            print(
                "tracking: ",
                round(predicted_distance,1), "in   ",
                round(predicted_angle,1), "deg   ", 
                best_circle.radius, "radius   "          
                )

        return best_circle
        




