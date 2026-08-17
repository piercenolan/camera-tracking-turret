"""Camera capture wrapper. See tools/test_camera.py for the manual test."""

import cv2

from src import config


class CameraDisconnected(RuntimeError):
    """Raised by Camera.frames() after too many consecutive failed reads."""


class Camera:
    """Thin wrapper around cv2.VideoCapture with clean open/release semantics."""

    def __init__(self, index=None, width=None, height=None):
        self.index = config.CAMERA_INDEX if index is None else index
        self.width = config.FRAME_WIDTH if width is None else width
        self.height = config.FRAME_HEIGHT if height is None else height
        self._cap = None

    def open(self):
        self._cap = cv2.VideoCapture(self.index)
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        if not self._cap.isOpened():
            self._cap.release()
            self._cap = None
            raise RuntimeError(
                f"Could not open camera at index {self.index}. "
                "Try a different CAMERA_INDEX in config.py."
            )

        return self

    def read(self):
        """Return the next frame, or None if the grab failed."""
        if self._cap is None:
            raise RuntimeError("Camera is not open. Call open() first.")

        ok, frame = self._cap.read()
        return frame if ok else None

    def frames(self):
        """Yield frames forever. A single dropped frame is skipped silently;
        after config.MAX_CONSECUTIVE_DROPPED_FRAMES in a row (camera likely
        disconnected), raises CameraDisconnected instead of looping forever."""
        dropped_in_a_row = 0
        while True:
            frame = self.read()

            if frame is None:
                dropped_in_a_row += 1
                if dropped_in_a_row >= config.MAX_CONSECUTIVE_DROPPED_FRAMES:
                    raise CameraDisconnected(
                        f"No frame after {dropped_in_a_row} consecutive attempts. "
                        "Camera may have disconnected."
                    )
                continue

            dropped_in_a_row = 0
            yield frame

    def release(self):
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
        return False
