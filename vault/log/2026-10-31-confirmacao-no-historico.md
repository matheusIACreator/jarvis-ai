---
tipo: log
data: 2026-10-31
agente: claude-code
tarefa: Corrigir o Jarvis duvidando de mensagem já enviada
tags: [log, fase-2, cerebro, telegram]
---

# 2026-10-31 — Confirmação registrada no histórico

## O que foi feito

- Usuário testou no serviço: palmas OK; mensagem "buy milk" enviada após "Do it.", mas no turno seguinte
  o Jarvis disse que não tinha enviado e ofereceu reenviar.
- Causa: o histórico só tinha o texto "Sent to your Telegram" sem nenhuma chamada de ferramenta; o modelo
  concluiu que tinha inventado.
- `confirmation.py`: `resolve` devolve `Resolution(reply, record)`.
- `assistant.py`: histórico por turno (`turns`); `remember(..., record)` insere `role: "system"` com o fato.
- `app.py`: grava o registro após cada confirmação.
- Teste real na API repetindo a conversa do usuário (envio falso): sem dúvida, sessão encerrada pela ferramenta.
- Testes: 119 passando.

## Decisões tomadas

- [[decisoes/0015-confirmacao-e-telegram]] atualizada.

## Problemas encontrados

- Uma edição quebrou uma f-string (apóstrofo em "user's"); corrigida antes dos testes.

## O que falta / próximo passo

- Usuário: repetir o teste de envio pelo serviço.
- Próximo: item 15 do [[backlog]] (comandos pelo Telegram) ou item 16.

## Arquivos principais tocados

- `src/jarvis/confirmation.py`, `src/jarvis/brain/assistant.py`, `src/jarvis/app.py`, `src/jarvis/tools/telegram.py`
- `tests/test_confirmation.py`, `tests/test_assistant.py`
