#!/usr/bin/env python3

import numpy as np
import cv2
import scipy.io

folder = 'lab'

# load corresponding set of points
points_dict = scipy.io.loadmat('./points/'+folder+'/points.mat')
zedcam_features = points_dict['matchedPtsOriginal']
ircam_features = points_dict['matchedPtsDistorted']

img_ircam = cv2.imread('ircam'+folder+'.png')
img_zed = cv2.imread('zedcam'+folder+'.png')

#ircam_corners = np.float32([[210.8,157.2], [540.8,158.8], [534.8,383.8],[221.3,436.3]])
#zedcam_corners = np.float32([[486.7,161.8], [795.7,178.3], [788.2,391.3], [495.7,433.2]])

h,w = img_zed.shape[:2]

tform, mask = cv2.findHomography(ircam_features, zedcam_features)
print(tform)

# write transformation to points file
points_dict['tform'] = tform
scipy.io.savemat('./points/'+folder+'/points.mat',points_dict)

# display result
warped = cv2.warpPerspective(img_ircam, tform, (w,h))

for i in zedcam_features:
	i = np.uint32(i)
	warped[i[1],i[0]] = [0,0,255]

cv2.imshow("dst", warped)

key = cv2.waitKey(0) & 0xFF
if key == ord("q"): cv2.destroyAllWindows()
