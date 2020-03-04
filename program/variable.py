VIDEO_MODE = True
OUTPUT_IMG_DIR="./"


IMAGE_SIZE = 400



#tune these two numbers
YELLOW_MIN = (25,90,90)
YELLOW_MAX = (40,255,255)





#this will calculate the numbers needed for camera

#------------
CALIBRATION_DIST = 12 #inch
PIXEL_WIDTH = 85 #px
REAL_WIDTH = 8 #inch


#--do not touch

FOCAL_LENGTH = PIXEL_WIDTH * CALIBRATION_DIST / REAL_WIDTH
FOCAL_WIDTH = 0.2

