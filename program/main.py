
import cv2
from algorithms import *
#from camera import *

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)


    last_tracked = None

    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
    


        bounding_circles, img = run_detection_on_frame(img, is_debug=False)

        last_tracked = run_custom_tracking_filter(bounding_circles, last_tracked, False)


        if(last_tracked != None):
            center = (last_tracked.x, last_tracked.y)
            radius = last_tracked.radius

            cv2.circle(img, center, radius,(0,255,0),2)
            predicted_size, predicted_angle = predict_location(last_tracked)
            

            
            #cv2.putText(img, str(circle.radius) , center , cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0), 2, cv2.LINE_AA)  
            #cv2.putText(img, "distance: " + str(predicted_size) + " in", (100,100), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0), 2, cv2.LINE_AA)  
        
        
        #print(bounding_circles)
        cv2.imshow('normal', img)

        
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()
        
show_webcam()