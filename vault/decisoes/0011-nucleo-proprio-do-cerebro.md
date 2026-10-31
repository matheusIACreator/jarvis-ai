---
tipo: decisao
numero: 0011
titulo: Núcleo próprio do cérebro (sem Hermes Agent)
status: aceita
data: 2026-10-31
agente: claude-code
tags: [decisao, cerebro, anthropic, fase-1]
---

# 0011 — Núcleo próprio do cérebro (sem Hermes Agent)

## Contexto

- Usuário cogitou usar o Hermes Agent (Nous Research) como harness.
- Comparado em 2026-10-30; usuário decidiu em 2026-10-31: construir o núcleo. Reforça [[decisoes/0001-cerebro-api-anthropic]].

## Decisão

- Loop manual sobre o SDK `anthropic` em `src/jarvis/brain/assistant.py` (`Assistant.reply`).
- `claude-haiku-5-5`, `effort: low`, `max_tokens` 2048, sem `temperature` (dá 400 no Haiku 5.5).
- Prompt de sistema fixo com `cache_control`; ferramentas ordenadas por nome (prefixo estável para o cache).
- Dentro de um turno: conteúdo do assistente (thinking + tool_use) volta à API sem alteração.
- Entre turnos: histórico só com o texto das trocas, últimas 6. Assim, cortar o histórico não edita
  turnos com blocos de thinking (o Haiku 5.5 dá 400 se o histórico antes deles mudar).
- Ferramentas atrás de `ToolRegistry` (`src/jarvis/tools/base.py`); erro de ferramenta vira `is_error`, não derruba o loop.
- Data/hora é ferramenta, não texto no prompt (timestamp no prompt quebraria o cache).

## Alternativas consideradas

- **Hermes Agent** — Windows nativo em beta (WSL2 recomendado, contra [[decisoes/0003-tudo-nativo-no-windows]]),
  instala Python 3.11/Node/ffmpeg/Git Bash próprios, prompts grandes (latência de voz), memória própria
  duplicando o vault. Reavaliar na Fase 2 (gateway do Telegram, cron).
- **Tool Runner do SDK (beta)** — menos código, mas o loop próprio facilita o histórico só-texto e o
  futuro portão de confirmação (item 14).

## Consequências

- Código pequeno e testável com cliente falso (8 testes do loop, 7 das ferramentas).
- Cache só passa a valer quando prompt + ferramentas passarem de 512 tokens.
- O modelo não lembra o raciocínio de turnos anteriores, só o texto (aceitável para voz).

## Status

- aceita

## Data

- 2026-10-31
