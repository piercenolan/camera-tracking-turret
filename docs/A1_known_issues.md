# Known issues — audit of Milestones 0–3

Audited 2026-11-15: `src/` (camera, tracker, serial_link, config), `turret_listener.ino`, and the
four `tools/` scripts. In M0–3 the camera and servos were tested separately and never integrated.

Severity: **High** = wrong behavior, unsafe motion, or blocks a milestone. **Medium** = violates a
PRD requirement or will cause a bug later. **Low** = cleanup or minor accuracy.

Grouped by the milestone that fixes each issue, in work order. Check off with `[x]` when fixed.
Issue numbers are stable IDs.

## A1 — fix now
- [x] **#15** (Low) Docstrings reference `tools/test_*.py`; the files are `try_*.py`.
- [x] **#17** (Low) FPS in `try_camera.py` is loop rate, not camera rate. Relabeled "Loop FPS".

## A2 — tracker
- [ ] **#3** (High) HSV range 9–127 spans orange to blue. Target is changing (lemon unavailable
  and not a COCO class); retune for the new one.
- [ ] **#5** (Medium) Tracker reads HSV bounds from config at call time instead of taking them as
  inputs (X4).
- [ ] **#6** (Medium) No support for hue ranges that wrap 179→0 (red targets).
- [ ] **#12a** (Low) Centroid `int()` truncates, losing sub-pixel precision.
- [ ] **#18** (Low) `m00 == 0` guard in the tracker is unreachable while `MIN_CONTOUR_AREA > 0`.

## A3 — control
- [ ] **#7** (Medium) Camera never checks the resolution it actually got; `cap.set()` fails
  silently. — *Control is first to actually use center.*
- [ ] **#12b** (Low) Angle `int()` truncates instead of rounding, biasing angles toward zero.

## A4 — predictor
- [ ] **#9** (Medium) Prediction lead is in frames (`PREDICTION_FRAMES`); PRD requires seconds.

## A5 — pipeline step
- [ ] **#8** (Medium) Frames carry no timestamp, but the pipeline needs time as an input (X2/X3).
  — *A5 defines the step function.*

## A7 — firmware core
- [ ] **#1** (High) Firmware serial parser is commented out; a pan sweep runs instead, so nothing
  reads serial. The old parser uses `String` and blocking `readStringUntil`, so it is replaced,
  not revived. — *Parser rewrite is A7's main job.*
- [ ] **#2a** (High) Firmware limits are impossible: `Servo.write()` clamps to 180, so tilt
  125–360 / startup 220 really means 125–180 with startup at the endpoint. Pan sweep ignores its
  15° minimum. — *A7: hard limits on device.*
- [ ] **#10** (Medium) Baud is 9600; protocol target is 115200. At 9600 the ack echo alone costs
  ~10 ms per command. — *Baud rate is part of A7 spec.*
- [ ] **#11** (Medium) Firmware uses plain `int` (16-bit on Uno, 32-bit on laptop) instead of
  fixed-width types. — *A7 requires fixed-width ints.*
- [ ] **#16** (Low) `.ino` header comment claims it parses `pan,tilt` and clamps 0–180; neither is
  true. — *File rewritten in A7.*

## A8 — host protocol
- [ ] **#2b** (High) Firmware limits disagree with `config.py` (X5). — *A8 meets X5.*
- [ ] **#4** (High) `send_angles()` returns `True` once bytes reach the OS buffer, not when the
  board receives or applies them. — *A8 is where the host builds frames.*

## Phase C — hardware
- [ ] **#14** (Low) Dropped-frame limit is a count, not a time; fast failures could trip
  `CameraDisconnected` on a brief hiccup (unverified). — *Can't be verified without the USB cam.*

## Won't fix
- **#13** (Low) `try_serial.py` reads one reply per command with a 1 s blocking read; any extra
  board output desyncs replies. — *Archive `try_serial.py` in A8.*
