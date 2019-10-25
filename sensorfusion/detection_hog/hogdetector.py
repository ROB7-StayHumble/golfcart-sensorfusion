#!/usr/bin/env python3

# import the necessary packages
import numpy as np
import cv2
import imageio
import os

from ..utils.img_utils import downsample_image

# initialize the HOG descriptor/person detector
input_image_path = 'sensorfusion/cam_data'
output_image_path = 'sensorfusion/detection_hog/output'
total_box = 0

WIN_STRIDE = (8,8)
SCALE = None
PADDING = None

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detect_hog():
	#cv2.startWindowThread()
	#cv2.namedWindow('img',cv2.WINDOW_NORMAL)


	for file in sorted(os.listdir(input_image_path)):
		if 'zedcam' in file:
			#print('Reading', file)  
			original_image = imageio.imread(os.path.join(input_image_path, file))	# Reading image
			if original_image is not None:

				gray = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)

				boxes, weights = hog.detectMultiScale(original_image, winStride=WIN_STRIDE)
				boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
				for (xA, yA, xB, yB) in boxes:	
						cv2.rectangle(original_image, (xA, yA), (xB, yB),
				    		      (0, 255, 0), 2)
				#output_image = detect_object(original_image)	# detecting objects
			name = file.split('1',1)[1].split('.')[0] + file.split('1',1)[0] + '.png'
			print(name)
			imageio.imwrite(os.path.join(output_image_path, name), original_image[:, :, :])
			
			num_box = len(boxes)
			print(num_box)	

			#cv2.imshow("img", original_image)
			#cv2.waitKey(0)

	#cv2.destroyAllWindows()

