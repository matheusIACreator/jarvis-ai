---
tipo: em-andamento
data: 2026-10-30
agente: claude-code
status: ativo
tags: [handoff, memoria]
---

# Em andamento

Checkpoint vivo da tarefa atual. Atualizar **durante** a sessão, após cada passo relevante,
para que o outro agente consiga continuar se este ficar sem tokens no meio do trabalho.

- `status: livre` → nenhuma tarefa em andamento; pegar a próxima do [[00-Indice]].
- `status: ativo` → existe tarefa em andamento; continuar a partir do "Próximo passo".

## Tarefa

- (1) Corrigir `scripts/agent.ps1` para o Codex conseguir registrar commits; (2) item 1 do [[backlog]]: ambiente de desenvolvimento.

## Feito até agora

- Commit das alterações pendentes da sessão do Codex (`624feec`).
- Escolhido Python 3.12 (3.11 não está instalado; 3.14 é novo demais para libs de áudio/ML).

## Próximo passo

- Ajustar `scripts/agent.ps1` (commit após o Codex) e criar a `.venv` com `py -3.12`.

## Arquivos tocados (ainda sem commit)

- `vault/em-andamento.md`
