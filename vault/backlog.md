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
- [x] 4b. Limiares das palmas validados com palmas reais em 2026-10-31 (padrões mantidos).
- [x] 7b. Limiares de fala validados com a voz real do usuário em 2026-10-31 (2,2 s de áudio, 1,8 s para transcrever, texto exato).
- [x] 5. Áudio de abertura: tocar o arquivo de `STARTUP_AUDIO_PATH` ao disparar o gatilho (sem travar o loop principal).
- [x] 6. Saudação: frase curta falada após a música.
- [x] 7. STT local: faster-whisper transcrevendo o comando (gravação até silêncio, modelo e idioma configuráveis).
- [x] 8. Loop do cérebro: Anthropic SDK com `claude-haiku-5-5`, prompt de sistema com cache, histórico curto, chamada de ferramentas.
- [x] 8b. Cérebro testado na API real pelo usuário em 2026-10-31 (créditos adicionados; ferramenta de data/hora e voz OK).
- [x] 8c. Conferir `cache_read_input_tokens` quando prompt + ferramentas passarem de 512 tokens.
- [x] 9. Interface de ferramentas: contrato único para tools (e servidores MCP quando fizer sentido); primeira tool simples (ex.: data/hora).
- [x] 10a. TTS por streaming HTTP (PCM 24 kHz, voz George) — `src/jarvis/tts/speaker.py`; testado pelo usuário.
- [ ] 10b. Migrar para WebSocket quando o cérebro gerar texto em streaming. Original: TTS por streaming: ElevenLabs `eleven_flash_v2_5` via WebSocket, tocando no alto-falante conforme os chunks chegam.
- [x] 11. Serviço principal: orquestrar gatilho → STT → cérebro → TTS em um único processo (gatilho como thread/task).
- [x] 12. (via advisor, [[decisoes/0014-sonnet-como-advisor]]) Escalonamento para `claude-sonnet-5-5` em tarefas que exigem raciocínio mais profundo.

## Fase 1 — extras

- [x] Palavra de ativação "Hey Jarvis" como alternativa às palmas ([[decisoes/0016-palavra-de-ativacao]]).
- [x] Palmas mais sensíveis (mínimo 0,08) após diagnóstico com palmas reais.

## Fase 2 — Telegram

- [x] 13. Bot do Telegram: enviar mensagem para `TELEGRAM_CHAT_ID` como tool do cérebro.
- [x] 14. Fluxo de confirmação: toda ação externa (enviar mensagem etc.) exige "sim" explícito do usuário antes de executar; máquina de estados testada.
- [ ] 15. Receber mensagens do Telegram como comandos (tratadas como dados, nunca como instruções do sistema).
- [ ] 16. "Me chama": Jarvis avisa pelo Telegram quando uma tarefa longa termina.
