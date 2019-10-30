#!/usr/bin/env python2

# Import libraries
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from random import randrange, uniform

import rosbag
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

from sensorfusion.detection_hog.hogdetector import *
from sensorfusion.utils.img_utils import plot_boxes, plot_polygons
from sensorfusion.cameramatching.transformbox import get_boxes_zedframe

bridge = CvBridge()
bag = rosbag.Bag('testing2.bag')


### START QtApp #####
app = QtGui.QApplication([])            # you MUST do this once (initialize things)
####################

win = pg.GraphicsWindow(title="Golfcart sensors") # creates a window
#win_layout = win.addLayout(row=0, col=0)
#plot_view = win_layout.addViewBox(0,0)
#img_view = win_layout.addViewBox(0,1)

p_lidar = win.addPlot(title="LIDAR data",labels={'left':'Range (meters)','bottom':'Angle (degrees)'})  # creates empty space for the plot in the window
#plot_view.addItem(p_lidar)
curve_lidar = p_lidar.plot()                        # create an empty "plot" (a curve to plot)
p_lidar.setYRange(0, 50, padding=0)
p_lidar.showGrid(x=True,y=True)

p_ir = win.addPlot(title = 'IR cam')
imgItem_ir = pg.ImageItem()
curve_ir = p_ir.plot()
curve_ir.getViewBox().invertY(True)
curve_ir.getViewBox().setAspectLocked(True)
p_ir.hideAxis('left')
p_ir.hideAxis('bottom')
p_ir.addItem(imgItem_ir)

p_zed = win.addPlot(title = 'ZED cam')
imgItem_zed = pg.ImageItem()
curve_zed = p_zed.plot()
curve_zed.getViewBox().invertY(True)
curve_zed.getViewBox().setAspectLocked(True)
p_zed.hideAxis('left')
p_zed.hideAxis('bottom')
p_zed.addItem(imgItem_zed)

angles = np.arange(-90,90.5,0.5)
# Realtime data plot. Each time this function is called, the data display is updated
def update_lidar(lidar_ranges):
    global curve_lidar, angles    
    curve_lidar.setData(angles,lidar_ranges)          # set the curve with this data
    QtGui.QApplication.processEvents()    # you MUST process the plot now

zed_init = False
ircam_init = False
# Realtime data plot. Each time this function is called, the data display is updated
def update_ir(image):
    global imgItem_ir
    image = np.swapaxes(image,0,1)    
    imgItem_ir.setImage(image,autoDownsample=True)          # set the curve with this data
    QtGui.QApplication.processEvents()    # you MUST process the plot now
# Realtime data plot. Each time this function is called, the data display is updated
def update_zed(image):
    global imgItem_zed
    image = np.swapaxes(image,0,1)    
    imgItem_zed.setImage(image,autoDownsample=True)          # set the curve with this data
    QtGui.QApplication.processEvents()    # you MUST process the plot now


### MAIN PROGRAM #####    
# this is a brutal infinite loop calling your realtime data plot
for topic, msg, t in bag.read_messages():
    #print t, topic
    if topic == '/bottom_scan':
	    update_lidar(msg.ranges)
    elif topic in [	'/ircam_data',
        '/zed_node/rgb/image_rect_color']:
        image = bridge.imgmsg_to_cv2(msg, "bgr8")
        boxes = run_hog_on_img(image)
        if topic == '/ircam_data':
			if not ircam_init: ircam_init = True
			boxes_tformed = get_boxes_zedframe(boxes)
			update_ir(image)
        elif topic == '/zed_node/rgb/image_rect_color':
            img_people = plot_boxes(image, boxes)
            if not zed_init: zed_init = True
            if ircam_init:
                img_people = plot_polygons(image, boxes_tformed)
            update_zed(img_people)

### END QtApp ####
pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################
