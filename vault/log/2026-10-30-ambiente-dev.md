---
tipo: log
data: 2026-10-30
agente: claude-code
tarefa: Corrigir commit do Codex no fallback e configurar o ambiente de desenvolvimento
tags: [log, fase-1, ambiente, handoff]
---

# 2026-10-30 — Ambiente de desenvolvimento

## O que foi feito

- Usuário confirmou o Codex CLI instalado e funcionando (`codex-cli 0.166.0`).
- Commit das alterações da sessão anterior do Codex ([[log/2026-10-30-verificacao-estado]]), que ficaram sem commit por causa do sandbox.
- `scripts/agent.ps1`: Codex roda com `--sandbox workspace-write` e o script faz o commit das alterações dele ao final.
- `AGENTS.md`: regra para o Codex quando `.git` estiver somente leitura.
- Criada a `.venv` com Python 3.12.10, `pip install -e ".[dev]"` (pytest), configuração do pytest no `pyproject.toml`.
- Teste de fumaça `tests/test_package.py`: `import jarvis` e subpacotes. Resultado: 2 testes passando.

## Decisões tomadas

- [[decisoes/0007-python-3-12]]

## Problemas encontrados

- Sandbox `workspace-write` do Codex mantém `.git` somente leitura → resolvido com commit pelo script.
- PowerShell 5.1 mostra acentos quebrados em `Get-Content` de arquivos UTF-8 sem BOM; os arquivos estão corretos (é só exibição).

## O que falta / próximo passo

- Item 2 do [[backlog]]: módulo `jarvis.config` carregando o `.env`.
- Fallback Claude → Codex por limite de uso ainda não foi observado de verdade (só a rota direta `-Agent codex`).

## Arquivos principais tocados

- `scripts/agent.ps1`, `AGENTS.md`, `README.md`, `pyproject.toml`, `tests/test_package.py`
- `vault/em-andamento.md`, `vault/00-Indice.md`, `vault/backlog.md`, `vault/decisoes/0007-python-3-12.md`
