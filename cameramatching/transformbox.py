#!/usr/bin/env python3

import numpy as np
import cv2
import scipy.io

def transform_box(tform,boxes,ir,zed):

	# create resizable windows for plotting
	cv2.namedWindow('IR',cv2.WINDOW_NORMAL)
	cv2.namedWindow('ZED',cv2.WINDOW_NORMAL)

	for box in boxes:
		box_corners = np.array([box])

		# plot bounding box for IR frame
		pts = np.int32(box_corners[0].reshape(-1,1,2))
		cv2.polylines(ir,[pts],True,(0,0,255),5)
		cv2.imshow("IR",ir)

		# transform bounding box coordinates to ZED frame
		box_warped = cv2.perspectiveTransform(box_corners, tform)

		# plot bounding box for ZED frame
		pts = np.int32(box_warped[0]).reshape((-1,1,2))
		cv2.polylines(zed,[pts],True,(0,255,255),5)

	cv2.imshow("ZED",zed)

	key = cv2.waitKey(0) & 0xFF
	if key == ord("q"): cv2.destroyAllWindows()

folder = '1571825077852250111'

ir = cv2.imread('ircam'+folder+'.png')
zed = cv2.imread('zedcam'+folder+'.png')

# load transformation info
points_dict = scipy.io.loadmat('./points/'+folder+'/points.mat')
tf = points_dict['tform']
boxes = points_dict['boxes']

transform_box(tf,boxes,ir,zed)


