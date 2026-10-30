---
tipo: decisao
numero: "0002"
titulo: Voz com ElevenLabs Flash e STT local
status: aceita
data: 2026-10-30
agente: claude-code
tags: [decisao, voz, tts, stt, elevenlabs]
---

# 0002 — Voz com ElevenLabs Flash e STT local

## Contexto

- A voz é a interface principal; a latência até a primeira palavra falada define a sensação de "Jarvis".
- A transcrição precisa ser confiável em português e não deve custar por uso.

## Decisão

- Saída de voz: ElevenLabs, modelo `eleven_flash_v2_5`, por streaming via WebSocket.
- Respostas faladas curtas.
- Voz configurável por `ELEVENLABS_VOICE_ID` no `.env`.
- Entrada de voz (STT): faster-whisper, rodando localmente.

## Alternativas consideradas

- **ElevenLabs multilingual (modelos de maior qualidade)** — mais naturais, porém com mais latência.
- **TTS do Windows (SAPI) / TTS local** — sem custo, mas voz pouco convincente.
- **STT em nuvem** — bom, mas adiciona custo, latência de rede e envia áudio para fora.

## Consequências

- Streaming permite começar a falar antes de a resposta inteira ser gerada.
- Custo da ElevenLabs proporcional aos caracteres: mais um motivo para respostas curtas.
- faster-whisper consome CPU/GPU local; o tamanho do modelo precisará ser ajustado ao notebook.

## Status

- aceita

## Data

- 2026-10-30
