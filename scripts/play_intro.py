"""Play the startup music exactly as Jarvis will (same start offset, length and fade).

Run from the repo root:  .\\.venv\\Scripts\\python.exe scripts\\play_intro.py
"""

from jarvis.config import load_config
from jarvis.tts.audio_file import FilePlayer


def main() -> None:
    config = load_config(required=())
    player = FilePlayer(
        config.startup_audio_path, config.startup_audio_seconds, config.startup_audio_start
    )
    length = "whole file" if config.startup_audio_seconds is None else f"{config.startup_audio_seconds:g} s"
    print(f"{config.startup_audio_path.name}: from {config.startup_audio_start:g} s, {length}")
    if not player.start():
        print("File not found.")
        return
    player.wait()


if __name__ == "__main__":
    main()
