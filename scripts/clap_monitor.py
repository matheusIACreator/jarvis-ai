"""Live check of the double-clap detector on the real microphone.

Run from the repo root:  .\\.venv\\Scripts\\python.exe scripts\\clap_monitor.py
Prints the loudest peak and the noise floor every second, and a line on every double clap.
Stop with Ctrl+C.
"""

import numpy as np

from jarvis.trigger.clap import ClapDetector
from jarvis.trigger.microphone import MicrophoneStream


def main() -> None:
    detector = ClapDetector()
    blocks_per_second = detector.settings.sample_rate // 512
    peak, count = 0.0, 0
    print("Listening. Clap twice. Ctrl+C to stop.")
    with MicrophoneStream() as mic:
        for block in mic:
            peak = max(peak, float(np.max(np.abs(block))))
            if detector.process(block):
                print(f"{detector.now:8.2f}s  >>> DOUBLE CLAP <<<")
            count += 1
            if count >= blocks_per_second:
                print(f"{detector.now:8.2f}s  peak={peak:.3f}  noise_floor={detector.noise_floor:.4f}")
                peak, count = 0.0, 0


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
