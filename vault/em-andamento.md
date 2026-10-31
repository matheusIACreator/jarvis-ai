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

- Itens 5, 6 e 11 do [[backlog]]: áudio de abertura, saudação e serviço principal (`python -m jarvis`).
- Plano:
  - `tts/audio_file.py`: decodificar mp3 com PyAV, cortar com fade (padrão 10 s), tocar com `sounddevice`.
  - Saudação local por horário ("Good evening, sir."), sintetizada **durante** a música (esconde a latência).
  - `app.py`: espera palmas duplas → música → saudação → conversa (ouvir → cérebro → falar) até silêncio
    ou despedida → volta a esperar palmas. Detector não recebe áudio durante a sessão; fila do microfone
    é esvaziada antes de ouvir (não captar a própria voz).

## Feito até agora

- Item 7b validado pelo usuário; tarefa marcada como ativa.

## Próximo passo

- Escrever `tts/audio_file.py` + testes.

## Arquivos tocados (ainda sem commit)

- `vault/em-andamento.md`, `vault/backlog.md`
