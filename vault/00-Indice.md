---
tipo: indice
data: 2026-10-30
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
- Fase 1 em andamento: ambiente, `jarvis.config`, microfone, detector de palmas e voz ElevenLabs prontos (28 testes passando).
- Voz: Daniel (britânico), `eleven_flash_v2_5` em streaming; chave no `.env`. Falta ouvir o teste (`scripts/say.py`).
- Limiares das palmas ainda não validados com palmas reais (`scripts/clap_monitor.py`).
- Falta o usuário criar o `.env` a partir do `.env.example`.
- Troca entre agentes funcionando: Codex CLI instalado; `scripts/agent.ps1` faz commit pelo Codex.

## Próxima tarefa

- Item 5 do [[backlog]]: tocar o áudio de abertura. Antes de instalar, pedir aprovação do usuário para a biblioteca de mp3.

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
- [[decisoes/0010-voz-daniel-e-streaming-http|0010 — Voz Daniel e streaming HTTP em PCM]]

### Tarefa em andamento
- [[em-andamento]]

### Último log
- [[log/2026-10-30-voz-elevenlabs|2026-10-30 — Voz com ElevenLabs]]

### Modelos
- [[_modelos/modelo-decisao|Modelo de decisão]]
- [[_modelos/modelo-log-sessao|Modelo de log de sessão]]
