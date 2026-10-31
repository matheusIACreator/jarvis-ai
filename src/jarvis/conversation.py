"""What Jarvis says around a session, and the listen -> think -> speak loop.

Kept free of audio and API code: the loop gets plain callables, so it is testable with fakes.
"""

from __future__ import annotations

import re
import threading
from collections.abc import Callable
from dataclasses import dataclass

FAREWELL = "Very good, sir. I'll be here if you need me."
FILLER = "One moment, sir."
FILLER_DELAY = 2.0  # seconds of silence before the filler plays

# Phrases that end the session wherever they appear ("thanks, that's all").
DISMISSAL_PHRASES = (
    "that's all",
    "that is all",
    "that will be all",
    "that'll be all",
    "goodbye",
    "good bye",
    "never mind",
    "go to sleep",
    "stand by",
    "no thanks",
    "no thank you",
    "nothing else",
)
# Single words that end the session only when said on their own.
DISMISSAL_WORDS = ("bye", "nothing", "no", "thanks", "dismissed")


def greeting_for(hour: int) -> str:
    if 5 <= hour < 12:
        part = "morning"
    elif 12 <= hour < 18:
        part = "afternoon"
    else:
        part = "evening"
    return f"Good {part}, sir. How may I help?"


def _normalize(text: str) -> str:
    text = text.lower().replace("’", "'")
    text = re.sub(r"[^a-z' ]+", " ", text)
    return " ".join(text.split())


def is_dismissal(text: str) -> bool:
    normalized = _normalize(text)
    if normalized in DISMISSAL_WORDS:
        return True
    padded = f" {normalized} "
    return any(f" {phrase} " in padded for phrase in DISMISSAL_PHRASES)


def with_filler(
    think: Callable[[str], str], play_filler: Callable[[], None], delay: float = FILLER_DELAY
) -> Callable[[str], str]:
    """Wrap `think` so a filler line plays if the answer takes longer than `delay`.

    The filler always finishes before the answer is returned, so the two never overlap.
    """

    def thinking_out_loud(text: str) -> str:
        done = threading.Event()

        def filler_if_slow() -> None:
            if not done.wait(delay):
                play_filler()

        filler = threading.Thread(target=filler_if_slow, daemon=True)
        filler.start()
        try:
            return think(text)
        finally:
            done.set()
            filler.join()

    return thinking_out_loud


@dataclass
class Conversation:
    listen: Callable[[], str]  # returns "" when nothing was said
    think: Callable[[str], str]
    say: Callable[[str], None]
    on_heard: Callable[[str], None] = lambda text: None
    finished: Callable[[], bool] = lambda: False  # e.g. the model called end_conversation

    def run(self) -> int:
        """Keep answering follow-ups until silence or a dismissal. Returns answered turns."""
        turns = 0
        while True:
            text = self.listen().strip()
            if not text:
                return turns
            self.on_heard(text)
            if is_dismissal(text):
                self.say(FAREWELL)
                return turns
            reply = self.think(text)
            if reply:
                self.say(reply)
            turns += 1
            if self.finished():
                return turns
