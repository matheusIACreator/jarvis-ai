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

- Fase 2: itens 14 (confirmação) e 13 (enviar mensagem no Telegram) do [[backlog]].
- Plano:
  - Descobrir `TELEGRAM_CHAT_ID` via `getUpdates` (usuário mandou "Hey Jarvis" ao bot; token já no `.env`).
  - `interfaces/telegram.py`: cliente HTTP só com a biblioteca padrão (`urllib`), sem dependência nova; nunca logar o token.
  - `confirmation.py`: `ConfirmationGate` determinístico — a ferramenta só cria ação pendente; envio só com "sim"
    explícito do usuário, decidido pelo código (não pelo modelo). "Não" cancela; resposta ambígua cancela e segue para o cérebro.
  - Ferramenta `send_telegram_message` (só para o chat do próprio usuário).

## Feito até agora

- Tarefa marcada como ativa.
- Bot é @mmasago_jarvis_bot. O usuário só consegue clicar em "Start Bot" (`/start`), e isso basta.
- `TELEGRAM_CHAT_ID` obtido via `getUpdates` e gravado no `.env`; Telegram habilitado na configuração.
- Escritos `confirmation.py`, `interfaces/telegram.py`, `tools/telegram.py`, ligação no `app.py`/`conversation.py`, testes (111 passando).

## Próximo passo

- Com autorização do usuário: enviar mensagem de teste real; depois fechar a sessão (log, decisão 0015, índice, backlog).

## Arquivos tocados (ainda sem commit)

- `vault/em-andamento.md`
