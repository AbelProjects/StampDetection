import numpy as np
import cv2
import sys
import os
import matplotlib.pyplot as plt
from typing import Tuple, List
from numpy import ndarray


def image_imshow(img: ndarray, figsize: Tuple[int, int] = (10, 10)) -> None:
    fig = plt.figure(figsize=figsize)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()


def _blue_color_mask(img: ndarray) -> ndarray:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blue_lower = np.array([80, 30, 30])
    blue_higher = np.array([140, 250, 250])
    mask = cv2.inRange(hsv, blue_lower, blue_higher)
    selection = cv2.bitwise_and(gray, gray, mask=mask)
    selection_blur = cv2.GaussianBlur(selection, (7, 7), 3)
    return selection_blur


def _find_circles(img: ndarray) -> ndarray:
    min_rad = round(img.shape[0] * 17 / 297)
    max_rad = round(img.shape[0] * 30 / 297)
    dist_stamps = 2 * min_rad
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT_ALT, 1.5, dist_stamps, param1=200,
                               param2=0.4, minRadius=min_rad, maxRadius=max_rad)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        return circles[0, :]
    else:
        return np.array([])


def _delete_duplicate_circles(circles: ndarray):
    hashmap = {}
    for x, y, r in circles:
        if (x, y) not in hashmap.keys():
            hashmap[(x, y)] = r
        else:
            if hashmap[(x, y)] <= r:
                hashmap[(x, y)] = r
            else:
                continue
    circles = np.array([[key[0], key[1], hashmap[key]] for key in hashmap.keys()])
    return circles


def image_find_stamps(img: ndarray) -> ndarray:
    return _delete_duplicate_circles(_find_circles(_blue_color_mask(img)))


def stamp_quantity_from_circles(circles: ndarray) -> int:
    return len(circles)


def is_stamped_from_circles(circles: ndarray) -> bool:
    if len(circles) > 0:
        return True
    else:
        return False


def image_draw_circles(img: ndarray, circles: ndarray) -> ndarray:
    for i in circles:
        cv2.circle(img, (i[0], i[1]), i[2], (165, 25, 165), 2)
    return img


def _square_from_circle(circle: ndarray) -> ndarray:
    center = (circle[0], circle[1])
    r = circle[2]
    side = 2*r
    left_corner = center[0] - r, center[1] - r
    right_corner = left_corner[0] + side, left_corner[1] + side
    return np.array([left_corner, right_corner])


def squares_from_circles(circles: ndarray) -> ndarray:
    squares = []
    for circle in circles:
        squares.append(_square_from_circle(circle))
    return np.array(squares)


def _stamp_box(img: ndarray, square: ndarray) -> ndarray:
    new_img = img[square[0][1]:square[1][1], square[0][0]:square[1][0],:]
    return new_img


def stamp_boxes(img: ndarray, squares: ndarray) -> ndarray:
    box_array = np.array([])
    for box in squares:
        box_img = _stamp_box(img, box)
        np.append(box_array, box_img)
    return box_array
