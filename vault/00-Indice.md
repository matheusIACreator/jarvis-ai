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

## Próxima tarefa

- Configurar o ambiente de desenvolvimento: criar a `.venv` com Python 3.11+, instalar o pacote em modo editável (`pip install -e .`), configurar pytest e validar que `import jarvis` funciona no PowerShell.
- Detalhes no [[backlog]].

## Links

### Arquitetura
- [[arquitetura/visao-geral|Visão geral da arquitetura]]

### Decisões
- [[decisoes/0001-cerebro-api-anthropic|0001 — Cérebro na API da Anthropic]]
- [[decisoes/0002-voz-elevenlabs-flash|0002 — Voz com ElevenLabs Flash]]
- [[decisoes/0003-tudo-nativo-no-windows|0003 — Tudo nativo no Windows]]
- [[decisoes/0004-memoria-compartilhada-obsidian|0004 — Memória compartilhada no Obsidian]]
- [[decisoes/0005-primeira-versao-telegram|0005 — Primeira versão com Telegram]]

### Último log
- [[log/2026-10-30-esqueleto-inicial|2026-10-30 — Esqueleto inicial]]

### Modelos
- [[_modelos/modelo-decisao|Modelo de decisão]]
- [[_modelos/modelo-log-sessao|Modelo de log de sessão]]
