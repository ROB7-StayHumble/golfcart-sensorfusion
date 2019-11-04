import cv2
import numpy as np
import math
from sensorfusion.detection_hough.lanedetection import *

GAUSSIAN_SIZE = 5 # kernel size
CANNY_LOW = 5
CANNY_HIGH = 15

def is_theta_in_range(theta):
    return (theta < np.deg2rad(-10) and theta > np.deg2rad(-70)) or (theta > np.deg2rad(10) and theta < np.deg2rad(70))

def preprocessing(image):
    # only keep bottom part of image
    img = image[220:,:]

    # downsample image
    h,w = img.shape[:2]
    desired_w = 250
    small_to_large_image_size_ratio = 0.3125
    img = cv2.resize(img,
                       (0,0), # set fx and fy, not the final size
                       fx=small_to_large_image_size_ratio,
                       fy=small_to_large_image_size_ratio,
                       interpolation=cv2.INTER_LINEAR)

    blurred = cv2.GaussianBlur(img, (GAUSSIAN_SIZE, GAUSSIAN_SIZE), 0)
    return blurred

def draw_lanes(image):
    image = preprocessing(image)
    edges = cv2.Canny(image, CANNY_LOW, CANNY_HIGH, None, 3)
    return do_hough_straightline(image, edges, 2, 10, plot=False)

input = cv2.imread('/home/nemo/Documents/rob7/hough-lane-detect-python/cam_data/ir/ircam1571825284702254658.png')
output = draw_lanes(input)
cv2.imshow('out',output)
cv2.waitKey(0)
