---
tipo: log
data: 2026-10-31
agente: claude-code
tarefa: Item 15 do backlog — conversar com o Jarvis pelo Telegram
tags: [log, fase-2, telegram]
---

# 2026-10-31 — Chat pelo Telegram

## O que foi feito

- Usuário confirmou que o envio ao Telegram por voz funcionou após a correção do histórico.
- `interfaces/telegram.py`: `get_updates` (long polling), `send_typing`; parâmetro `http_timeout`.
- `interfaces/telegram_chat.py`: `TelegramChat` (só o chat do usuário, ignora o resto, descarta mensagens antigas).
- `brain/assistant.py`: `TEXT_CHAT_PROMPT` e `system_prompt` configurável.
- `app.py`: canal do Telegram sobe junto com o serviço; `safe_reply` compartilhado.
- `scripts/telegram_chat.py`: roda só o Telegram (opcional: minutos).
- Teste real: "What day is it today?" → "Today is Saturday, 31 October 2026, sir..." no Telegram.
- Testes: 128 passando.

## Decisões tomadas

- [[decisoes/0017-chat-pelo-telegram]]

## Problemas encontrados

- Primeiro teste real: nada respondia. Causa: `call(..., timeout=...)` colidia com o parâmetro `timeout` do
  `getUpdates` (TypeError) e a thread morria em silêncio. Corrigido (`http_timeout`), loop resistente a erros,
  e teste novo que exercita o cliente real com HTTP falso (os testes antigos usavam um bot falso e não pegaram).

## O que falta / próximo passo

- Item 16 do [[backlog]]: "me chama" (aviso no Telegram quando uma tarefa longa termina).
- Ideias: lembretes agendados, memória do vault acessível ao Jarvis, barge-in (interromper a fala).

## Arquivos principais tocados

- `src/jarvis/interfaces/telegram.py`, `src/jarvis/interfaces/telegram_chat.py`, `src/jarvis/brain/assistant.py`
- `src/jarvis/app.py`, `scripts/telegram_chat.py`, `tests/test_telegram_chat.py`, `tests/test_confirmation.py`
