#!/usr/bin/env python3

import cv2
import numpy as np

colors = {
            'white':(255, 255, 255),
            'black':(0,0,0),
            'green':(0, 255, 0),
            'blue':(0,255,255)
}

def plot_boxes(img, boxes, color='white'):
	global colors
	for (xA, yA, xB, yB) in boxes:	
		cv2.rectangle(img, (xA, yA), (xB, yB), colors[color], 5)
	return img

def plot_polygons(img, polygons, color='white'):
	global colors
	for polygon in polygons:
		#print(polygon)
		pts = np.int32(polygon).reshape((-1,1,2))
		cv2.polylines(img,[pts],True,colors[color],5)
	return img

def downsample_image(img, desired_width):
	h,w = img.shape[:2]
	small_to_large_image_size_ratio = desired_width/w
	img = cv2.resize(img,
		       (0,0), # set fx and fy, not the final size
		       fx=small_to_large_image_size_ratio,
		       fy=small_to_large_image_size_ratio,
		       interpolation=cv2.INTER_LINEAR)

	return img

	
