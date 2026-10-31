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

- Bug: após "Do it." a mensagem foi enviada, mas no turno seguinte o modelo achou que não tinha enviado
  (viu "Sent" no histórico sem nenhuma chamada de ferramenta e se "corrigiu").
- Correção: registrar o resultado da confirmação como mensagem `role: "system"` no meio da conversa
  (Haiku 5.5 suporta, sem beta). `ConfirmationGate.resolve` passa a devolver fala + registro.
  Histórico vira lista de turnos (corte por turno, nunca deixa `system` como primeira mensagem).

## Feito até agora

- Causa identificada a partir do log do usuário (palmas funcionaram).

## Próximo passo

- Alterar `confirmation.py`, `assistant.py`, `app.py`, testes; teste real na API com envio falso.

## Arquivos tocados (ainda sem commit)

- `vault/em-andamento.md`
