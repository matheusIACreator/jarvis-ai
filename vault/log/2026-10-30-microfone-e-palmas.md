---
tipo: log
data: 2026-10-30
agente: claude-code
tarefa: Itens 3 e 4 do backlog — captura de microfone e detector de palmas duplas
tags: [log, fase-1, audio, gatilho]
---

# 2026-10-30 — Microfone e detector de palmas

## O que foi feito

- Usuário aprovou `sounddevice` (+ `numpy`); adicionados ao `pyproject.toml`.
- `src/jarvis/trigger/microphone.py`: `MicrophoneStream` mono float32, 16 kHz, blocos de 512 (32 ms),
  fila limitada que descarta o bloco mais antigo quando o consumidor atrasa.
- `src/jarvis/trigger/clap.py`: `ClapDetector` + `ClapSettings`.
  - Palma = pico ≥ max(0,25; piso de ruído × 10) e silêncio de novo em até 120 ms.
  - Som alto mais longo é rejeitado e cancela um par pendente.
  - Duas palmas com intervalo de 0,12–0,8 s disparam; depois 1,5 s de cooldown.
  - Piso de ruído adaptativo (média móvel do RMS dos blocos silenciosos).
- `scripts/clap_monitor.py`: monitor ao vivo (pico, piso de ruído, aviso de palma dupla).
- Testes: 23 passando (microfone: 4; palmas: 8, com sinais sintéticos).
- Captura real no microfone Realtek a 16 kHz funcionou sem blocos descartados.

## Decisões tomadas

- [[decisoes/0009-audio-sounddevice-e-palmas-por-pico]]

## Problemas encontrados

- Primeira versão usava o RMS do bloco → palma sumia em ambiente ruidoso. Trocado para pico.
- Ambiente muito silencioso no teste (pico ~0,001). **Limiar `min_peak=0,25` ainda não validado com palmas reais.**

## O que falta / próximo passo

- Usuário: rodar `.\.venv\Scripts\python.exe scripts\clap_monitor.py`, bater palmas e ajustar `ClapSettings` se preciso.
- Item 5 do [[backlog]]: tocar o áudio de abertura. Exige biblioteca para tocar mp3 → pedir aprovação.

## Arquivos principais tocados

- `pyproject.toml`, `src/jarvis/trigger/microphone.py`, `src/jarvis/trigger/clap.py`
- `tests/test_microphone.py`, `tests/test_clap.py`, `scripts/clap_monitor.py`
