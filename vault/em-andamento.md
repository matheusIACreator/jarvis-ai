---
tipo: em-andamento
data: 2026-10-31
agente: claude-code
status: ativo
tags: [handoff, memoria]
---

# Em andamento

Checkpoint vivo da tarefa atual. Atualizar **durante** a sessão, após cada passo relevante,
para que o outro agente consiga continuar se este ficar sem tokens no meio do trabalho.

- `status: livre` → nenhuma tarefa em andamento; pegar a próxima do [[00-Indice]].
- `status: ativo` → existe tarefa em andamento; continuar a partir do "Próximo passo".

## Tarefa

- Item 7 do [[backlog]]: STT local com faster-whisper.
- Aprovado pelo usuário em 2026-10-31: instalar `faster-whisper`, modelo `small`, **somente inglês** (`en`).
- Plano: `stt/recorder.py` (grava do início da fala até ~0,8 s de silêncio; lógica pura testável),
  `stt/transcriber.py` (`WhisperModel` CPU int8, carregamento preguiçoso), `WHISPER_MODEL` e
  `WHISPER_LANGUAGE` no `jarvis.config`, `scripts/listen.py` para teste manual.
- PyAV (vem com o faster-whisper) decodifica mp3 → item 5 sem biblioteca extra.

## Feito até agora

- Aprovação do usuário; tarefa marcada como ativa.

## Próximo passo

- `pip install faster-whisper`, escrever recorder + transcriber + testes.

## Arquivos tocados (ainda sem commit)

- `vault/em-andamento.md`
