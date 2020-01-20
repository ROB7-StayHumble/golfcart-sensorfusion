#!/usr/bin/env python3

import numpy as np
import cv2

src    = cv2.imread("./undistort_test/ircam1571825284702254658.png")

width  = src.shape[1]
height = src.shape[0]

x = width/2.0
y = height/2.0
fov = 63
fx = x / np.tan(np.deg2rad(fov/2))
fy = y / np.tan(np.deg2rad(fov/2))
cam2 = np.array([[fx, 0, x],
        [0, fy, y],
        [0, 0, 1]])
print(cam2)

distCoeff = np.array([-0.145,-0.024,0,0])
dst = cv2.undistort(src,cam2,distCoeff)
cv2.imwrite("./undistort_test/ircam1571825284702254658_undistorted.png",dst)
