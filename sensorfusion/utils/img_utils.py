#!/usr/bin/env python3

import cv2

def downsample_image(img, desired_width):
	h,w = img.shape[:2]
	small_to_large_image_size_ratio = desired_width/w
	img = cv2.resize(img,
		       (0,0), # set fx and fy, not the final size
		       fx=small_to_large_image_size_ratio,
		       fy=small_to_large_image_size_ratio,
		       interpolation=cv2.INTER_LINEAR)

	return img

	
