#!/usr/bin/env python2

import rosbag
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import matplotlib.pyplot as plt

from sensorfusion.detection_hog.hogdetector import *
from sensorfusion.utils.img_utils import plot_boxes, plot_polygons
from sensorfusion.cameramatching.transformbox import get_boxes_zedframe

bridge = CvBridge()

bag = rosbag.Bag('testing2.bag')

#cv2.namedWindow('peoples',cv2.WINDOW_NORMAL)

zed_init = False

for topic, msg, t in bag.read_messages():	
	if topic in [	'/ircam_data',
			'/zed_node/rgb/image_rect_color']:
		image = bridge.imgmsg_to_cv2(msg, "bgr8")
		print t,topic,image.shape
		boxes = run_hog_on_img(image)

		if topic == '/ircam_data':
			boxes_tformed = get_boxes_zedframe(boxes)
		else:
			if not zed_init: zed_init = True
			image_zed = image
			img_people = plot_boxes(image, boxes)
			print(boxes_tformed)
			img_people = plot_polygons(image, boxes_tformed)
		if zed_init:
			cv2.imshow('peoples',img_people)

			key = cv2.waitKey(500) & 0xFF
			if key == ord("q"):
				break

bag.close()
cv2.destroyAllWindows()
