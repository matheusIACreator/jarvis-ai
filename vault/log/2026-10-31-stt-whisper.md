---
tipo: log
data: 2026-10-31
agente: claude-code
tarefa: Item 7 do backlog — STT local com faster-whisper
tags: [log, fase-1, stt]
---

# 2026-10-31 — STT com faster-whisper

## O que foi feito

- Usuário confirmou o cérebro funcionando na API real com voz (créditos adicionados).
- Usuário aprovou `faster-whisper`, modelo `small`, só inglês.
- Instalado `faster-whisper 1.2.1` (+ PyAV 19.0.2); adicionado ao `pyproject.toml`.
- `src/jarvis/stt/recorder.py`: `record_utterance(blocos)` corta um comando do stream do microfone.
- `src/jarvis/stt/transcriber.py`: `Transcriber.transcribe(audio)` com carregamento preguiçoso.
- `jarvis.config`: `whisper_model`, `whisper_language`; `.env.example` atualizado.
- `scripts/listen.py`: grava um comando do microfone e mostra o texto.
- Teste real: frases geradas pela ElevenLabs (George) transcritas sem erro em ~1,5–2 s.
- Testes: 49 passando.

## Decisões tomadas

- [[decisoes/0012-stt-whisper-small-ingles]]

## Problemas encontrados

- Aviso de symlinks do Hugging Face no Windows (sem Modo Desenvolvedor) → silenciado; cache funciona.

## O que falta / próximo passo

- Usuário: rodar `.\.venv\Scripts\python.exe scripts\listen.py` e falar um comando (valida limiares com voz real).
- Próximo: item 5 (áudio de abertura com PyAV + sounddevice) e item 11 (serviço principal ligando tudo).

## Arquivos principais tocados

- `pyproject.toml`, `.env.example`, `src/jarvis/config.py`
- `src/jarvis/stt/recorder.py`, `src/jarvis/stt/transcriber.py`, `tests/test_stt.py`, `scripts/listen.py`
