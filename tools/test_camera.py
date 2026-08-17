"""Manual test: show the raw camera feed with a live FPS overlay. Quit with 'q'."""

import sys
import time
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2

from src.camera import Camera

FPS_WINDOW = 30
MAX_CONSECUTIVE_DROPPED_FRAMES = 10


def main():
    frame_times = deque(maxlen=FPS_WINDOW)
    dropped_in_a_row = 0

    with Camera() as cam:
        print(f"Camera opened at index {cam.index} ({cam.width}x{cam.height}). Press 'q' to quit.")

        while True:
            frame = cam.read()

            if frame is None:
                dropped_in_a_row += 1
                if dropped_in_a_row >= MAX_CONSECUTIVE_DROPPED_FRAMES:
                    print(f"No frame after {dropped_in_a_row} consecutive attempts. Camera may have disconnected.")
                    break
                continue
            dropped_in_a_row = 0

            frame_times.append(time.perf_counter())
            fps = 0.0
            if len(frame_times) >= 2:
                elapsed = frame_times[-1] - frame_times[0]
                if elapsed > 0:
                    fps = (len(frame_times) - 1) / elapsed

            cv2.putText(
                frame, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2,
            )
            cv2.imshow("test_camera", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
