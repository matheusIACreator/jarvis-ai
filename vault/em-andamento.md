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

- Item 2 do [[backlog]]: módulo `jarvis.config` que carrega o `.env`.
- Plano: parser próprio de `.env` (sem dependência nova), dataclass `Config` imutável,
  `ConfigError` listando todas as chaves faltando, variáveis do ambiente real têm prioridade
  sobre o `.env`, caminhos relativos resolvidos a partir da raiz do projeto com `pathlib`.
- Obrigatórias na Fase 1: `ANTHROPIC_API_KEY`, `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`.
  Telegram opcional (Fase 2). Valores de exemplo (`your-...`) contam como ausentes.

## Feito até agora

- Protocolo de início lido; tarefa marcada como ativa.

## Próximo passo

- Escrever `src/jarvis/config.py` e `tests/test_config.py`, rodar `pytest`.

## Arquivos tocados (ainda sem commit)

- `vault/em-andamento.md`
