---
tipo: log
data: 2026-10-31
agente: claude-code
tarefa: Música de abertura começando no 6º segundo
tags: [log, fase-1, audio]
---

# 2026-10-31 — Início da música de abertura

## O que foi feito

- Usuário adicionou "Back in Black" (AC/DC); arquivo renomeado para `assets/audio/startup.mp3` (fora do git).
- Nova configuração `STARTUP_AUDIO_START` (segundos pulados) com fade-in de 50 ms; `.env` do usuário com `STARTUP_AUDIO_START=6`.
- `scripts/play_intro.py`: toca a abertura exatamente como o Jarvis tocará. Tocado com sucesso.
- Testes: 76 passando.

## Decisões tomadas

- [[decisoes/0013-fluxo-da-sessao-de-voz]] atualizada (início da música).

## Problemas encontrados

- Nome original do arquivo não batia com `STARTUP_AUDIO_PATH` → renomeado.

## O que falta / próximo passo

- Usuário: testar `python -m jarvis` com palmas reais.

## Arquivos principais tocados

- `src/jarvis/tts/audio_file.py`, `src/jarvis/config.py`, `src/jarvis/app.py`, `.env.example`, `README.md`
- `tests/test_audio_file.py`, `scripts/play_intro.py`
