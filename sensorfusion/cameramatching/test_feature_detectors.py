#!/usr/bin/env python3

import numpy as np
import cv2
from matplotlib import pyplot as plt

folder = '1571825077852250111'

ir = cv2.imread('ircam'+folder+'.png',0)
zed = cv2.imread('zedcam'+folder+'.png',0)

# Initiate SIFT detector
orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(ir,None)
kp2, des2 = orb.detectAndCompute(zed,None)

# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1,des2)

# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches.
img3 = cv2.drawMatches(ir,kp1,zed,kp2,matches[:20], None, flags=2)

plt.imshow(img3)
plt.savefig("feature_matching/feature_matching_orb.png", bbox_inches='tight', pad_inches=0)
plt.show()

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(ir,None)
kp2, des2 = sift.detectAndCompute(zed,None)
# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)
# Apply ratio test
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])
# cv.drawMatchesKnn expects list of lists as matches.
img3 = cv2.drawMatchesKnn(ir,kp1,zed,kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
plt.savefig("feature_matching/feature_matching_sift.png", bbox_inches='tight', pad_inches=0)
plt.imshow(img3),plt.show()
