---
tipo: decisao
numero: "0006"
titulo: Troca entre agentes quando um fica sem tokens
status: aceita
data: 2026-10-30
agente: claude-code
tags: [decisao, memoria, agentes, handoff]
---

# 0006 — Troca entre agentes quando um fica sem tokens

## Contexto

- Claude Code e Codex compartilham a memória do [[decisoes/0004-memoria-compartilhada-obsidian|vault]].
- Quando um agente fica sem tokens no meio da tarefa, o protocolo de fim de sessão não roda e o progresso se perde.
- O usuário quer que, ao acabar o limite de um, o outro assuma.

## Decisão

- Novo arquivo [[em-andamento]]: checkpoint vivo da tarefa, atualizado após cada passo relevante (não só no fim).
- Commits de trabalho em andamento frequentes (`wip:` permitido), para o outro agente ver o código mais recente.
- No início da sessão, se `em-andamento.md` estiver `ativo`, o agente continua a tarefa a partir do "Próximo passo".
- Script `scripts/agent.ps1`: roda a tarefa no Claude Code em modo não interativo (`claude -p`); se a saída indicar limite de uso, repassa a mesma tarefa ao Codex (`codex exec`).

## Alternativas consideradas

- **Troca manual apenas** — funciona sempre, mas depende do usuário perceber e abrir o outro agente.
- **Trocar a sessão interativa ao vivo** — nenhuma das ferramentas permite transferir uma sessão interativa em andamento.

## Consequências

- Troca automática só no modo não interativo (via script). Em sessão interativa, a troca é manual: abrir o outro agente e dizer "continue a tarefa em andamento".
- Codex CLI ainda não está instalado nesta máquina; a parte do Codex no script não foi testada.
- A detecção de limite usa padrões de texto da mensagem de erro; pode precisar de ajuste.
- Exige disciplina: checkpoint desatualizado = trabalho perdido.

## Status

- aceita

## Data

- 2026-10-30
