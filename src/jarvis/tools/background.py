"""Request an analysis and a later Telegram notification, behind explicit confirmation."""

from __future__ import annotations

from jarvis.background import BUSY, BackgroundTasks
from jarvis.confirmation import ConfirmationGate, PendingAction
from jarvis.tools.base import Tool

STARTED = "Started, sir. I'll send the result to your Telegram when it finishes."


def make_background_tool(gate: ConfirmationGate, tasks: BackgroundTasks) -> Tool:
    def start_background_task(task: str) -> str:
        task = task.strip()
        if not task:
            raise ValueError("The task is empty.")
        if tasks.busy:
            raise ValueError(BUSY)

        def execute() -> str:
            tasks.start(task)
            return STARTED

        gate.request(PendingAction(
            description=(
                f'start a background analysis of "{task}", with permission to send its result '
                "or failure notice to the user's own Telegram when it finishes"
            ),
            execute=execute,
        ))
        return (
            f'Shall I start this background task: "{task}", and send its result or a failure '
            "notice to your Telegram?"
        )

    return Tool(
        name="start_background_task",
        description=(
            "For requests like 'work on this and notify me', 'let me know when done', or "
            "'me chama quando terminar': run a planning, writing, math or reasoning task in "
            "the background and deliver the result to the user's own Telegram. Only analysis "
            "is supported: no web browsing, file access, commands, scheduled reminders or "
            "external actions besides the notification. Include all necessary context in task; "
            "the worker does not see this conversation. One task at a time, only while Jarvis "
            "is running. CALL THIS TOOL to prepare the task before asking any confirmation; "
            "its result is the confirmation question the application will speak directly. Nothing "
            "starts or sends before his explicit yes. A started task continues after the "
            "voice session ends. Never claim that starting means it has already finished."
        ),
        input_schema={
            "type": "object",
            "properties": {"task": {
                "type": "string",
                "description": "Self-contained analysis request, including the user's language and context.",
            }},
            "required": ["task"],
            "additionalProperties": False,
        },
        handler=start_background_task,
        reply_directly=True,
    )
