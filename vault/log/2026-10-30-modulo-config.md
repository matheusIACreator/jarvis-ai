---
tipo: log
data: 2026-10-30
agente: claude-code
tarefa: Item 2 do backlog — módulo jarvis.config
tags: [log, fase-1, config]
---

# 2026-10-30 — Módulo de configuração

## O que foi feito

- Criado `src/jarvis/config.py`:
  - `load_config()` devolve um `Config` imutável (dataclass `frozen`).
  - Lê o `.env` da raiz do projeto, se existir; variáveis do ambiente real têm prioridade.
  - `ConfigError` lista **todas** as chaves obrigatórias faltando de uma vez.
  - Obrigatórias: `ANTHROPIC_API_KEY`, `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`.
  - Telegram opcional (`telegram_enabled` só com token e chat id).
  - Valores de exemplo (`your-...`) contam como ausentes.
  - `STARTUP_AUDIO_PATH` relativo é resolvido a partir da raiz do projeto (`pathlib`).
  - `repr` do `Config` não mostra segredos.
- Criado `tests/test_config.py`: 9 testes. Total: 11 testes passando.
- Verificado: sem `.env` local, a mensagem de erro é clara.

## Decisões tomadas

- [[decisoes/0008-config-sem-dependencia]]

## Problemas encontrados

- Nenhum.

## O que falta / próximo passo

- Usuário: copiar `.env.example` para `.env` e preencher as chaves reais.
- Item 3 do [[backlog]]: captura de microfone. Precisa de aprovação do usuário para a biblioteca
  (sugestão: `sounddevice`, leve, wheels prontos para Windows, entrega arrays NumPy).

## Arquivos principais tocados

- `src/jarvis/config.py`, `tests/test_config.py`
- `vault/em-andamento.md`, `vault/00-Indice.md`, `vault/backlog.md`, `vault/decisoes/0008-config-sem-dependencia.md`
