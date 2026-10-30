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

- `status: livre` → nenhuma tarefa em andamento; pegar a próxima do [[00-Indice]].
- `status: ativo` → existe tarefa em andamento; continuar a partir do "Próximo passo".

## Tarefa

- Item 3 do [[backlog]]: captura de microfone em `src/jarvis/trigger/microphone.py`.
- Biblioteca aprovada pelo usuário em 2026-10-30: `sounddevice` (+ `numpy`).
- Plano: `MicrophoneStream` com `sounddevice.InputStream` mono float32 16 kHz, blocos de 512
  amostras (32 ms) numa fila limitada (descarta o bloco mais antigo se encher); iterável.
  Lógica do callback testável sem dispositivo.

## Feito até agora

- Biblioteca aprovada; tarefa marcada como ativa.
- `sounddevice 0.5.6` + `numpy 2.5.4` instalados e no `pyproject.toml`.
- `microphone.py` e `tests/test_microphone.py` prontos; 15 testes passando.
- Captura real de 2 s no microfone Realtek a 16 kHz: OK, sem blocos descartados.

## Próximo passo

- Fechar a sessão (log, índice, backlog, decisão 0009) e começar o item 4 (detector de palmas).

## Arquivos tocados (ainda sem commit)

- `vault/em-andamento.md`
