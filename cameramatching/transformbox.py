#!/usr/bin/env python3

import numpy as np
import cv2

def transform_box(tform,box_corners,ir,zed):

	# create resizable windows for plotting
	cv2.namedWindow('IR',cv2.WINDOW_NORMAL)
	cv2.namedWindow('ZED',cv2.WINDOW_NORMAL)

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

tf = np.float32([[ 9.84948418e-01, -1.43587405e-01,  2.96846573e+02],
 [ 4.95329092e-02,  8.53635664e-01,  1.10887223e+01],
 [ 9.78910279e-05, -2.25220225e-04,  1.00000000e+00]])


ir = cv2.imread("ircam.png")
zed = cv2.imread("zedcam.png")
box_corners = np.float32([[[520,265],[520+205,265],[520+205,265+330],[520,265+330]]])

ir = cv2.imread("ircam1571825077852250111.png")
zed = cv2.imread("zedcam1571825077852250111.png")
box_corners = np.float32([[[204.8,196.2],[278.2,196.2],[278.2,370.3],[203.3,370.3]]])


transform_box(tf,box_corners,ir,zed)


