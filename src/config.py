"""
All tunable constants for the turret, in one place.

Every value below is a PLACEHOLDER. Nothing here has been measured or tuned
yet — that happens milestone by milestone (tune_hsv.py, try_serial.py,
main.py). Do not hardcode any of these elsewhere; import from here instead.
"""

# ---------------------------------------------------------------------------
# Camera (Milestone 1)
# ---------------------------------------------------------------------------
CAMERA_INDEX = 1            # cv2.VideoCapture device index; may not be the USB cam
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
MAX_CONSECUTIVE_DROPPED_FRAMES = 10  # Camera.frames() raises CameraDisconnected past this

# ---------------------------------------------------------------------------
# Tracker / HSV color threshold (Milestone 2)
# Six bounds set interactively with tools/tune_hsv.py, then copied here.
# Currently tuned for: a lemon.
# ---------------------------------------------------------------------------
HSV_LOWER = (9, 191, 80)
HSV_UPPER = (127, 255, 255) 
MIN_CONTOUR_AREA = 500      # px^2 below which a detection is rejected as noise

MORPH_KERNEL_SIZE = 5       # erode/dilate kernel is MORPH_KERNEL_SIZE x MORPH_KERNEL_SIZE
MORPH_ITERATIONS = 2        # erode/dilate passes; higher = cleans more noise, costs more time

# ---------------------------------------------------------------------------
# Serial / Arduino (Milestone 3)
# Board: Elegoo Uno R3. Pan servo -> pin 9, tilt servo -> pin 10.
# ---------------------------------------------------------------------------
SERIAL_PORT = "COM3"        # placeholder — check Device Manager / Arduino IDE
BAUD_RATE = 9600
SERIAL_TIMEOUT_S = 1.0

PAN_MIN_DEG = 0
PAN_MAX_DEG = 180
TILT_MIN_DEG = 0
TILT_MAX_DEG = 180

PAN_CENTER_DEG = 90
TILT_CENTER_DEG = 90

# ---------------------------------------------------------------------------
# Control loop (Milestone 4)
# ---------------------------------------------------------------------------
CONTROL_GAIN = 0.05          # pixel offset -> degrees; tune per oscillation/lag
DEADZONE_PX = 10              # ignore offsets smaller than this, stops jitter
MAX_STEP_DEG = 5               # per-loop servo slew limit, prevents slamming

# ---------------------------------------------------------------------------
# Prediction (Milestone 5)
# ---------------------------------------------------------------------------
USE_PREDICTION = False        # toggle without touching main.py
PREDICTION_HISTORY_LEN = 5    # number of recent positions kept for velocity estimate
PREDICTION_FRAMES = 3         # how many frames ahead to extrapolate

# ---------------------------------------------------------------------------
# Telemetry (Milestone 4)
# ---------------------------------------------------------------------------
LOG_DIR = "logs"
