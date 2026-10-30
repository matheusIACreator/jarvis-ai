---
tipo: backlog
data: 2026-10-30
tags: [backlog, planejamento]
---

# Backlog

Itens em ordem de execução. Marque `[x]` ao concluir e registre no log da sessão.

## Fase 1 — MVP (palmas → música → saudação → comando → resposta)

- [ ] 1. Ambiente de desenvolvimento: `.venv` com Python 3.11+, `pip install -e .`, pytest configurado, `import jarvis` funcionando no PowerShell.
- [ ] 2. Configuração: carregar variáveis do `.env` em um módulo `jarvis.config` (caminhos com `pathlib`, falha clara se faltar chave).
- [ ] 3. Captura de microfone: stream de áudio contínuo do microfone do notebook (escolher biblioteca e pedir aprovação antes de instalar).
- [ ] 4. Detector de palmas duplas: detecção de picos de energia + janela de tempo entre as duas palmas; testes com sinais sintéticos.
- [ ] 5. Áudio de abertura: tocar o arquivo de `STARTUP_AUDIO_PATH` ao disparar o gatilho (sem travar o loop principal).
- [ ] 6. Saudação: frase curta falada após a música.
- [ ] 7. STT local: faster-whisper transcrevendo o comando (gravação até silêncio, modelo e idioma configuráveis).
- [ ] 8. Loop do cérebro: Anthropic SDK com `claude-haiku-5-5`, prompt de sistema com cache, histórico curto, chamada de ferramentas.
- [ ] 9. Interface de ferramentas: contrato único para tools (e servidores MCP quando fizer sentido); primeira tool simples (ex.: data/hora).
- [ ] 10. TTS por streaming: ElevenLabs `eleven_flash_v2_5` via WebSocket, tocando no alto-falante conforme os chunks chegam.
- [ ] 11. Serviço principal: orquestrar gatilho → STT → cérebro → TTS em um único processo (gatilho como thread/task).
- [ ] 12. Escalonamento para `claude-sonnet-5-5` em tarefas que exigem raciocínio mais profundo.

## Fase 2 — Telegram

- [ ] 13. Bot do Telegram: enviar mensagem para `TELEGRAM_CHAT_ID` como tool do cérebro.
- [ ] 14. Fluxo de confirmação: toda ação externa (enviar mensagem etc.) exige "sim" explícito do usuário antes de executar; máquina de estados testada.
- [ ] 15. Receber mensagens do Telegram como comandos (tratadas como dados, nunca como instruções do sistema).
- [ ] 16. "Me chama": Jarvis avisa pelo Telegram quando uma tarefa longa termina.
