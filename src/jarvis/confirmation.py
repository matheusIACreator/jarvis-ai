"""Explicit user confirmation before any outbound action.

Tools never act on the outside world directly. They hand a `PendingAction` to the
`ConfirmationGate`, and the model reads it back to the user. Whether the user said yes is
decided here, by code, from the user's own words; the model cannot confirm on his behalf.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass

CANCELLED = "Cancelled, sir. Nothing was sent."
FAILED = "I'm afraid that didn't go through, sir."

# The whole reply must be one of these (after normalizing), so "yes, but change it" never sends.
YES = {
    "yes", "yeah", "yep", "yup", "sure", "confirm", "confirmed", "affirmative", "correct",
    "do it", "send it", "go ahead", "please do", "yes please", "yes send it", "yes do it",
    "yes go ahead", "yes jarvis", "yes sir", "that's right", "sounds good", "ok send it",
    "okay send it",
}
NO_STARTS = ("no", "nope", "don't", "do not", "cancel", "stop", "never mind", "wait", "hold on")


@dataclass(frozen=True)
class PendingAction:
    description: str  # what will happen, e.g. "send 'Running late' to your Telegram"
    execute: Callable[[], str]  # performs it and returns what Jarvis should say


def _normalize(text: str) -> str:
    text = text.lower().replace("’", "'")
    text = re.sub(r"[^a-z' ]+", " ", text)
    return " ".join(text.split())


def classify(text: str) -> str:
    """Return "yes", "no" or "unclear" for a reply to a confirmation question."""
    normalized = _normalize(text)
    if normalized in YES:
        return "yes"
    if any(normalized == start or normalized.startswith(start + " ") for start in NO_STARTS):
        return "no"
    return "unclear"


class ConfirmationGate:
    def __init__(self) -> None:
        self.pending: PendingAction | None = None

    def request(self, action: PendingAction) -> str:
        """Hold `action` until the user answers. Returns the tool result for the model."""
        self.pending = action
        return (
            f"NOT DONE YET. Pending: {action.description}. Read it back to the user in one short "
            "sentence and ask him to confirm. It happens only if he says yes; do not claim it is done."
        )

    def resolve(self, text: str) -> str | None:
        """Handle the user's answer to a pending action.

        Returns what to say when the answer settles it (done or cancelled), or None when there
        is nothing pending or the answer was unclear; an unclear answer cancels the action and
        the words go on to the brain as a normal request.
        """
        action, self.pending = self.pending, None
        if action is None:
            return None
        answer = classify(text)
        if answer == "yes":
            try:
                return action.execute()
            except Exception:
                return FAILED
        if answer == "no":
            return CANCELLED
        return None

    def cancel(self) -> None:
        self.pending = None
