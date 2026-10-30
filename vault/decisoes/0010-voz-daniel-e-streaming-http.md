---
tipo: decisao
numero: 0010
titulo: Voz George e streaming HTTP em PCM
status: aceita
data: 2026-10-30
agente: claude-code
tags: [decisao, tts, elevenlabs, fase-1]
---

# 0010 — Voz George e streaming HTTP em PCM

## Contexto

- Usuário pediu a ElevenLabs como voz do Jarvis, voz masculina britânica.
- A [[decisoes/0002-voz-elevenlabs-flash|0002]] previa `eleven_flash_v2_5` por WebSocket.
- Chave criada com `npx -y @elevenlabs/cli@latest onboard init` (fica só no `.env`).

## Decisão

- Voz padrão **George** (`JBFqnCBsd6RMkjVDRZzb`): britânico, maduro, caloroso (atualizado em 2026-10-30).
  - Daniel (`onwK4e9ZLuTAKqWW03F9`) foi o primeiro padrão; usuário achou jovem demais.
  - Oliver (biblioteca, `L1aJrPa7pLJEyYlh3Ilq`) foi o preferido, mas vozes da biblioteca exigem plano pago
    (erro 402 `paid_plan_required`). Possível volta se o usuário assinar o Creator.
  - Trocar via `ELEVENLABS_VOICE_ID` no `.env`.
- `eleven_flash_v2_5` por **streaming HTTP** (`text_to_speech.stream`) em `pcm_24000`, tocado direto
  com `sounddevice` conforme os chunks chegam. Sem decodificar MP3, sem `ffplay`.
- O `.env` continua carregado pelo `jarvis.config` (não pelo `python-dotenv`); a chave vai para o SDK explicitamente.

## Alternativas consideradas

- **WebSocket `stream-input`** — só compensa quando o cérebro mandar texto em streaming; fica para depois.
- **MP3 + ffplay** — dependência externa e decodificação desnecessárias.
- **`python-dotenv`** — sugerido pelo `onboard check`, mas duplicaria o [[decisoes/0008-config-sem-dependencia|0008]].

## Consequências

- Latência baixa para respostas curtas, código simples e testável.
- O `onboard check` da CLI acusa "nada carrega o .env" (falso positivo: ele procura `load_dotenv`).
- Migrar para WebSocket quando o loop do cérebro gerar texto em streaming.

## Status

- aceita

## Data

- 2026-10-30
