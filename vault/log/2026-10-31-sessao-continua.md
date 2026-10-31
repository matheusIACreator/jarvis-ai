---
tipo: log
data: 2026-10-31
agente: codex
tarefa: Evitar reativação após pausas e confirmação repetida
tags: [log, voz, confirmacao, fase-2]
---

# 2026-10-31 — Sessão contínua durante pausas

## O que foi feito

- Usuário confirmou correção do PyAV e forneceu log real de "me chama"; iniciar tarefa exigiu várias confirmações e a sessão retornou ao gatilho após silêncio.
- Serviço agora espera fala sem limite por padrão, com `SESSION_IDLE_SECONDS` opcional; despedida explícita continua voltando ao gatilho.
- Captura ignora transcrição vazia em vez de encerrar a sessão. Scripts avulsos mantêm limite original de 5 s.
- Perguntas de confirmação do Telegram e tarefa vêm diretamente da ferramenta após registrar a ação; modelo não reformula esse resultado nem pode executar pela própria confirmação.
- Prompt orienta preparar ação antes de perguntar e não encerrar em "Okay, I'll wait"; frase explícita de iniciar/enviar reconhecida pelo código.
- Confirmação expira em 60 s e não pode ser substituída enquanto válida. Respostas ambíguas e com ressalvas continuam sem executar.
- Suíte completa: 160 testes passando, incluindo novas regressões para silêncio, ruído, configuração, pergunta direta e aprovação única/expirada.
- Validação com Anthropic real: pedido igual ao log registrou a tarefa antes da pergunta; uma aprovação executou trabalho simulado uma vez; "Okay, I'll wait" não encerrou. Sem captura, TTS ou Telegram real nesse teste.
- Teste manual local em `.venv/verify_voice_session.py` (ignorado pelo git); nenhuma credencial impressa ou registrada no vault.
- README, exemplo de ambiente, arquitetura, índice e backlog atualizados.

## Decisões tomadas

- [[../decisoes/0020-sessao-continua-e-confirmacao-direta|0020 — Sessão contínua e confirmação direta]]

## Problemas encontrados

- O log não distingue ausência inicial de chamada de ferramenta de outros detalhes internos; não foi atribuído o primeiro "yes" a uma falha comprovada do gate. O fluxo foi reforçado e validado com o modelo real.
- Alterações das sessões anteriores continuam sem commit; `.git` permanece sem permissão de escrita no sandbox.

## O que falta / próximo passo

- Reiniciar serviço e validar por voz: pedir análise, confirmar uma vez, esperar em silêncio e retomar sem ativação; conferir resultado real no Telegram (item 16b do [[../backlog|backlog]]).
- Para voltar ao gatilho, dizer "that's all" ou "go to sleep". Manter processo ligado enquanto espera tarefa.
- Commit pelo script de troca ou agente com permissão em `.git`; depois Gmail (item 17).

## Arquivos principais tocados

- `src/jarvis/app.py`, `src/jarvis/config.py`, `src/jarvis/stt/recorder.py`
- `src/jarvis/confirmation.py`, `src/jarvis/brain/assistant.py`, `src/jarvis/tools/base.py`, `src/jarvis/tools/background.py`, `src/jarvis/tools/telegram.py`, `src/jarvis/tools/session.py`
- `tests/test_stt.py`, `tests/test_config.py`, `tests/test_confirmation.py`, `tests/test_assistant.py`, `tests/test_background.py`
- `.env.example`, `README.md` e notas do vault desta sessão.
