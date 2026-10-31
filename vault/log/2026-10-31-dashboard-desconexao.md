---
tipo: log
data: 2026-10-31
agente: codex
tarefa: Corrigir desconexão HTTP do painel
tags: [log, frontend, correcao]
---

# 2026-10-31 — Desconexão HTTP do painel

## O que foi feito
- Tratados ConnectionAbortedError (WinError 10053), ConnectionResetError e BrokenPipeError ao escrever cabeçalhos ou corpo da resposta.
- Conexão encerrada sem nova tentativa de resposta; erros não relacionados continuam visíveis.
- Estado copiado sob bloqueio e transmitido depois de liberá-lo, evitando bloquear o fluxo de voz pela rede.
- Oito testes de regressão novos; 172 testes da suíte completa passaram.

## Decisões tomadas
- Nenhuma mudança de arquitetura; mantém [[decisoes/0021-painel-e-memoria]].

## Problemas encontrados
- O log do usuário mostrou conexão abortada ao responder ao painel; a causa exata do cancelamento não foi identificada. A voz continuou aguardando gatilho.
- Commit permanece sujeito ao bloqueio de escrita em .git deste ambiente.

## O que falta / próximo passo
- Reiniciar o serviço Python para carregar a correção; validar uso com o painel aberto.

## Arquivos principais tocados
- src/jarvis/interfaces/dashboard.py
- tests/test_memory_dashboard.py
- vault/00-Indice.md, vault/backlog.md, vault/em-andamento.md
