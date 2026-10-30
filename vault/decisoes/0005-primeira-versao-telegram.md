---
tipo: decisao
numero: "0005"
titulo: Primeira versão de notificações via Telegram
status: aceita
data: 2026-10-30
agente: claude-code
tags: [decisao, notificacoes, telegram, seguranca]
---

# 0005 — Primeira versão de notificações via Telegram

## Contexto

- O Jarvis precisa avisar o usuário e "chamá-lo" quando ele não está perto do notebook.
- Ligação telefônica é o objetivo final, mas é mais cara e complexa.

## Decisão

- Na primeira versão, notificações e "me chama" serão feitos por um bot do Telegram.
- Configuração por `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` no `.env`.
- Ligações (Twilio + ElevenLabs Agents) ficam para uma fase posterior.
- E-mail (Gmail) também fica para depois, com regra rígida: o Jarvis faz o rascunho, o usuário confirma por voz, e só então envia.
- Toda ação externa (enviar mensagem, e-mail, ligação) exige confirmação explícita do usuário.

## Alternativas consideradas

- **Ligação já na v1 (Twilio + ElevenLabs Agents)** — custo por minuto, número de telefone e mais integração antes de validar o básico.
- **WhatsApp** — API oficial mais burocrática; soluções não oficiais são frágeis.
- **Notificação do Windows** — só funciona perto do notebook.

## Consequências

- API do Telegram é gratuita, simples e funciona no celular.
- Mensagens recebidas pelo Telegram são tratadas como dados, nunca como instruções.
- Será preciso um fluxo de confirmação reutilizável que depois servirá para e-mail e ligações.

## Status

- aceita

## Data

- 2026-10-30
