---
tipo: log
data: 2026-10-31
agente: codex
tarefa: Corrigir erro de Controle de Aplicativos ao iniciar Whisper
tags: [log, windows, stt, dependencias]
---

# 2026-10-31 — Corrigir bloqueio do PyAV no Windows

## O que foi feito

- Reproduzido o erro informado pelo usuário na importação de `av`.
- Consulta autorizada dos eventos do Windows confirmou bloqueio de `av/bitstream.pyd` do PyAV 19.0.2 pelo Controle de Aplicativos (evento 3077).
- Baixado wheel oficial PyAV 18.0.0 do PyPI e instalado na `.venv`; importações reais `av` e `faster_whisper` passaram.
- Pin específico para Windows em `pyproject.toml` e instruções de reparo no README.
- Nenhuma proteção desativada ou política alterada.
- Verificação real offline: Whisper small/CPU/int8 carregou, VAD com silêncio retornou texto vazio e MP3 de abertura foi decodificado, sem tocar áudio.
- `pip check`: nenhum requisito quebrado. Suíte completa: 141 testes passando.
- Nenhuma API paga, mensagem Telegram ou captura de microfone usada na validação.

## Decisões tomadas

- [[../decisoes/0019-pyav-compativel-com-app-control|0019 — PyAV compatível com Controle de Aplicativos]]

## Problemas encontrados

- Sandbox impediu consulta dos eventos, acesso de rede do pip e uso de temporários durante substituição de pacote; operações necessárias repetidas com autorização fora do sandbox.
- Tentativa inicial de instalação deixou resíduos `~v`, `~v.libs` e `~v-19.0.2.dist-info`; arquivados em `.venv/repair-backup-pyav-19.0.2`, sem excluir arquivos.
- Wheel de reparo guardado em `.venv/repair-wheels`. Ambos os diretórios são locais e ignorados pelo git.
- `.git` continua sem permissão para commit; alterações anteriores de [[2026-10-31-me-chama]] preservadas.

## O que falta / próximo passo

- Usuário pode executar novamente `python -m jarvis` e validar o "me chama" por voz e bot reais (item 16b do [[../backlog|backlog]]).
- Registrar alterações pendentes em commit pelo script de troca ou agente com permissão em `.git`.

## Arquivos principais tocados

- `pyproject.toml`, `README.md`
- `vault/00-Indice.md`, `vault/backlog.md`, `vault/em-andamento.md`
- `vault/decisoes/0019-pyav-compativel-com-app-control.md`, `vault/log/2026-10-31-pyav-app-control.md`
- Ambiente local `.venv` (não versionado).
