---
tipo: decisao
numero: "0021"
titulo: Painel local e memória de conversas
status: aceita
data: 2026-10-31
agente: codex
tags: [decisao, frontend, memoria, obsidian]
---

# 0021 — Painel local e memória de conversas

## Contexto
- Matheus pediu frontend Next.js/React/shadcn inspirado em um núcleo luminoso e skills Obsidian para memória compartilhada.

## Decisão
- Frontend em `frontend/`, inicializado pelo CLI shadcn, com SVG/CSS animado por estado de fala.
- Ponte Python na porta 8765 e Next.js na 3000, ambas em loopback; proxy do servidor sem expor credenciais ao navegador.
- Chat web separado da voz, com ferramentas de relógio e busca; sem ferramentas de ações externas.
- Conversas em Markdown citado em `vault/conversas/`, fora do Git. Busca lexical consultável pelo cérebro e painel, compartilhada entre voz, web e Telegram.
- Skills de kepano em `.claude/skills/`, com licença preservada e instruções para ambos os agentes em AGENTS.md.
- Webpack nos comandos locais: Turbopack falhou ao iniciar o processo CSS neste Windows.

## Alternativas consideradas
- Banco vetorial ou serviço remoto: complexidade desnecessária nesta fase.
- CLI Obsidian no fluxo de voz: exige aplicativo aberto; arquivos Markdown dispensam isso.
- Publicação remota: não serve à integração com áudio e arquivos privados do computador.

## Consequências
- Sem dependências Python adicionais; painel requer Node e processo Next.js separado.
- Animação por período de fala, sem análise de amplitude; chat web é textual.
- Busca percorre notas locais; reavaliar indexação se o volume crescer.
- Filtro conservador pula padrões comuns de credenciais, mas não garante detectar todo segredo; nunca ditar senhas.
- Não recupera conversas anteriores que não foram persistidas.

## Status
- aceita

## Data
- 2026-10-31
