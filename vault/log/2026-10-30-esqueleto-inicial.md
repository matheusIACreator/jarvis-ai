---
tipo: log
data: 2026-10-30
agente: claude-code
tarefa: Criar o esqueleto do projeto e o vault de memória compartilhada
tags: [log, fase-0]
---

# 2026-10-30 — Esqueleto inicial

## O que foi feito

- Criada a estrutura do repositório: `AGENTS.md`, `CLAUDE.md`, `README.md`, `.gitignore`, `.gitattributes`, `.env.example`, `pyproject.toml`.
- Criado o pacote `src/jarvis` com os subpacotes vazios: `trigger`, `stt`, `brain`, `tts`, `tools`, `interfaces`.
- Criado o vault em `vault/`: índice, backlog, arquitetura, decisões 0001–0005, modelos e este log.
- Repositório git inicializado na branch `main` com o commit inicial.
- Nenhuma funcionalidade implementada e nenhuma dependência instalada (apenas esqueleto).

## Decisões tomadas

- [[decisoes/0001-cerebro-api-anthropic]]
- [[decisoes/0002-voz-elevenlabs-flash]]
- [[decisoes/0003-tudo-nativo-no-windows]]
- [[decisoes/0004-memoria-compartilhada-obsidian]]
- [[decisoes/0005-primeira-versao-telegram]]

## Problemas encontrados

- Nenhum.

## O que falta / próximo passo

- Configurar o ambiente de desenvolvimento (`.venv`, `pip install -e .`, pytest). Ver [[backlog]] item 1.

## Arquivos principais tocados

- `AGENTS.md`, `CLAUDE.md`, `README.md`, `pyproject.toml`
- `src/jarvis/**/__init__.py`
- `vault/**`
