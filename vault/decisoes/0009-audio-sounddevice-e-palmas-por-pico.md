---
tipo: decisao
numero: 0009
titulo: Áudio com sounddevice e palmas detectadas por pico
status: aceita
data: 2026-10-30
agente: claude-code
tags: [decisao, audio, gatilho, fase-1]
---

# 0009 — Áudio com sounddevice e palmas detectadas por pico

## Contexto

- O gatilho precisa de captura contínua do microfone e detecção de palmas duplas leve, sem modelo de ML.

## Decisão

- Captura com `sounddevice` (aprovado pelo usuário em 2026-10-30): mono float32, 16 kHz, blocos de 32 ms.
  16 kHz é o que o faster-whisper usa, então o mesmo stream serve para o STT.
- Detecção por regras: pico do bloco contra um piso de ruído adaptativo, duração máxima de 120 ms,
  intervalo entre palmas de 0,12–0,8 s, cooldown de 1,5 s. Parâmetros em `ClapSettings`.

## Alternativas consideradas

- **PyAudio** — API de nível mais baixo, devolve bytes crus.
- **RMS do bloco como medida** — testado e descartado: dilui a palma (poucos ms) em 32 ms de ruído.
- **Modelo de classificação de som** — pesado demais para um gatilho simples.

## Consequências

- Sem modelo, CPU quase zero, totalmente testável com sinais sintéticos.
- Limiares precisam de ajuste com palmas reais no microfone do notebook (`scripts/clap_monitor.py`).
- Sons secos e curtos (bater na mesa duas vezes) também disparam; aceitável na v1.

## Status

- aceita

## Data

- 2026-10-30
