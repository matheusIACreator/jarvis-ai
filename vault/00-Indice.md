---
tipo: indice
data: 2026-10-31
atualizado-por: codex
tags: [indice, jarvis]
---

# Índice do Jarvis

## Visão geral

- Assistente de voz pessoal (estilo Homem de Ferro) para um único usuário (Matheus), rodando nativamente no Windows 11.
- Fluxo: palmas duplas → música de abertura → saudação → comando por voz → resposta falada.
- Cérebro na API da Anthropic, voz pela ElevenLabs, transcrição local com faster-whisper.

## Estado atual

- Arquivos versionáveis revisados para commit; frontend integrado ao Git principal, dados privados continuam ignorados. [[log/2026-10-31-git-implementacoes]].

- Ponte do painel corrigida para desconexões HTTP (WinError 10053), sem bloquear estado da voz durante escrita. 172 testes passando; [[log/2026-10-31-dashboard-desconexao]].

- Painel local Next.js/React/shadcn implementado: núcleo animado, chat e consulta de memória. Conversas de voz, web e Telegram persistidas em Markdown privado; [[Memória]] e [[decisoes/0021-painel-e-memoria]]. 164 testes passando.

- [x] Fase 0 — esqueleto do projeto e vault de memória compartilhada ✔
- [x] Fase 1 — MVP: palmas → música → saudação → comando → resposta ✔
- [x] Fase 2 — notificações e "me chama" via bot do Telegram (implementação; novo fluxo aguarda teste real)
- [ ] Fase 3 — e-mail (Gmail) com rascunho + confirmação por voz antes de enviar
- [ ] Fase 4 — ligação telefônica (Twilio + ElevenLabs Agents)
- Fase 1 concluída: ambiente, `jarvis.config`, microfone, detector de palmas, voz ElevenLabs, cérebro, STT e serviço principal (`python -m jarvis`) prontos.
- Sonnet 5.5 como advisor em perguntas difíceis; sessão encerra pela ferramenta `end_conversation`.
- Fase 2 implementada: envio ao Telegram com confirmação por voz, conversa por mensagem e análise em segundo plano com aviso de conclusão.
- "Me chama": após confirmação por voz, uma análise por vez; resultado ou falha no Telegram; sessão de voz pode encerrar; serviço precisa continuar ligado.
- Gatilhos: palmas duplas (mínimo 0,08) ou "Hey Jarvis" (openWakeWord). 160 testes passando.
- Após ativar, sessão permanece aberta durante silêncio; basta voltar a falar. Despedida explícita volta ao gatilho; `SESSION_IDLE_SECONDS=0` (padrão) desativa limite, valor positivo define segundos.
- Confirmação de ações preparada pela ferramenta e falada diretamente pelo código; uma resposta clara confirma. Validade de 60 s separada da escuta. Teste com modelo real e entrega simulada passou, incluindo "Okay, I'll wait" sem encerrar sessão.
- Inicialização corrigida: Controle de Aplicativos bloqueou `av/bitstream.pyd` do PyAV 19.0.2; PyAV 18.0.0 instalado e fixado no Windows, sem alterar a proteção. Importações, Whisper small/int8, VAD e decodificação MP3 validados de verdade ([[decisoes/0019-pyav-compativel-com-app-control]]).
- Música de abertura: "Back in Black" a partir do 6º s, 10 s.
- Testado com palmas reais em 2026-10-31: palmas → música → saudação OK. Conversa completa testada pelo usuário (perguntas seguidas, ferramenta de data, despedida).
- Cérebro: núcleo próprio em `claude-haiku-5-5` (sem Hermes); testado de verdade com voz pelo usuário em 2026-10-31.
- Voz: George (britânico maduro), `eleven_flash_v2_5` em streaming; testada e aprovada pelo usuário.
- Limiares das palmas e configuração local já validados nas sessões anteriores; conteúdo do `.env` não foi lido por Codex nesta sessão.
- Troca entre agentes funcionando: Codex CLI instalado; `scripts/agent.ps1` faz commit pelo Codex.

## Próxima tarefa

- Iniciar serviço e frontend para validar pulsação com voz real e recuperação de conversas; ver [[log/2026-10-31-frontend-memoria]].

- Validar ajuste por voz: pedir análise + aviso → confirmar uma vez → ficar em silêncio → retomar fala sem gatilho e conferir entrega no Telegram. Encerrar explicitamente quando quiser voltar ao gatilho.
- Depois: definir integração Gmail da fase 3 (rascunho + confirmação antes de enviar).
- Ideias para depois: lembretes agendados e interromper a fala (barge-in). Memória de conversas implementada; leitura de outras áreas do vault ainda pode ser ampliada.

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
- [[decisoes/0013-fluxo-da-sessao-de-voz|0013 — Fluxo da sessão de voz]]
- [[decisoes/0014-sonnet-como-advisor|0014 — Sonnet como advisor e encerramento pela ferramenta]]
- [[decisoes/0015-confirmacao-e-telegram|0015 — Confirmação por voz e Telegram]]
- [[decisoes/0016-palavra-de-ativacao|0016 — "Hey Jarvis" e palmas mais sensíveis]]
- [[decisoes/0017-chat-pelo-telegram|0017 — Conversa pelo Telegram em canal separado]]
- [[decisoes/0018-analise-em-segundo-plano|0018 — Análise em segundo plano com aviso autorizado]]
- [[decisoes/0019-pyav-compativel-com-app-control|0019 — PyAV compatível com Controle de Aplicativos]]
- [[decisoes/0020-sessao-continua-e-confirmacao-direta|0020 — Sessão contínua e confirmação direta]]

### Tarefa em andamento
- [[em-andamento]]

### Último log
- [[log/2026-10-31-git-implementacoes|2026-10-31 — Registro das mudanças em Git]]
- [[log/2026-10-31-dashboard-desconexao|2026-10-31 — Desconexão HTTP do painel]]
- [[log/2026-10-31-frontend-memoria|2026-10-31 — Painel e memória Obsidian]]
- [[log/2026-10-31-sessao-continua|2026-10-31 — Sessão contínua durante pausas]]

### Modelos
- [[_modelos/modelo-decisao|Modelo de decisão]]
- [[_modelos/modelo-log-sessao|Modelo de log de sessão]]
