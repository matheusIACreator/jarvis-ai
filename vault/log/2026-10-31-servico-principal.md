---
tipo: log
data: 2026-10-31
agente: claude-code
tarefa: Itens 5, 6 e 11 — áudio de abertura, saudação e serviço principal
tags: [log, fase-1, servico, audio]
---

# 2026-10-31 — Serviço principal

## O que foi feito

- Usuário validou o STT com a própria voz ("Tell me what day it is.", 1,8 s).
- `src/jarvis/tts/audio_file.py`: `decode` (PyAV → estéreo 44,1 kHz), `trim_with_fade`, `FilePlayer`.
  Testado com mp3 e wav gerados localmente.
- `Speaker.synthesize` / `Speaker.play`; `MicrophoneStream.drain`.
- `src/jarvis/conversation.py`: `greeting_for`, `is_dismissal`, `Conversation` (ouvir → pensar → falar).
- `src/jarvis/app.py` + `__main__.py`: serviço completo em `python -m jarvis`.
- `jarvis.config`: `STARTUP_AUDIO_SECONDS` (padrão 10; 0 = inteiro).
- README com instruções de execução e scripts de teste.
- Teste de fumaça: serviço sobe, carrega o Whisper, avisa da falta da música e espera palmas.
- Testes: 74 passando.

## Decisões tomadas

- [[decisoes/0013-fluxo-da-sessao-de-voz]]

## Problemas encontrados

- `assets/audio/startup.mp3` ainda não existe (usuário precisa colocar a música).
- Fluxo completo com palmas reais ainda não testado (depende do usuário).

## O que falta / próximo passo

- Usuário: colocar a música, rodar `.\.venv\Scripts\python.exe -m jarvis`, bater palmas, conversar.
- Se as palmas não dispararem: `scripts\clap_monitor.py` para ajustar `ClapSettings` (item 4b).
- Depois: item 12 (escalonar para Sonnet) ou Fase 2 (Telegram).

## Arquivos principais tocados

- `src/jarvis/app.py`, `src/jarvis/__main__.py`, `src/jarvis/conversation.py`, `src/jarvis/tts/audio_file.py`
- `src/jarvis/tts/speaker.py`, `src/jarvis/trigger/microphone.py`, `src/jarvis/config.py`, `.env.example`, `README.md`
- `tests/test_conversation.py`, `tests/test_audio_file.py`
