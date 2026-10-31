"""One confirmed analysis at a time, independent of the voice session.

The caller supplies a read-only worker and a notifier already bound to the user's chat.
Nothing starts until the confirmation gate invokes ``start``.
"""

from __future__ import annotations

import threading
from collections.abc import Callable

FAILED = "I'm afraid your background task failed, sir. Please ask me to try again."
BUSY = "A background task is already running. Wait for it to finish before starting another."
# At most 4000 UTF-16 code units, even if every character is an emoji.
MESSAGE_CHARS = 2000


class BackgroundTasks:
    def __init__(
        self,
        work: Callable[[str], str],
        notify: Callable[[str], None],
        log: Callable[[str], None] = print,
    ) -> None:
        self.work = work
        self.notify = notify
        self.log = log
        self._lock = threading.Lock()
        self._stopped = threading.Event()
        self._thread: threading.Thread | None = None

    @property
    def busy(self) -> bool:
        with self._lock:
            return self._thread is not None and self._thread.is_alive()

    def start(self, task: str) -> None:
        task = task.strip()
        if not task:
            raise ValueError("The task is empty.")
        with self._lock:
            if self._stopped.is_set():
                raise RuntimeError("Background tasks have been stopped.")
            if self._thread is not None and self._thread.is_alive():
                raise ValueError(BUSY)
            self._thread = threading.Thread(
                target=self._run, args=(task,), name="background-task", daemon=True
            )
            self._thread.start()

    def _run(self, task: str) -> None:
        label = task if len(task) <= 300 else task[:297] + "..."
        try:
            result = self.work(task).strip()
            if not result:
                raise ValueError("The analysis returned no result.")
            message = f"Background task finished.\n\nTask: {label}\n\n{result}"
        except Exception as exc:
            # Exception text can contain credentials or request contents.
            self.log(f"(Background task failed: {type(exc).__name__})")
            message = f"{FAILED}\n\nTask: {label}"
        try:
            for start in range(0, len(message), MESSAGE_CHARS):
                if self._stopped.is_set():
                    return
                self.notify(message[start:start + MESSAGE_CHARS])
        except Exception as exc:
            # Do not retry automatically: a timeout may mean Telegram accepted the message.
            self.log(f"(Background notification failed: {type(exc).__name__}; not retried)")

    def wait(self, timeout: float | None = None) -> bool:
        """Wait for the current task, returning whether it finished within the timeout."""
        with self._lock:
            thread = self._thread
        if thread is not None:
            thread.join(timeout)
        return thread is None or not thread.is_alive()

    def stop(self) -> None:
        """Reject new tasks and suppress remaining notifications; in-flight calls may finish."""
        self._stopped.set()
