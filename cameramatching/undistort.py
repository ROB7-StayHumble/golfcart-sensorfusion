#!/usr/bin/env python3

import numpy as np
import cv2

def nothing(a): pass

cv2.namedWindow('undistort')
cv2.createTrackbar('k1','undistort',0,1000,nothing)
cv2.createTrackbar('k2','undistort',0,1000,nothing)
cv2.createTrackbar('p1','undistort',0,1000,nothing)
cv2.createTrackbar('p2','undistort',0,1000,nothing)
cv2.createTrackbar('k3','undistort',0,1000,nothing)

cv2.setTrackbarPos('k1','undistort',500)
cv2.setTrackbarPos('k2','undistort',500)
cv2.setTrackbarPos('p1','undistort',500)
cv2.setTrackbarPos('p2','undistort',500)
cv2.setTrackbarPos('k3','undistort',500)

src    = cv2.imread("ircam.png")
width  = src.shape[1]
height = src.shape[0]

distCoeff = np.zeros((5,1),np.float64)

# assume unit matrix for camera
cam = np.eye(3,dtype=np.float32)

cam[0,2] = width/2.0  # define center x
cam[1,2] = height/2.0 # define center y
cam[0,0] = 19.        # define focal length x
cam[1,1] = 19.        # define focal length y
print(cam)

x = width/2.0
y = height/2.0
fov = 63
fx = x / np.tan(np.deg2rad(fov/2))
fy = y / np.tan(np.deg2rad(fov/2))
cam2 = np.array([[fx, 0, x],
        [0, fy, y],
        [0, 0, 1]])
print(cam2)
# here the undistortion will be computed

cv2.imshow('src',src)

while(True):

    # get current positions of four trackbars
    k1 = cv2.getTrackbarPos('k1','undistort')
    k2 = cv2.getTrackbarPos('k2','undistort')
    p1 = cv2.getTrackbarPos('p1','undistort')
    p2 = cv2.getTrackbarPos('p2','undistort')
    k3 = cv2.getTrackbarPos('k3','undistort')

    # TODO: add your coefficients here!
    k1 = (k1-500) * 1.0e-3
    k2 = (k2-500) * 1.0e-3
    p1 = (p1-500) * 1.0e-3
    p2 = (p2-500) * 1.0e-3
    k3 = (k3-500) * 1.0e-3

    distCoeff[0,0] = k1
    distCoeff[1,0] = k2
    distCoeff[2,0] = p1
    distCoeff[3,0] = p2
    distCoeff[4,0] = k3

    dst = cv2.undistort(src,cam2,distCoeff)

    cv2.imshow('undistort',dst)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
