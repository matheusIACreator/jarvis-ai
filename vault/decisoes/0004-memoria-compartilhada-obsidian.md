---
tipo: decisao
numero: "0004"
titulo: Memória compartilhada em vault do Obsidian
status: aceita
data: 2026-10-30
agente: claude-code
tags: [decisao, memoria, agentes, obsidian]
---

# 0004 — Memória compartilhada em vault do Obsidian

## Contexto

- Dois agentes de código trabalham no repositório: Claude Code e Codex.
- Cada agente começa sem memória da sessão anterior; sem um registro comum, decisões se perdem e trabalho é refeito.

## Decisão

- Memória compartilhada = arquivos Markdown simples em `vault/`, compatível com Obsidian, versionado no git.
- Regras dos agentes em um único arquivo: `AGENTS.md` (o `CLAUDE.md` apenas importa `@AGENTS.md`).
- Protocolo de sessão obrigatório:
  - **Início:** ler `00-Indice.md`, depois o log mais recente em `log/`, depois as decisões relevantes.
  - **Fim:** criar novo log (`AAAA-MM-DD-slug.md`, a partir do modelo), atualizar `00-Indice.md` (estado atual + próxima tarefa), atualizar `backlog.md`, criar nota em `decisoes/` para escolhas não triviais, e fazer commit.
- Logs são somente acréscimo: nunca editar nem apagar logs antigos; sempre registrar o agente (`claude-code` ou `codex`).
- Notas do vault em pt-BR, curtas e estruturadas (frontmatter, títulos, tópicos), para que o próprio Jarvis possa lê-las como memória no futuro.

## Alternativas consideradas

- **Memória própria de cada agente** — não é compartilhada entre Claude Code e Codex.
- **Banco de dados / serviço de memória** — mais complexo, sem histórico legível no git.
- **Arquivos de regras separados por agente** — risco de divergência entre as regras.

## Consequências

- Histórico de decisões e sessões legível por humanos e por agentes, versionado junto com o código.
- Exige disciplina: o protocolo de fim de sessão precisa ser seguido sempre.
- Arquivos locais do Obsidian (`workspace*.json`, cache) ficam fora do git.
- Nenhuma credencial pode ser gravada no vault.

## Status

- aceita

## Data

- 2026-10-30
