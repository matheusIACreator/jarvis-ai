---
tipo: log
data: 2026-10-31
agente: claude-code
tarefa: Corrigir palmas que não disparavam e adicionar "Hey Jarvis"
tags: [log, fase-1, gatilho]
---

# 2026-10-31 — Palmas e "Hey Jarvis"

## O que foi feito

- Gravação de diagnóstico de 60 s com o usuário batendo palmas: picos 0,12–0,27 < mínimo 0,25 → causa encontrada.
- `trigger/clap.py`: `min_peak` 0,08; piso de ruído atualiza em som alto contínuo. `CLAP_MIN_PEAK` no config.
- Instalado `openwakeword 0.6.0` (+ scipy, scikit-learn); modelo `hey_jarvis` baixado.
- `trigger/wake_word.py`: `WakeWordDetector` (reagrupa blocos em quadros de 1280 amostras int16).
- `app.py`: `wait_for_trigger` (palmas ou "Hey Jarvis"); `WAKE_WORD_THRESHOLD` no config.
- Teste com fala sintética da ElevenLabs e teste de fumaça do serviço (sobe e espera os dois gatilhos).
- Testes: 118 passando.

## Decisões tomadas

- [[decisoes/0016-palavra-de-ativacao]]

## Problemas encontrados

- Teste de sala ruidosa falhou com o limiar menor (detector travado em "som contínuo") → piso de ruído adaptado.

## O que falta / próximo passo

- Usuário: testar palmas e "Hey Jarvis" no serviço real.
- Próximo: item 15 do [[backlog]] (comandos pelo Telegram) ou item 16.

## Arquivos principais tocados

- `src/jarvis/trigger/clap.py`, `src/jarvis/trigger/wake_word.py`, `src/jarvis/app.py`, `src/jarvis/config.py`
- `.env.example`, `pyproject.toml`, `tests/test_clap.py`, `tests/test_wake_word.py`, `tests/test_audio_file.py`
