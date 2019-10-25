#!/usr/bin/env python3

import numpy as np
import cv2
import scipy.io

from ..utils.img_utils import plot_polygons

folder = '1571825077852250111'

ir = cv2.imread('ircam'+folder+'.png')
zed = cv2.imread('zedcam'+folder+'.png')

# load transformation info
points_dict = scipy.io.loadmat('./sensorfusion/cameramatching/points/'+folder+'/points.mat')
tf = points_dict['tform']
boxes = points_dict['boxes']

def get_boxes_zedframe(boxes,tform=tf):
	n = 0
	for (xA, yA, xB, yB) in boxes:
		
		w = xB - xA
		h = yB - yA
		box_corners = np.float32([[[xA,yA],[xB,yA],[xB,yB],[xA,yB]]])
		print(box_corners)
		box_warped = cv2.perspectiveTransform(box_corners, tform)
		if n == 0:
			boxes_tformed = box_warped
		else:
			boxes_tformed = np.vstack((box_warped, boxes_tformed))
		n += 1
	return boxes_tformed

def show_transform_box(tform,boxes,ir,zed):

	# create resizable windows for plotting
	cv2.namedWindow('IR',cv2.WINDOW_NORMAL)
	cv2.namedWindow('ZED',cv2.WINDOW_NORMAL)

	for box in boxes:
		box_corners = np.array([box])

		# plot bounding box for IR frame
		ir = plot_polygons(ir,box_corners[0])
		cv2.imshow("IR",ir)
		
		# transform bounding box coordinates to ZED frame
		box_warped = cv2.perspectiveTransform(box_corners, tform)

		# plot bounding box for ZED frame
		zed = plot_polygons(zed,box_warped[0])

	cv2.imshow("ZED",zed)

	key = cv2.waitKey(0) & 0xFF
	if key == ord("q"): cv2.destroyAllWindows()

#show_transform_box(tf,boxes,ir,zed)


