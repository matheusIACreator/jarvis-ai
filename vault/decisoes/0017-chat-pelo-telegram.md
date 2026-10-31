---
tipo: decisao
numero: 0017
titulo: Conversa pelo Telegram em canal separado
status: aceita
data: 2026-10-31
agente: claude-code
tags: [decisao, telegram, seguranca, fase-2]
---

# 0017 — Conversa pelo Telegram em canal separado

## Contexto

- Item 15 do [[backlog]]: falar com o Jarvis por mensagem no Telegram.
- Regra: conteúdo externo (inclusive mensagens do Telegram) é dado, nunca instrução.

## Decisão

- `TelegramChat` (`src/jarvis/interfaces/telegram_chat.py`): thread em segundo plano com long polling (`getUpdates`).
- Só responde ao `TELEGRAM_CHAT_ID` do usuário; outros chats são ignorados e registrados no log.
- Texto do usuário entra como pedido (papel `user`), nunca como instrução de sistema; conteúdo citado ou
  encaminhado dentro da mensagem é dado.
- `Assistant` próprio para texto: prompt `TEXT_CHAT_PROMPT` (respostas escritas, texto simples) e histórico
  separado da voz. Ferramentas: relógio + advisor (sem envio ao Telegram, sem encerrar sessão).
- Responder no próprio chat em que o usuário escreveu não exige confirmação (é a resposta ao pedido dele,
  não uma ação em nome dele). Ações externas continuam exigindo "sim" ([[decisoes/0015-confirmacao-e-telegram]]).
- Mensagens recebidas com o Jarvis desligado são descartadas ao iniciar; "digitando…" enquanto pensa.
- Thread nunca morre em silêncio: qualquer erro é registrado e o loop tenta de novo em 5 s.

## Alternativas consideradas

- **Webhook** — exige servidor público com HTTPS; long polling funciona atrás do roteador de casa.
- **`python-telegram-bot`** — mais recursos, mas dependência grande para poucas chamadas.

## Consequências

- Sobe junto com `python -m jarvis`; `scripts/telegram_chat.py` roda só o Telegram.
- Testado em 2026-10-31: "What day is it today?" respondido com a data certa pelo Telegram.

## Status

- aceita

## Data

- 2026-10-31
