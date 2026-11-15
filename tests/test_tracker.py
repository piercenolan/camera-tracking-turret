import cv2
import numpy as np

from src import tracker

LOWER = (20, 100, 100)  # yellow in OpenCV
UPPER = (40, 255, 255)
YELLOW_BGR = (0, 255, 255)


def make_frame(cx, cy, half=20):
    """Black 640x480 frame with a yellow square centered at (cx, cy)."""
    frame = np.zeros((480, 640, 3), np.uint8)
    frame[cy - half:cy + half + 1, cx - half: cx + half + 1] = YELLOW_BGR
    return frame

def centroid_of(frame, min_area=500):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = tracker.get_mask(hsv, LOWER, UPPER)
    return tracker.largest_centroid(mask, min_area)



def test_finds_known_blob_position():
    result = centroid_of(make_frame(320, 240))
    assert result is not None
    assert abs(result[0] - 320) <= 2
    assert abs(result[1] - 240) <= 2
def test_empty_frame_gives_no_target():
    assert centroid_of(np.zeros((480, 640, 3), np.uint8)) is None
