---
tipo: log
data: 2026-10-30
agente: claude-code
tarefa: Voz do Jarvis com ElevenLabs (item 10 adiantado)
tags: [log, fase-1, tts, elevenlabs]
---

# 2026-10-30 — Voz com ElevenLabs

## O que foi feito

- Rodado `npx -y @elevenlabs/cli@latest onboard init`: login, chave nova (final 3cac) gravada no `.env`.
- Lida a skill `text-to-speech` da ElevenLabs (baixada em pasta temporária, fora do projeto).
- Instalado `elevenlabs 2.75.0`; adicionado ao `pyproject.toml`.
- `src/jarvis/tts/speaker.py`: `Speaker.speak(texto)` com `eleven_flash_v2_5`, PCM 24 kHz, tocado por `sounddevice`.
- `jarvis.config`: `ELEVENLABS_VOICE_ID` opcional (padrão Daniel, britânico); parâmetro `required=`.
- `scripts/say.py`: fala uma frase para teste manual.
- Testes: 28 passando. Confirmado que o `jarvis.config` carrega a chave do `.env` (sem exibir).

## Decisões tomadas

- [[decisoes/0010-voz-daniel-e-streaming-http]]

## Problemas encontrados

- `onboard check` pede `python-dotenv`; falso positivo, mantido o `jarvis.config` ([[decisoes/0008-config-sem-dependencia]]).
- `tar` falhou ao extrair a pasta `evals/` das skills (caminho inválido no Windows); irrelevante.
- **Ainda não foi tocada voz real**: a CLI exige o "sim" do usuário antes do teste.

## O que falta / próximo passo

- Usuário: autorizar e ouvir `.\.venv\Scripts\python.exe scripts\say.py`.
- Migrar para WebSocket quando o cérebro gerar texto em streaming.
- Seguir o [[backlog]]: item 5 (áudio de abertura) precisa de aprovação de biblioteca de mp3.

## Arquivos principais tocados

- `pyproject.toml`, `.env.example`, `src/jarvis/config.py`, `src/jarvis/tts/speaker.py`
- `tests/test_config.py`, `tests/test_speaker.py`, `scripts/say.py`
