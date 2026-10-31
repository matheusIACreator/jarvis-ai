---
tipo: backlog
data: 2026-10-30
tags: [backlog, planejamento]
---

# Backlog

Itens em ordem de execução. Marque `[x]` ao concluir e registre no log da sessão.

## Revisão documental

- [x] Resumo do estado do projeto por Codex em 2026-10-30; pendências técnicas mantidas conforme [[00-Indice]] e [[log/2026-10-30-verificacao-estado]].
- [x] Registrar em commit as alterações desta revisão (feito por claude-code; `scripts/agent.ps1` agora faz o commit pelo Codex).

## Infra dos agentes

- [x] Checkpoint vivo em `em-andamento.md` e protocolo de troca no `AGENTS.md`.
- [x] Script `scripts/agent.ps1` com fallback Claude Code → Codex.
- [x] Instalar o Codex CLI e fazer login (`codex-cli 0.166.0`).
- [ ] Observar um fallback real Claude → Codex por limite de uso e ajustar a detecção se necessário.

## Fase 1 — MVP (palmas → música → saudação → comando → resposta)

- [x] 1. Ambiente de desenvolvimento: `.venv` com Python 3.12, `pip install -e ".[dev]"`, pytest configurado, `import jarvis` funcionando no PowerShell.
- [x] 2. Configuração: carregar variáveis do `.env` em um módulo `jarvis.config` (caminhos com `pathlib`, falha clara se faltar chave).
- [x] 3. Captura de microfone: stream de áudio contínuo do microfone do notebook (escolher biblioteca e pedir aprovação antes de instalar).
- [x] 4. Detector de palmas duplas: detecção de picos de energia + janela de tempo entre as duas palmas; testes com sinais sintéticos.
- [ ] 4b. Validar limiares das palmas com palmas reais (`scripts/clap_monitor.py`) — precisa do usuário.
- [ ] 5. Áudio de abertura: tocar o arquivo de `STARTUP_AUDIO_PATH` ao disparar o gatilho (sem travar o loop principal).
- [ ] 6. Saudação: frase curta falada após a música.
- [ ] 7. STT local: faster-whisper transcrevendo o comando (gravação até silêncio, modelo e idioma configuráveis).
- [x] 8. Loop do cérebro: Anthropic SDK com `claude-haiku-5-5`, prompt de sistema com cache, histórico curto, chamada de ferramentas.
- [ ] 8b. Testar o cérebro na API real (conta sem créditos em 2026-10-31) e conferir o cache.
- [x] 9. Interface de ferramentas: contrato único para tools (e servidores MCP quando fizer sentido); primeira tool simples (ex.: data/hora).
- [x] 10a. TTS por streaming HTTP (PCM 24 kHz, voz George) — `src/jarvis/tts/speaker.py`; testado pelo usuário.
- [ ] 10b. Migrar para WebSocket quando o cérebro gerar texto em streaming. Original: TTS por streaming: ElevenLabs `eleven_flash_v2_5` via WebSocket, tocando no alto-falante conforme os chunks chegam.
- [ ] 11. Serviço principal: orquestrar gatilho → STT → cérebro → TTS em um único processo (gatilho como thread/task).
- [ ] 12. Escalonamento para `claude-sonnet-5-5` em tarefas que exigem raciocínio mais profundo.

## Fase 2 — Telegram

- [ ] 13. Bot do Telegram: enviar mensagem para `TELEGRAM_CHAT_ID` como tool do cérebro.
- [ ] 14. Fluxo de confirmação: toda ação externa (enviar mensagem etc.) exige "sim" explícito do usuário antes de executar; máquina de estados testada.
- [ ] 15. Receber mensagens do Telegram como comandos (tratadas como dados, nunca como instruções do sistema).
- [ ] 16. "Me chama": Jarvis avisa pelo Telegram quando uma tarefa longa termina.
