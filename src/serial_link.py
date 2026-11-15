"""Serial connection to the Arduino. See tools/test_serial.py for the manual test."""

import time

import serial

from src import config

# The Uno resets when a new serial connection opens (DTR toggle), so commands
# sent immediately after open() would be dropped while it reboots.
BOOT_SETTLE_S = 2.0


class SerialLink:
    """Thin wrapper around pyserial with clean open/close semantics."""

    def __init__(self, port=None, baud_rate=None, timeout=None):
        self.port = config.SERIAL_PORT if port is None else port
        self.baud_rate = config.BAUD_RATE if baud_rate is None else baud_rate
        self.timeout = config.SERIAL_TIMEOUT_S if timeout is None else timeout
        self._ser = None

    def open(self):
        try:
            self._ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
        except serial.SerialException as e:
            raise RuntimeError(
                f"Could not open serial port {self.port}. Check the port name in "
                "config.py, and that no other program (e.g. the Arduino IDE's "
                "Serial Monitor) has it open."
            ) from e

        time.sleep(BOOT_SETTLE_S)
        return self

    def send_angles(self, pan_deg, tilt_deg):
        """Send a clamped pan,tilt angle pair. Returns False (does not raise)
        on write failure, e.g. the Arduino was disconnected mid-run."""
        if self._ser is None:
            raise RuntimeError("Serial link is not open. Call open() first.")

        pan_deg = max(config.PAN_MIN_DEG, min(config.PAN_MAX_DEG, int(pan_deg)))
        tilt_deg = max(config.TILT_MIN_DEG, min(config.TILT_MAX_DEG, int(tilt_deg)))

        line = f"{pan_deg},{tilt_deg}\n"
        try:
            self._ser.write(line.encode("ascii"))
            return True
        except serial.SerialException:
            return False

    def read_line(self):
        """Blocking read of the next line from the Arduino (bounded by
        config.SERIAL_TIMEOUT_S), or None on timeout/disconnect. For manual
        testing only -- the real-time control loop should not block on this."""
        if self._ser is None:
            raise RuntimeError("Serial link is not open. Call open() first.")

        try:
            raw = self._ser.readline()
        except serial.SerialException:
            return None

        if not raw:
            return None
        return raw.decode("ascii", errors="replace").strip()

    def close(self):
        if self._ser is not None:
            self._ser.close()
            self._ser = None

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False
