---
tipo: decisao
numero: 0016
titulo: Palavra de ativação "Hey Jarvis" e palmas mais sensíveis
status: aceita
data: 2026-10-31
agente: claude-code
tags: [decisao, gatilho, fase-1]
---

# 0016 — Palavra de ativação "Hey Jarvis" e palmas mais sensíveis

## Contexto

- Palmas pararam de disparar. Diagnóstico de 60 s: palmas reais com pico 0,12–0,27; mínimo era 0,25.
- Usuário pediu um gatilho falado alternativo.

## Decisão

- Palmas: `min_peak` 0,25 → **0,08** (ruído da sala ~0,003), configurável por `CLAP_MIN_PEAK`.
  O piso de ruído agora também sobe durante som alto contínuo (sala barulhenta não trava o detector).
- Palavra de ativação **"Hey Jarvis"** com `openwakeword` (aprovado pelo usuário), modelo pré-treinado
  `hey_jarvis`, ONNX. Escuta junto com as palmas; o que disparar primeiro acorda o Jarvis.
  Limiar 0,5 por `WAKE_WORD_THRESHOLD` (0 desliga).

## Alternativas consideradas

- **Frase livre via Whisper** ("Ok Jarvis, wake up") — sem dependência nova, mas ~1,5 s de atraso,
  CPU sempre que alguém fala e mais falsos disparos.
- **Treinar modelo próprio** de frase personalizada — trabalhoso; fica para depois se necessário.

## Consequências

- Wake word custa 1,7 ms por quadro de 80 ms (quase zero de CPU).
- Teste com fala sintética (3 vozes): disparou em todos os "Hey Jarvis", em nenhuma frase comum;
  "Hey Travis" disparou com uma das vozes (quase homófono, aceitável).
- `openwakeword` trouxe `scipy` e `scikit-learn` (~50 MB). Palmas mais sensíveis podem disparar com
  batidas secas duplas (ex.: na mesa); ajustar `CLAP_MIN_PEAK` se acontecer.

## Status

- aceita

## Data

- 2026-10-31
