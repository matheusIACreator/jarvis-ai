# Jarvis

A personal voice assistant (Iron Man style) for a single user, running natively on Windows 11.

> Status: voice MVP working, with Telegram chat, confirmed messages and background analysis notifications. Email and phone come later.

## Flow

1. A double hand-clap (or the wake word "Hey Jarvis") is detected from the laptop microphone.
2. A local startup track plays, then Jarvis greets the user.
3. The spoken command is transcribed locally (faster-whisper).
4. The Anthropic API (Haiku by default, Sonnet on demand) decides the reply and calls tools.
5. The reply is spoken back via ElevenLabs streaming TTS.
6. Notifications go out through a Telegram bot. Email and phone calls come later, always behind explicit user confirmation.

## Setup (PowerShell)

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env   # then fill in real values locally
pytest
```

Put your startup music at `assets/audio/startup.mp3` (never committed). Without it, Jarvis just greets.

If startup fails with `DLL load failed while importing bitstream` and an Application Control
policy block, the Windows event log can identify the blocked PyAV binary (CodeIntegrity,
event 3077). This laptop blocked PyAV 19.0.2; the project pins the tested Windows wheel to
18.0.0. Repair an existing environment with:

```powershell
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: "av==18.0.0"
.\.venv\Scripts\python.exe -c "import av; from faster_whisper import WhisperModel; print(av.__version__)"
```

This keeps Windows security policies enabled. If a policy still blocks a binary, check the
exact file in the event log; this version pin is a tested fix for this laptop, not a general
allow rule for Application Control.

## Run

```powershell
.\.venv\Scripts\python.exe -m jarvis
```

Clap twice (or say "Hey Jarvis"), wait for the greeting, then speak. After activation the
session stays open through pauses: just speak again, with no new clap, wake word, music or
greeting. Say "that's all", "goodbye" or "go to sleep" to return to waiting for activation.
"Okay, I'll wait" keeps the session open. Ctrl+C stops the entire service, including background
work that has not finished; keep it running while waiting for a notification.

Optional `SESSION_IDLE_SECONDS=90` in `.env` returns to waiting for activation after 90 seconds
without a command. The default is `0` (no idle limit). Silence itself does not trigger Whisper
transcription or an Anthropic request. Unrecognized speech/noise does not end the session.

With `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` set, you can say "send me a Telegram message
saying ...". Jarvis reads it back and sends it only after you answer with a plain "yes".
The question comes directly from the tool after it registers the pending action. Confirmation
expires after 60 seconds even if the voice session stays open; ask for the action again if it
expires. Replies that change the action, such as "yes, but change it", do not authorize it.
You can also message the bot: Jarvis answers your own chat (and only yours) while the service runs.

For a longer analysis, say "Plan a week of Python study and notify me on Telegram when you're
done." Jarvis reads back the task and asks permission to start it and send the result. Answer
"yes" (or "yes, start it and send the result") to begin. You can stay silent, end the voice
session explicitly, or ask other questions while it works. The result
(or a failure notice) goes to your own Telegram chat without another confirmation.

Background tasks currently start through voice only and support planning, writing, math and
reasoning with the advisor. They have no web, file or command access. Only one runs at a time;
keep Jarvis running until it finishes. Tasks are not saved or resumed after shutdown. Long
results arrive in consecutive messages. If delivery fails, Jarvis logs the error and does not
retry automatically, to avoid duplicate notifications.

Manual test tools in `scripts/`:

| Script | What it does |
|---|---|
| `clap_monitor.py` | Live clap detector levels |
| `play_intro.py` | Play the startup music as Jarvis will (`STARTUP_AUDIO_START`, `STARTUP_AUDIO_SECONDS`) |
| `listen.py` | Record one command and print the transcription |
| `chat.py [--speak]` | Type to the brain, optionally hear the replies |
| `say.py "text"` | Speak a line with the configured voice |
| `telegram_chat.py [minutes]` | Run only the Telegram chat channel |

## Shared agent memory

Two coding agents (Claude Code and Codex) work on this repo. They share memory through an
Obsidian-compatible vault in `vault/` (plain Markdown, versioned with git, written in pt-BR).
Each session starts by reading `vault/00-Indice.md` and the latest log, and ends by writing a
new log, updating the index and backlog, and recording decisions. See `AGENTS.md` for the full rules.

During a session the active agent keeps `vault/em-andamento.md` up to date, so if it runs out of
tokens the other agent can continue. To run a task with automatic fallback from Claude Code to Codex:

```powershell
.\scripts\agent.ps1 "Do backlog item 1"
```

## Local dashboard and conversation memory

The Next.js/React frontend in `frontend/` was initialized using `npx shadcn@latest init --template next --name frontend --defaults --no-monorepo`. Node.js 20.9+ is required (developed with Node 24).

Run the voice service in one PowerShell terminal:

```powershell
.venv/Scripts/python.exe -m jarvis
```

Run the dashboard in another:

```powershell
npm --prefix frontend ci
npm --prefix frontend run dev
```

Open http://127.0.0.1:3000. The Python bridge binds to 127.0.0.1:8765; Next.js proxies requests on the server. Both must run on the same computer. If the bridge is unavailable, the panel shows offline. The reactor pulses during voice playback (state-driven, not audio-amplitude analysis). Voice activation still uses the native microphone, double clap or wake word. Web chat is text-only and has clock and memory tools, without outbound-action tools.

Voice, Telegram and web exchanges are saved as quoted Markdown in `vault/conversas/`, excluded from Git. Open `vault/` in Obsidian and use `Memória.md` or `Conversas.base`. The brain can search earlier exchanges via `search_memory`; no embeddings, cloud memory service or Obsidian application is required. Existing conversations before this change cannot be recovered. Delete unwanted note files in Obsidian to remove them from future retrieval. Credential-like exchanges are skipped by a conservative keyword filter; never dictate secrets. Raw conversation text retains its original language.

The upstream [Obsidian skills](https://github.com/kepano/obsidian-skills) are in `.claude/skills/`, shared with Codex via `AGENTS.md`. They guide development; runtime recall is implemented by Python, not by executing skills.

Validation:

```powershell
.venv/Scripts/python.exe -m pytest -q
npm --prefix frontend run build
```
