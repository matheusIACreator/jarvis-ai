---
tipo: decisao
numero: "0003"
titulo: Tudo nativo no Windows
status: aceita
data: 2026-10-30
agente: claude-code
tags: [decisao, plataforma, windows]
---

# 0003 — Tudo nativo no Windows

## Contexto

- O projeto é centrado em áudio: microfone (palmas, comandos) e alto-falante (música, voz).
- No WSL2, o acesso a microfone e alto-falante é pouco confiável (depende de WSLg/PulseAudio, com latência e falhas).

## Decisão

- Tudo roda nativamente no Windows 11: PowerShell e Python nativo.
- Ambiente virtual local em `.venv`.
- Comandos na documentação escritos para PowerShell.
- Caminhos sempre montados com `pathlib`, nunca com barras invertidas fixas.
- `.gitattributes` com `eol=lf` para evitar reescrita de fim de linha entre agentes.

## Alternativas consideradas

- **WSL2** — ambiente Linux confortável, mas áudio instável e com latência.
- **Híbrido (detector de palmas no Windows + serviço no WSL)** — resolve o microfone para o gatilho, mas cria dois processos, comunicação entre sistemas e ainda deixa STT/TTS com o problema de áudio.
- **Docker** — adiado; mesmo problema de acesso a dispositivos de áudio e complexidade desnecessária para um único usuário.

## Consequências

- Acesso direto e confiável aos dispositivos de áudio.
- Algumas bibliotecas podem ter instalação mais chata no Windows; avaliar antes de adotar.
- Docker pode ser reconsiderado no futuro para partes sem áudio (ex.: servidores MCP).

## Status

- aceita

## Data

- 2026-10-30
