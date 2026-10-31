"""Explicit user confirmation before any outbound action.

Tools never act on the outside world directly. They hand a `PendingAction` to the
`ConfirmationGate`, and the model reads it back to the user. Whether the user said yes is
decided here, by code, from the user's own words; the model cannot confirm on his behalf.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from time import monotonic

CANCELLED = "Cancelled, sir. Nothing was sent."
FAILED = "I'm afraid that didn't go through, sir."
EXPIRED = "That confirmation has expired, sir. Please ask me again; nothing was started or sent."

# The whole reply must be one of these (after normalizing), so "yes, but change it" never sends.
YES = {
    "yes", "yeah", "yep", "yup", "sure", "confirm", "confirmed", "affirmative", "correct",
    "do it", "send it", "go ahead", "please do", "yes please", "yes send it", "yes do it",
    "yes go ahead", "yes jarvis", "yes sir", "that's right", "sounds good", "ok send it",
    "okay send it",
    "start it", "yes start it", "start it and send the result",
    "yes start it and send the result", "yes please start it and send the result",
    "sim", "pode iniciar", "sim pode iniciar", "sim pode iniciar e enviar o resultado",
}
NO_STARTS = ("no", "nope", "don't", "do not", "cancel", "stop", "never mind", "wait", "hold on")


@dataclass(frozen=True)
class Resolution:
    reply: str  # what Jarvis says out loud
    record: str  # authoritative note for the model's history: what actually happened


@dataclass(frozen=True)
class PendingAction:
    description: str  # what will happen, e.g. "send 'Running late' to the user's Telegram"
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
    def __init__(self, timeout: float = 60.0, clock: Callable[[], float] = monotonic) -> None:
        self.pending: PendingAction | None = None
        self.timeout = timeout
        self.clock = clock
        self._requested_at = 0.0

    def request(self, action: PendingAction) -> str:
        """Hold `action` until the user answers. Returns the tool result for the model."""
        if self.pending is not None and self.clock() - self._requested_at < self.timeout:
            raise ValueError("An action is already waiting for confirmation. Settle it first.")
        self.pending = action
        self._requested_at = self.clock()
        return (
            f"NOT DONE YET. Pending: {action.description}. Read it back to the user in one short "
            "sentence and ask him to confirm. It happens only if he says yes; do not claim it is done."
        )

    def resolve(self, text: str) -> Resolution | None:
        """Handle the user's answer to a pending action.

        Returns what to say and what to record when the answer settles it (done or
        cancelled), or None when there is nothing pending or the answer was unclear; an
        unclear answer cancels the action and the words go on to the brain as a new request.
        """
        action, self.pending = self.pending, None
        if action is None:
            return None
        if self.clock() - self._requested_at >= self.timeout:
            return Resolution(EXPIRED, f"Confirmation expired; this was not done: {action.description}.")
        answer = classify(text)
        if answer == "yes":
            try:
                reply = action.execute()
            except Exception as exc:
                return Resolution(
                    FAILED,
                    f"The user confirmed, but it failed ({type(exc).__name__}): "
                    f"{action.description}. Nothing was delivered.",
                )
            return Resolution(
                reply,
                f"The user confirmed and Jarvis's code carried it out: {action.description}. "
                "It succeeded; it is done and must not be repeated unless he asks again.",
            )
        if answer == "no":
            return Resolution(
                CANCELLED, f"The user declined, so this was not done: {action.description}."
            )
        return None

    def cancel(self) -> None:
        self.pending = None
