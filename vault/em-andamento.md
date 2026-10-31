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

- Item 15 do [[backlog]]: conversar com o Jarvis por mensagens no Telegram (usuário confirmou que o envio por voz funcionou).
- Plano:
  - `interfaces/telegram.py`: `get_updates` (long polling) e `send_chat_action` ("digitando").
  - `interfaces/telegram_chat.py`: `TelegramChat` — thread em segundo plano; só aceita mensagens do
    `TELEGRAM_CHAT_ID`; texto vira pedido do usuário (papel `user`, nunca instrução de sistema);
    resposta enviada no mesmo chat; mensagens antigas (Jarvis offline) são descartadas ao iniciar.
  - `Assistant` com prompt próprio para texto e histórico separado da voz.

## Feito até agora

- Tarefa marcada como ativa.

## Próximo passo

- Escrever cliente + `TelegramChat` + testes; ligar no `app.py`.

## Arquivos tocados (ainda sem commit)

- `vault/em-andamento.md`
