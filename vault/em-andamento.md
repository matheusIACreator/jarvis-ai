---
tipo: em-andamento
data: 2026-10-30
agente: claude-code
status: ativo
tags: [handoff, memoria]
---

# Em andamento

Checkpoint vivo da tarefa atual. Atualizar **durante** a sessão, após cada passo relevante,
para que o outro agente consiga continuar se este ficar sem tokens no meio do trabalho.

- `status: ativo` → nenhuma tarefa em andamento; pegar a próxima do [[00-Indice]].
- `status: ativo` → existe tarefa em andamento; continuar a partir do "Próximo passo".

## Tarefa

- Item 3 do [[backlog]]: captura de microfone em `src/jarvis/trigger/microphone.py`.
- Biblioteca aprovada pelo usuário em 2026-10-30: `sounddevice` (+ `numpy`).
- Plano: `MicrophoneStream` com `sounddevice.InputStream` mono float32 16 kHz, blocos de 512
  amostras (32 ms) numa fila limitada (descarta o bloco mais antigo se encher); iterável.
  Lógica do callback testável sem dispositivo.

## Feito até agora

- Biblioteca aprovada; tarefa marcada como ativa.

## Próximo passo

- `pip install sounddevice numpy`, adicionar ao `pyproject.toml`, escrever módulo e testes.

## Arquivos tocados (ainda sem commit)

- `vault/em-andamento.md`
