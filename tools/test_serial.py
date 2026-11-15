"""Manual test: type pan,tilt angle pairs, watch the servos move. No vision.
Close the Arduino IDE's Serial Monitor before running this. Type 'q' to quit."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.serial_link import SerialLink


def main():
    with SerialLink() as link:
        print(f"Connected on {link.port} @ {link.baud_rate} baud.")
        print("Type angles as 'pan,tilt' (e.g. 90,90). Type 'q' to quit.\n")

        while True:
            raw = input("> ").strip()
            if raw.lower() == "q":
                break

            parts = raw.split(",")
            if len(parts) != 2:
                print("Expected format: pan,tilt (e.g. 90,90)")
                continue

            try:
                pan, tilt = int(parts[0]), int(parts[1])
            except ValueError:
                print("Both values must be integers.")
                continue

            if not link.send_angles(pan, tilt):
                print("Write failed -- check the connection.")
                continue

            reply = link.read_line()
            print(f"Arduino: {reply}" if reply else "(no reply)")


if __name__ == "__main__":
    main()
