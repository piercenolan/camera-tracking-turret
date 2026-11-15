"""Frame -> target centroid. See tools/try_tracker.py for the manual test."""

import cv2
import numpy as np

from src import config


def get_mask(hsv_frame, lower, upper):
    """Threshold an HSV frame to a binary mask and clean it up with erode/dilate."""
    mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))

    kernel = np.ones((config.MORPH_KERNEL_SIZE, config.MORPH_KERNEL_SIZE), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=config.MORPH_ITERATIONS)
    mask = cv2.dilate(mask, kernel, iterations=config.MORPH_ITERATIONS)
    return mask


def largest_centroid(mask, min_area):
    """Return the (x, y) centroid of the largest contour in mask, or None."""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    largest = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest) < min_area:
        return None

    moments = cv2.moments(largest)
    if moments["m00"] == 0:
        return None

    x = int(moments["m10"] / moments["m00"])
    y = int(moments["m01"] / moments["m00"])
    return (x, y)


def find_target(frame):
    """Return the (x, y) pixel centroid of the target color blob, or None."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = get_mask(hsv, config.HSV_LOWER, config.HSV_UPPER)
    return largest_centroid(mask, config.MIN_CONTOUR_AREA)
