---
tipo: indice
data: 2026-10-31
atualizado-por: claude-code
tags: [indice, jarvis]
---

# Índice do Jarvis

## Visão geral

- Assistente de voz pessoal (estilo Homem de Ferro) para um único usuário (Matheus), rodando nativamente no Windows 11.
- Fluxo: palmas duplas → música de abertura → saudação → comando por voz → resposta falada.
- Cérebro na API da Anthropic, voz pela ElevenLabs, transcrição local com faster-whisper.

## Estado atual

- [x] Fase 0 — esqueleto do projeto e vault de memória compartilhada ✔
- [ ] Fase 1 — MVP: palmas → música → saudação → comando → resposta
- [ ] Fase 2 — notificações e "me chama" via bot do Telegram
- [ ] Fase 3 — e-mail (Gmail) com rascunho + confirmação por voz antes de enviar
- [ ] Fase 4 — ligação telefônica (Twilio + ElevenLabs Agents)
- Fase 1 em andamento: ambiente, `jarvis.config`, microfone, detector de palmas, voz ElevenLabs, cérebro e STT (faster-whisper small, inglês) prontos (49 testes passando).
- Cérebro: núcleo próprio em `claude-haiku-5-5` (sem Hermes); testado de verdade com voz pelo usuário em 2026-10-31.
- Voz: George (britânico maduro), `eleven_flash_v2_5` em streaming; testada e aprovada pelo usuário.
- Limiares das palmas ainda não validados com palmas reais (`scripts/clap_monitor.py`).
- Falta o usuário criar o `.env` a partir do `.env.example`.
- Troca entre agentes funcionando: Codex CLI instalado; `scripts/agent.ps1` faz commit pelo Codex.

## Próxima tarefa

- Item 5 do [[backlog]]: tocar o áudio de abertura (PyAV decodifica o mp3, `sounddevice` toca; sem dependência nova).
- Depois: item 6 (saudação) e item 11 (serviço principal: palmas → música → saudação → ouvir → cérebro → voz).

## Links

### Arquitetura
- [[arquitetura/visao-geral|Visão geral da arquitetura]]

### Decisões
- [[decisoes/0001-cerebro-api-anthropic|0001 — Cérebro na API da Anthropic]]
- [[decisoes/0002-voz-elevenlabs-flash|0002 — Voz com ElevenLabs Flash]]
- [[decisoes/0003-tudo-nativo-no-windows|0003 — Tudo nativo no Windows]]
- [[decisoes/0004-memoria-compartilhada-obsidian|0004 — Memória compartilhada no Obsidian]]
- [[decisoes/0005-primeira-versao-telegram|0005 — Primeira versão com Telegram]]
- [[decisoes/0006-troca-entre-agentes|0006 — Troca entre agentes]]
- [[decisoes/0007-python-3-12|0007 — Python 3.12]]
- [[decisoes/0008-config-sem-dependencia|0008 — Configuração sem dependência externa]]
- [[decisoes/0009-audio-sounddevice-e-palmas-por-pico|0009 — Áudio com sounddevice e palmas por pico]]
- [[decisoes/0010-voz-daniel-e-streaming-http|0010 — Voz George e streaming HTTP em PCM]]
- [[decisoes/0011-nucleo-proprio-do-cerebro|0011 — Núcleo próprio do cérebro]]
- [[decisoes/0012-stt-whisper-small-ingles|0012 — STT com faster-whisper small, só inglês]]

### Tarefa em andamento
- [[em-andamento]]

### Último log
- [[log/2026-10-31-stt-whisper|2026-10-31 — STT com faster-whisper]]

### Modelos
- [[_modelos/modelo-decisao|Modelo de decisão]]
- [[_modelos/modelo-log-sessao|Modelo de log de sessão]]
