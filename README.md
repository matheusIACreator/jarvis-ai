# Jarvis

A personal voice assistant (Iron Man style) for a single user, running natively on Windows 11.

> Status: voice MVP working (clap trigger, startup music, greeting, local speech-to-text, Claude, ElevenLabs voice). Telegram, email and phone come later.

## Flow

1. A double hand-clap is detected from the laptop microphone.
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

## Run

```powershell
.\.venv\Scripts\python.exe -m jarvis
```

Clap twice, wait for the greeting, then speak. Ask follow-ups without clapping again; stay silent
or say "that's all" to end the session. Ctrl+C stops the service.

With `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` set, you can say "send me a Telegram message
saying ...". Jarvis reads it back and sends it only after you answer with a plain "yes".

Manual test tools in `scripts/`:

| Script | What it does |
|---|---|
| `clap_monitor.py` | Live clap detector levels |
| `play_intro.py` | Play the startup music as Jarvis will (`STARTUP_AUDIO_START`, `STARTUP_AUDIO_SECONDS`) |
| `listen.py` | Record one command and print the transcription |
| `chat.py [--speak]` | Type to the brain, optionally hear the replies |
| `say.py "text"` | Speak a line with the configured voice |

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
