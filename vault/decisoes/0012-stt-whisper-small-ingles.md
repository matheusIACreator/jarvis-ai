---
tipo: decisao
numero: 0012
titulo: STT com faster-whisper small, só inglês
status: aceita
data: 2026-10-31
agente: claude-code
tags: [decisao, stt, whisper, fase-1]
---

# 0012 — STT com faster-whisper small, só inglês

## Contexto

- Jarvis precisa transcrever comandos de voz localmente (sem enviar áudio para fora).
- Roda na CPU do notebook; latência pesa na experiência de voz.

## Decisão

- `faster-whisper` aprovado pelo usuário em 2026-10-31.
- Modelo `small`, CPU `int8`, idioma fixo **inglês** (`en`), ambos escolhas do usuário.
- `beam_size=1` (guloso), `vad_filter=True`, `condition_on_previous_text=False`.
- Fim do comando por silêncio: começa quando o RMS passa de 3× o piso de ruído (mín. 0,01),
  guarda 0,3 s antes, termina após 0,8 s de silêncio; máximo 12 s; desiste após 5 s sem fala.
- Configurável por `WHISPER_MODEL` e `WHISPER_LANGUAGE` no `.env`.

## Alternativas consideradas

- **`base`** — mais rápido, mais erros. **`large-v3-turbo`** — mais preciso, lento demais na CPU.
- **Detecção automática de idioma** — mais lenta e pode errar em frases curtas.
- **`beam_size=5`** — mesmo texto nos testes, ~0,3 s mais lento.

## Consequências

- Medido (áudio sintético da ElevenLabs, 3 s): ~1,5–1,7 s para transcrever, texto exato.
- Primeiro uso baixa o modelo (~460 MB) para `~/.cache/huggingface` (~30 s).
- PyAV (dependência do faster-whisper) também decodifica mp3 → item 5 sem biblioteca nova.
- Limiares de fala ainda não validados com a voz real do usuário (`scripts/listen.py`).

## Status

- aceita

## Data

- 2026-10-31
