"""Interactive HSV threshold tuning. Adjust trackbars until the target is
cleanly isolated in the mask window and nothing else is, then copy the
printed HSV_LOWER / HSV_UPPER values into config.py. Quit with 'q'."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from src import config
from src.camera import Camera, CameraDisconnected
from src.tracker import get_mask

WINDOW = "tune_hsv - mask"


def _nothing(_value):
    pass


def create_trackbars():
    cv2.namedWindow(WINDOW)
    h_lo, s_lo, v_lo = config.HSV_LOWER
    h_hi, s_hi, v_hi = config.HSV_UPPER
    cv2.createTrackbar("H low", WINDOW, h_lo, 179, _nothing)
    cv2.createTrackbar("S low", WINDOW, s_lo, 255, _nothing)
    cv2.createTrackbar("V low", WINDOW, v_lo, 255, _nothing)
    cv2.createTrackbar("H high", WINDOW, h_hi, 179, _nothing)
    cv2.createTrackbar("S high", WINDOW, s_hi, 255, _nothing)
    cv2.createTrackbar("V high", WINDOW, v_hi, 255, _nothing)


def read_trackbars():
    lower = (
        cv2.getTrackbarPos("H low", WINDOW),
        cv2.getTrackbarPos("S low", WINDOW),
        cv2.getTrackbarPos("V low", WINDOW),
    )
    upper = (
        cv2.getTrackbarPos("H high", WINDOW),
        cv2.getTrackbarPos("S high", WINDOW),
        cv2.getTrackbarPos("V high", WINDOW),
    )
    return lower, upper


def main():
    create_trackbars()
    lower, upper = config.HSV_LOWER, config.HSV_UPPER

    with Camera() as cam:
        print("Adjust trackbars until the target is cleanly isolated. Press 'q' to quit.")

        try:
            for frame in cam.frames():
                lower, upper = read_trackbars()
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = get_mask(hsv, lower, upper)
                isolated = cv2.bitwise_and(frame, frame, mask=mask)

                cv2.imshow("tune_hsv - frame", frame)
                cv2.imshow(WINDOW, mask)
                cv2.imshow("tune_hsv - isolated", isolated)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        except CameraDisconnected as e:
            print(e)

    cv2.destroyAllWindows()

    print("\nCopy these into config.py:")
    print(f"HSV_LOWER = {lower}")
    print(f"HSV_UPPER = {upper}")


if __name__ == "__main__":
    main()
