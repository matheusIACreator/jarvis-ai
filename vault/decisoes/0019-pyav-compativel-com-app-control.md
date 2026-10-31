---
tipo: decisao
numero: 0019
titulo: PyAV compatível com Controle de Aplicativos do Windows
status: aceita
data: 2026-10-31
agente: codex
tags: [decisao, windows, stt, dependencias]
---

# 0019 — PyAV compatível com Controle de Aplicativos do Windows

## Contexto

- Usuário não conseguiu iniciar Jarvis: `ImportError` em `av/bitstream.pyd`, com bloqueio por política de Controle de Aplicativos.
- Reproduzido com Python 3.12.10, faster-whisper 1.2.1 e PyAV 19.0.2.
- Evento 3077 de `Microsoft-Windows-CodeIntegrity/Operational` confirmou o arquivo exato. A mensagem, sozinha, não identifica se a política é Smart App Control ou outra configuração de App Control.
- PyAV é usado tanto pelo Whisper quanto pela música de abertura ([[0012-stt-whisper-small-ingles]]).

## Decisão

- Instalar wheel oficial PyAV 18.0.0 do PyPI e fixar `av==18.0.0; sys_platform == 'win32'` em `pyproject.toml`.
- Não alterar políticas de segurança, criar exceções ou modificar binários.
- Manter diagnóstico e comandos de reparo no README; se outro arquivo for bloqueado, consultar eventos antes de escolher solução.

## Alternativas consideradas

- **Manter 19.0.2** — importação falha nesta máquina; não é problema de configuração de credenciais nem do modelo Whisper.
- **Desativar proteção** — desnecessário: a distribuição oficial 18.0.0 passou com a mesma política.
- **Compilar dependências ou trocar STT** — complexidade desnecessária para corrigir o binário bloqueado.

## Consequências

- Importações reais `av` e `faster_whisper` passaram.
- Whisper `small` em CPU/int8 carregou do cache; VAD com silêncio sintético retornou texto vazio e música MP3 decodificou normalmente.
- `pip check` sem requisitos quebrados; suíte com 141 testes passando.
- Pin limitado ao Windows. Não é uma garantia de liberação em outras máquinas ou políticas; reavaliar ao atualizar PyAV.

## Referências

- [Wheel oficial PyAV 18.0.0 no PyPI](https://pypi.org/project/av/18.0.0/).
- [Microsoft: eventos de integridade de código para diagnóstico](https://learn.microsoft.com/en-us/windows/apps/develop/smart-app-control/test-your-app-with-smart-app-control).

## Status

- aceita

## Data

- 2026-10-31
