#!/usr/bin/env python2

import rosbag
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import matplotlib.pyplot as plt

bridge = CvBridge()

bag = rosbag.Bag('testing2.bag')

angles = np.arange(-90,90.5,0.5)
print(len(angles))
plt.ion()
fig = plt.figure()
ax=fig.add_subplot(111)
ax.set_xlim([-90,90])
ax.set_ylim([0,10])
line,  = ax.plot(angles,np.zeros_like(angles))
ax.invert_xaxis()
fig.show()

for topic, msg, t in bag.read_messages():	
	if topic in [	'/ircam_data',
			'/zed_node/rgb/image_rect_color']:
		image = bridge.imgmsg_to_cv2(msg, "bgr8")
		print t,topic,image.shape
		if topic == '/ircam_data':
			ircam_last = image
			cv2.imshow('ircam',ircam_last)
		elif topic == '/zed_node/rgb/image_rect_color':
			zed = image
			#cv2.imshow('zed',zed)
			#cv2.imwrite('./zedcam'+str(t)+'.png',zed)
		key = cv2.waitKey(0) & 0xFF
		if key == ord("s"):
			cv2.imwrite('./ircam'+str(t)+'.png',ircam_last)
			try: cv2.imwrite('./zedcam'+str(t)+'.png',zed)
			except: pass
		elif key == ord("q"):
			break
	elif topic == '/bottom_scan':
		scan_data = msg
		print t,topic
		line.set_data(angles,scan_data.ranges)
		fig.canvas.draw()

bag.close()
cv2.destroyAllWindows()
