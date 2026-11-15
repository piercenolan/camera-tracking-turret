"""Manual test: overlay the detected target centroid on the live feed.
Confirms config.py's HSV bounds (set via tune_hsv.py) track smoothly as the
target moves. Quit with 'q'."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from src.camera import Camera, CameraDisconnected
from src.tracker import find_target


def main():
    with Camera() as cam:
        print("Move the target through the frame. Press 'q' to quit.")

        try:
            for frame in cam.frames():
                target = find_target(frame)

                if target is not None:
                    x, y = target
                    cv2.drawMarker(
                        frame, (x, y), (0, 255, 0),
                        markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2,
                    )
                    cv2.circle(frame, (x, y), 15, (0, 255, 0), 2)
                    cv2.putText(
                        frame, f"({x}, {y})", (x + 20, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2,
                    )
                else:
                    cv2.putText(
                        frame, "no target", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2,
                    )

                cv2.imshow("test_tracker", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        except CameraDisconnected as e:
            print(e)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
