# Jarvis

A personal voice assistant (Iron Man style) for a single user, running natively on Windows 11.

> Status: skeleton only. No features implemented yet.

## Planned flow

1. A double hand-clap is detected from the laptop microphone.
2. A local startup track plays, then Jarvis greets the user.
3. The spoken command is transcribed locally (faster-whisper).
4. The Anthropic API (Haiku by default, Sonnet on demand) decides the reply and calls tools.
5. The reply is spoken back via ElevenLabs streaming TTS.
6. Notifications go out through a Telegram bot. Email and phone calls come later, always behind explicit user confirmation.

## Setup (PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
Copy-Item .env.example .env   # then fill in real values locally
```

## Shared agent memory

Two coding agents (Claude Code and Codex) work on this repo. They share memory through an
Obsidian-compatible vault in `vault/` (plain Markdown, versioned with git, written in pt-BR).
Each session starts by reading `vault/00-Indice.md` and the latest log, and ends by writing a
new log, updating the index and backlog, and recording decisions. See `AGENTS.md` for the full rules.
