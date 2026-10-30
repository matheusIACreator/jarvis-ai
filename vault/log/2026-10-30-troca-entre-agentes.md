---
tipo: log
data: 2026-10-30
agente: claude-code
tarefa: Permitir que Claude Code e Codex troquem entre si quando um fica sem tokens
tags: [log, fase-0, handoff]
---

# 2026-10-30 — Troca entre agentes

## O que foi feito

- Criado [[em-andamento]]: checkpoint vivo da tarefa atual.
- Protocolo de sessão no `AGENTS.md` atualizado: ler e manter `em-andamento.md`, commits `wip:` frequentes.
- Criado `scripts/agent.ps1`: roda no Claude Code e repassa ao Codex se o limite de uso for atingido.

## Decisões tomadas

- [[decisoes/0006-troca-entre-agentes]]

## Problemas encontrados

- Codex CLI não está instalado nesta máquina; o fallback para o Codex não foi testado.
- Não é possível trocar automaticamente uma sessão interativa em andamento; só o modo não interativo.

## O que falta / próximo passo

- Usuário instalar o Codex CLI e fazer login; testar `scripts/agent.ps1 -Agent codex`.
- Depois: item 1 do [[backlog]] (ambiente de desenvolvimento).

## Arquivos principais tocados

- `AGENTS.md`, `README.md`, `scripts/agent.ps1`
- `vault/em-andamento.md`, `vault/decisoes/0006-troca-entre-agentes.md`, `vault/00-Indice.md`, `vault/backlog.md`
