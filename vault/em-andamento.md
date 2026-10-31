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

- (a) Palmas pararam de disparar no serviço (relato do usuário em 2026-10-31). Diagnóstico com gravação de 60 s
  registrando pico, limiar, piso de ruído e estado do detector.
- (b) Gatilho de voz alternativo: **"Hey Jarvis" com openWakeWord** (aprovado pelo usuário; modelo pré-treinado
  `hey_jarvis`; palmas continuam como gatilho principal).

## Feito até agora

- Usuário aprovou openWakeWord; gravação de diagnóstico das palmas iniciada.

## Próximo passo

- Analisar a gravação e corrigir o detector; instalar `openwakeword`, criar `trigger/wake_word.py`, ligar no `app.py`.

## Arquivos tocados (ainda sem commit)

- `vault/em-andamento.md`
