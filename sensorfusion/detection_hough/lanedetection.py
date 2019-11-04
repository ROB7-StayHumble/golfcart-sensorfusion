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


def plot_line(a, b, rho, img, opacity=0.8, color='firebrick'):
    y_max, x_max = img.shape[:2]
    pt1 = (0, int(a * 0 + b))
    pt2 = (x_max, int(a * x_max + b))
    cv2.line(img, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)
    print(a, b)
    return img


def is_theta_in_range(theta):
    return (theta < np.deg2rad(-10) and theta > np.deg2rad(-70)) or (theta > np.deg2rad(10) and theta < np.deg2rad(70))


def do_hough_straightline(orig, img, n_lines, max_area, plot=False):
    # Copy edges to the images that will display the results in BGR
    color_edges = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # img = img[10:-10][10:-10] # ignore image boundaries
    # print("-------------------------------------")
    max_iterations = 20

    h, w = img.shape
    h_orig, w_orig = orig.shape[:2]
    middle = w / 2
    diag = np.ceil(np.hypot(h, w))
    # print(f"IMG dimensions: {img.shape} max. intensity: {np.max(img)}")

    thetas = np.deg2rad(np.arange(-90.0, 90.0))
    rhos = np.linspace(-diag, diag, diag * 2.0)

    # print(f"diagonal: {diag}")

    accumulator = np.zeros((np.uint64(2 * diag), len(thetas)), dtype=np.uint64)

    for i in range(0, h):
        for j in range(0, w):
            if img[i, j] > 0:  # if we're on an edge
                for theta_i in range(len(thetas)):  # calculate rho for every theta
                    theta = thetas[theta_i]
                    if is_theta_in_range(theta):
                        rho = np.round(j * np.cos(theta) + i * np.sin(theta)) + diag
                        # print("point",(i,j),"rho",rho,"theta",theta)
                        rho = np.uint64(rho)
                        accumulator[rho, theta_i] += 1  # increment accumulator for this coordinate pair

    n = 1
    iterations = 0

    while n <= n_lines and iterations < max_iterations:
        # print(iterations)
        # find maximum point in accumulator
        # result = np.where(accumulator == np.max(accumulator))
        # print("max. in accumulator:", np.max(accumulator))
        # maxCoordinates = list(zip(result[0], result[1]))
        # print(maxCoordinates)

        max_index = np.argmax(accumulator)  # 2d index of maximum point in accumulator
        theta_index = np.uint64(max_index % accumulator.shape[1])
        rho_index = np.uint64(max_index / accumulator.shape[1])

        # cv2.circle(accumulator, (rho_index,theta_index), 50, (0,255,0), thickness=5, lineType=8, shift=0)

        ang = thetas[theta_index]
        rho = rhos[rho_index]

        # print(f"Hough coordinates: rho {rho:.2f}  theta(rad) {ang:.2f}  theta(deg) {np.rad2deg(ang)}")

        if n == 1:
            lane1_pos = (ang > 0)
            a = -(np.cos(ang) / np.sin(ang))
            b = rho / np.sin(ang)
            lane1_start = ((h - 1) - b) / a
            lane1_end = -b / a
            lane1_side = (lane1_start < middle)
            # print(f"- Lane 1: Cartesion form (ax+b): {a:.2f} * x + {b:.2f}")
            # print(f"\t starting at y = ", lane1_start)
            color_edges = plot_line(a, b, rho, color_edges, color='green')
            n += 1
        elif n == 2:
            lane2_pos = (ang > 0)
            a = -(np.cos(ang) / np.sin(ang))
            b = rho / np.sin(ang)
            lane2_start = ((h - 1) - b) / a
            lane2_end = -b / a
            lane2_side = (lane2_start < middle)
            if (lane1_side != lane2_side) and ((lane2_end > lane1_end and lane2_start > lane1_start) or (
                    lane2_end < lane1_end and lane2_start < lane1_start)):
                # print(f"- Lane 2: Cartesion form (ax+b): {a:.2f} * x + {b:.2f}")
                # print(f"\t starting at y = ", lane2_start)
                color_edges = plot_line(a, b, rho, color_edges, color='blue')
                n += 1

        prev_ang = ang
        prev_rho = rho

        remove_area = max_area
        for i in range(np.int(rho_index - remove_area), np.int(rho_index + remove_area + 1)):
            try:
                accumulator[i][np.int(theta_index - remove_area):np.int(theta_index + remove_area)] = 0
            except:
                pass

        iterations += 1

    return color_edges


def draw_lanes(image):
    image = preprocessing(image)
    edges = cv2.Canny(image, CANNY_LOW, CANNY_HIGH, None, 3)
    return do_hough_straightline(image, edges, 2, 10, plot=False)
