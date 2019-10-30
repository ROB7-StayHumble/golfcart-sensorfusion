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

bridge = CvBridge()
bag = rosbag.Bag('testing2.bag')


### START QtApp #####
app = QtGui.QApplication([])            # you MUST do this once (initialize things)
####################

win = pg.GraphicsWindow(title="Golfcart sensors") # creates a window
p_lidar = win.addPlot(title="LIDAR data")  # creates empty space for the plot in the window
curve_lidar = p.plot()                        # create an empty "plot" (a curve to plot)

angles = np.arange(-90,90.5,0.5)

# Realtime data plot. Each time this function is called, the data display is updated
def update(ranges):
    global curve_lidar, angles    
    curve_lidar.setData(angles,ranges)          # set the curve with this data
    QtGui.QApplication.processEvents()    # you MUST process the plot now

### MAIN PROGRAM #####    
# this is a brutal infinite loop calling your realtime data plot
for topic, msg, t in bag.read_messages():	
    print t, topic
    if topic == '/bottom_scan':
	    update(msg.ranges)


### END QtApp ####
pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################
