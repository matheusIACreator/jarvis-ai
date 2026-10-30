---
tipo: decisao
numero: 0008
titulo: Configuração sem dependência externa
status: aceita
data: 2026-10-30
agente: claude-code
tags: [decisao, config, fase-1]
---

# 0008 — Configuração sem dependência externa

## Contexto

- O Jarvis precisa carregar chaves e caminhos do `.env` com erro claro quando faltar algo.
- Regra do projeto: preferir soluções simples e evitar dependências desnecessárias.

## Decisão

- Parser próprio de `.env` em `jarvis.config` (~20 linhas): `KEY=value`, comentários `#`, aspas, `export`.
- O `.env` é lido mas **não** é copiado para `os.environ`; o ambiente real tem prioridade.
- `Config` é uma dataclass imutável; `ConfigError` lista todas as chaves faltando.
- Valores começando com `your-` (do `.env.example`) contam como ausentes.

## Alternativas consideradas

- **python-dotenv** — funciona, mas é uma dependência a mais para algo trivial.
- **pydantic-settings** — validação rica, porém pesado demais para seis variáveis.

## Consequências

- Zero dependências novas; comportamento totalmente coberto por testes.
- Não suporta recursos avançados do dotenv (interpolação `${VAR}`, valores multilinha). Trocar para `python-dotenv` se isso for necessário.

## Status

- aceita

## Data

- 2026-10-30
