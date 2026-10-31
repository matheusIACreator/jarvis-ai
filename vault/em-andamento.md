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

- Itens 8 e 9 do [[backlog]]: núcleo próprio do cérebro (decisão do usuário em 2026-10-31:
  construir, não usar Hermes Agent; mantém [[decisoes/0001-cerebro-api-anthropic]]).
- `src/jarvis/brain/`: loop de conversa com `claude-haiku-5-5`, prompt de sistema com cache,
  histórico curto, chamada de ferramentas. `src/jarvis/tools/`: contrato único + tool de data/hora.
- `ANTHROPIC_API_KEY` já está no `.env` (usuário confirmou).

## Feito até agora

- Tarefa marcada como ativa.
- `anthropic 2.3.0` instalado. Escritos `tools/base.py`, `tools/clock.py`, `brain/assistant.py`, `scripts/chat.py` e testes (42 passando).

## Próximo passo

- Teste real na API (uma pergunta de data/hora), depois fechar a sessão (log, decisão 0011, índice, backlog).

## Arquivos tocados (ainda sem commit)

- `vault/em-andamento.md`
