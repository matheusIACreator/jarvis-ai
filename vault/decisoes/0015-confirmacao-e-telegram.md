---
tipo: decisao
numero: 0015
titulo: Confirmação por voz decidida pelo código e Telegram sem dependência
status: aceita
data: 2026-10-31
agente: claude-code
tags: [decisao, seguranca, telegram, fase-2]
---

# 0015 — Confirmação por voz decidida pelo código e Telegram sem dependência

## Contexto

- Regra do projeto: toda ação externa exige confirmação explícita do usuário antes.
- Itens 13 e 14 do [[backlog]]: enviar mensagem no Telegram e máquina de estados de confirmação.

## Decisão

- Ferramentas externas **não agem**: criam uma `PendingAction` no `ConfirmationGate` (`src/jarvis/confirmation.py`)
  e o modelo lê a ação de volta e pede confirmação.
- Quem decide é o **código**, pela fala do usuário (não o modelo):
  - "sim" só se a frase inteira for uma afirmação simples ("yes", "send it", "go ahead"...) → executa;
  - começa com negação ("no", "cancel", "wait"...) → cancela;
  - qualquer outra coisa → cancela e a fala segue para o cérebro como pedido novo.
- Ação pendente não passa para a próxima sessão.
- Resultado da confirmação (feito / recusado / falhou) vai para o histórico como mensagem `role: "system"`
  entre a fala do usuário e a resposta (atualizado em 2026-10-31: sem isso o modelo duvidava do próprio "Sent").
- `send_telegram_message`: só para o chat do próprio usuário (`TELEGRAM_CHAT_ID`); não envia a terceiros.
- Cliente do Telegram com `urllib` (biblioteca padrão); o token nunca aparece em erros, logs ou `repr`.
- Bot: @mmasago_jarvis_bot. Chat id obtido por `getUpdates` após o usuário clicar em "Start Bot".

## Alternativas consideradas

- **Modelo decide se houve "sim"** — o modelo poderia confirmar sozinho (ou ser induzido por conteúdo externo).
- **`python-telegram-bot`** — dependência grande para uma chamada HTTP; útil só ao receber mensagens (item 15).

## Consequências

- Confirmação previsível e testada (frases ambíguas nunca enviam).
- Respostas como "yes, but change it" cancelam e exigem novo pedido.

## Status

- aceita

## Data

- 2026-10-31
