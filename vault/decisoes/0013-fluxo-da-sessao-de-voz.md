---
tipo: decisao
numero: 0013
titulo: Fluxo da sessão de voz
status: aceita
data: 2026-10-31
agente: claude-code
tags: [decisao, servico, fase-1]
---

# 0013 — Fluxo da sessão de voz

## Contexto

- Itens 5, 6 e 11 do [[backlog]]: ligar gatilho, música, saudação, STT, cérebro e voz num processo só.

## Decisão

- Entrada: `python -m jarvis` (`src/jarvis/app.py`).
- Palmas duplas → música de abertura → saudação → conversa → volta a esperar palmas.
- Música: PyAV decodifica, `sounddevice` toca sem bloquear; padrão 10 s com fade de 1,5 s
  (`STARTUP_AUDIO_SECONDS`, `0` = arquivo inteiro). Sem arquivo → só a saudação.
- Saudação local por horário ("Good evening, sir. How may I help?"), sintetizada **durante** a música.
- Conversa contínua: perguntas seguidas sem bater palmas de novo; termina com silêncio (5 s)
  ou despedida ("that's all", "goodbye", "no"...), com resposta curta de despedida.
- Detector de palmas não recebe áudio durante a sessão; a fila do microfone é esvaziada antes de
  ouvir, para não transcrever a própria voz do Jarvis.
- Erros de API viram frase falada curta; qualquer erro na sessão é registrado e o serviço continua.

## Alternativas consideradas

- **Saudação gerada pelo Claude** — mais variada, mas adiciona latência e custo a cada ativação.
- **Uma palma dupla por pergunta** — mais simples, porém pouco natural.

## Consequências

- Tudo síncrono em uma thread principal + 1 thread para pré-gerar a saudação.
- Sem barge-in: não dá para interromper o Jarvis enquanto ele fala (fica para depois).
- Limiares das palmas ainda não validados com palmas reais (item 4b).

## Status

- aceita

## Data

- 2026-10-31
