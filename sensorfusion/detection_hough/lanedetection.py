import cv2
import numpy as np
import math

GAUSSIAN_SIZE = 5 # kernel size
CANNY_LOW = 5
CANNY_HIGH = 15

def preprocessing(image):
    # only keep bottom part of image
    img = image[220:,:]

    # downsample image
    h,w = img.shape[:2]
    desired_w = 250
    small_to_large_image_size_ratio = 0.3125
    img = cv2.resize(img,
                       (0,0), # set fx and fy, not the final size
                       fx=small_to_large_image_size_ratio,
                       fy=small_to_large_image_size_ratio,
                       interpolation=cv2.INTER_LINEAR)

    blurred = cv2.GaussianBlur(img, (GAUSSIAN_SIZE, GAUSSIAN_SIZE), 0)
    return blurred

def draw_lanes(image):
    image = preprocessing(image)
    edges = cv2.Canny(image, CANNY_LOW, CANNY_HIGH, None, 3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 50, None, 0, 0)

    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            print(rho,theta)
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)

    return cdst, edges