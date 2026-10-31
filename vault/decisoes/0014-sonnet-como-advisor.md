---
tipo: decisao
numero: 0014
titulo: Sonnet como advisor e encerramento pela ferramenta
status: aceita
data: 2026-10-31
agente: claude-code
tags: [decisao, cerebro, anthropic, fase-1]
---

# 0014 — Sonnet como advisor e encerramento pela ferramenta

## Contexto

- Item 12 do [[backlog]]: usar `claude-sonnet-5-5` só quando precisar de raciocínio mais profundo
  ([[decisoes/0001-cerebro-api-anthropic]]).
- Teste real: "That's okay, Jarvis. Thank you." não encerrou a sessão (lista fixa de frases).

## Decisão

- Escalonamento pela ferramenta de servidor **advisor** (`advisor_20260301`, beta `advisor-tool-2026-03-01`):
  Haiku 5.5 continua sendo a voz e consulta o Sonnet 5.5 dentro da mesma requisição.
  `max_uses` 1, `max_tokens` 1024, cache do prompt do advisor (5 min). Prompt diz quando consultar.
- `stop_reason: pause_turn` é retomado (servidor ainda trabalhando).
- Ferramenta **final** `end_conversation`: Claude chama ao perceber a despedida; o turno termina sem nova
  chamada à API e a sessão de voz fecha. A lista fixa de despedidas continua como atalho sem custo.
- Frase de espera "One moment, sir." (sintetizada uma vez na inicialização) se a resposta passar de 2 s;
  sempre termina antes da resposta.
- Prompt pede horas como leitura de relógio ("twelve thirty-six a.m."): o modelo se confundiu com
  "twenty-four to one".

## Alternativas consideradas

- **Roteador próprio (classificar e trocar de modelo)** — chamada extra e histórico dividido entre modelos.
- **Ferramenta própria que chama o Sonnet** — reimplementa o que o advisor já faz no servidor.

## Consequências

- Medido em 2026-10-31: pergunta simples ~1,9 s; pergunta de planejamento com advisor 9,5 s (era 13,4 s
  com `max_tokens` 2048). Cache do prompt de sistema funcionando (1515 tokens lidos do cache).
- O conteúdo do advisor vem criptografado (`advisor_redacted_result`); só é reenviado, nunca lido.

## Status

- aceita

## Data

- 2026-10-31
