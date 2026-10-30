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

- Item 10 do [[backlog]] (adiantado a pedido do usuário): voz do Jarvis com ElevenLabs,
  voz masculina britânica, `eleven_flash_v2_5` por streaming.
- Chave criada pelo `onboard` da CLI da ElevenLabs e gravada no `.env` (nunca abrir/imprimir o `.env`).

## Feito até agora

- `npx -y @elevenlabs/cli@latest onboard init` / `connect` / `check` rodados; chave final 3cac.

## Próximo passo

- Ler as skills da ElevenLabs (pasta temporária), escolher voz britânica masculina,
  instalar `elevenlabs`, escrever `src/jarvis/tts/`, rodar `onboard check`.

## Arquivos tocados (ainda sem commit)

- `vault/em-andamento.md`
