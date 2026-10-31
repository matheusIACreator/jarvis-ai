---
tipo: em-andamento
data: 2026-10-31
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

- (a) Ferramenta `end_conversation`: "That's okay, Jarvis. Thank you." não encerrou a sessão (lista fixa de frases).
  Claude chama a ferramenta ao perceber a despedida; ferramenta "final" encerra o turno sem nova chamada à API.
- (b) Item 12 do [[backlog]]: escalonamento para `claude-sonnet-5-5` via ferramenta de servidor **advisor**
  (`advisor_20260301`, beta `advisor-tool-2026-03-01`): Haiku executa, consulta o Sonnet só em perguntas difíceis;
  `max_uses` 1, `max_tokens` limitado, cache do prompt do advisor.

## Feito até agora

- Conversa completa validada pelo usuário; tarefa marcada como ativa.

## Próximo passo

- Implementar (a) em `tools/session.py` + `Tool.final` + `Conversation.finished`; depois (b) em `brain/assistant.py`.

## Arquivos tocados (ainda sem commit)

- `vault/em-andamento.md`, `vault/00-Indice.md`
