#!/usr/bin/env python2

# Import libraries
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from random import randrange, uniform

import rosbag
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks

from sensorfusion.detection_hog.hogdetector import *
from sensorfusion.utils.img_utils import *
from sensorfusion.cameramatching.transformbox import get_boxes_zedframe

H_ZED = 720
W_ZED = 1280
H_IR = 600
W_IR = 800

bridge = CvBridge()
bag = rosbag.Bag('testing2.bag')


### START QtApp #####
app = QtGui.QApplication([])            # you MUST do this once (initialize things)
####################

win = pg.GraphicsWindow(title="Golfcart sensors") # creates a window
#win_layout = win.addLayout(row=0, col=0)
#plot_view = win_layout.addViewBox(0,0)
#img_view = win_layout.addViewBox(0,1)

p_lidar = win.addPlot(row=1, col=1, title="LIDAR data",labels={'left':'Range (meters)','bottom':'Angle (degrees)'})  # creates empty space for the plot in the window
#plot_view.addItem(p_lidar)
curve_lidar = p_lidar.plot()                        # create an empty "plot" (a curve to plot)
curve_lidar_smooth = p_lidar.plot()                        # create an empty "plot" (a curve to plot)
p_lidar.showGrid(x=True,y=True)

curve_lidar.getViewBox().invertX(True)
curve_lidar.getViewBox().setLimits(yMin=0,yMax=80)
curve_lidar.getViewBox().setAspectLocked(True)
#p_lidar.setYRange(0, 50, padding=0)
curve_lidar_smooth.setPen(pg.mkPen({'color': (100, 255, 255, 150), 'width': 4}))

p_ir = win.addPlot(row=1, col=2, rowspan=2, title = 'IR cam')
imgItem_ir = pg.ImageItem()
curve_ir = p_ir.plot()
curve_ir.getViewBox().invertY(True)
curve_ir.getViewBox().setAspectLocked(True)
p_ir.hideAxis('left')
p_ir.hideAxis('bottom')
p_ir.addItem(imgItem_ir)

p_zed = win.addPlot(row=2, col=1, title = 'ZED cam')
imgItem_zed = pg.ImageItem()
curve_zed = p_zed.plot()
curve_zed.getViewBox().invertY(True)

curve_zed.getViewBox().setLimits(xMin=0,xMax=W_ZED)
curve_zed.getViewBox().setAspectLocked(True)
p_zed.hideAxis('left')
p_zed.hideAxis('bottom')
p_zed.addItem(imgItem_zed)

#cross hair
vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen({'color': (0, 255, 0, 100), 'width': 4}))
#p_lidar.addItem(vLine, ignoreBounds=True)
angleLines = []

def show_lane_direction(angles):
    for line in angleLines:
        p_ir.removeItem(line)
    for angle in angles:
        angleLine = pg.InfiniteLine(pos=(W_IR/2,H_IR), angle=90-angle, movable=False, pen=pg.mkPen({'color': (0, 255, 0, 100), 'width': 4}))
        angleLines.append(angleLine)
        p_ir.addItem(angleLine, ignoreBounds=True)

def angles_of_max_ranges(data_x,data_y):
    peaks, props = find_peaks(data_y, height=30)
    if not len(peaks):
        peaks, props = find_peaks(data_y, height=10)
        peaks = [sorted(peaks,key=lambda x: data_x[x],reverse=True)[0]]
    angles = [data_x[i_max] for i_max in peaks]
    return angles
    
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filtfilt(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y
    
def smooth_lidar_data(method,data_x,data_y):
    if method == 'poly':
        poly = np.polyfit(data_x,data_y,15)
        poly_y = np.poly1d(poly)(data_x)
        return poly_y
    elif method == 'butter':
        cutoff = 1500
        fs = 100000
        return butter_lowpass_filtfilt(data_y, cutoff, fs)


angles = np.arange(-90,90.5,0.5)
# Realtime data plot. Each time this function is called, the data display is updated
def update_lidar(lidar_ranges):
    global curve_lidar, angles
    angleLines = []    
    smooth = smooth_lidar_data('butter',angles,lidar_ranges)
    curve_lidar.setData(angles,lidar_ranges)
    curve_lidar_smooth.setData(angles,smooth)
    lane_angles = angles_of_max_ranges(angles,smooth)
    show_lane_direction(lane_angles)
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

n_frame = 0 # for counting frames
people_angles = []
### MAIN PROGRAM #####    
# this is a brutal infinite loop calling your realtime data plot
for topic, msg, t in bag.read_messages():
    n_frame += 1 
    #if t > rospy.Time(1571746650.00000):
    if topic == '/bottom_scan':
        ranges = np.array(msg.ranges)
        ranges[ranges == 0] = 50
        update_lidar(ranges)
    elif topic in [	'/ircam_data',
        '/zed_node/rgb/image_rect_color']:
        image = bridge.imgmsg_to_cv2(msg, "bgr8")
        boxes = run_hog_on_img(image)
        if topic == '/ircam_data':
            if not ircam_init: ircam_init = True
            people_angles = [angle_from_box(image,box) for box in boxes]
            if people_angles: vLine.setPos(people_angles[0])
            boxes_tformed = get_boxes_zedframe(boxes)
            img_people = plot_boxes(image, boxes, color='blue')
            update_ir(img_people)
        elif topic == '/zed_node/rgb/image_rect_color':
            img_people = plot_boxes(image, boxes, color='green')
            if not zed_init: zed_init = True
            if ircam_init:
                img_people = plot_polygons(image, boxes_tformed, color='blue')
            update_zed(img_people)

### END QtApp ####
pg.QtGui.QApplication.exec_() # you MUST put this at the end
##################
