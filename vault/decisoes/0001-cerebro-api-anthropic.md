---
tipo: decisao
numero: "0001"
titulo: Cérebro na API da Anthropic
status: aceita
data: 2026-10-30
agente: claude-code
tags: [decisao, cerebro, anthropic, custo]
---

# 0001 — Cérebro na API da Anthropic

## Contexto

- O Jarvis precisa de um "cérebro" que entenda comandos em linguagem natural, responda rápido e chame ferramentas.
- O loop de voz exige baixa latência; o uso diário exige custo baixo.

## Decisão

- Usar a API da Anthropic com um núcleo próprio e enxuto sobre o SDK oficial.
- Modelo padrão: `claude-haiku-5-5` para o loop de voz (rápido e barato).
- `claude-sonnet-5-5` apenas sob demanda, para tarefas que exigem raciocínio mais profundo.
- Ferramentas expostas como servidores MCP quando for prático.
- Hermes Agent **não** será usado.

## Alternativas consideradas

- **Hermes Agent / frameworks de agente** — mais camadas e dependências do que o necessário para um único usuário.
- **Sonnet como padrão** — melhor raciocínio, mas mais lento e mais caro para respostas curtas de voz.
- **Modelo local** — sem custo por token, mas qualidade e chamada de ferramentas inferiores no hardware do notebook.

## Consequências

- Custo: a maioria das interações usa Haiku; Sonnet só quando justificado.
- Prompt caching no prompt de sistema e nas definições de ferramentas, que são estáveis, reduz custo e latência.
- Respostas curtas (voz) mantêm o consumo de tokens de saída baixo.
- Dependência de internet e de chave de API (`ANTHROPIC_API_KEY` no `.env`).
- Precisamos manter nosso próprio loop de ferramentas (simples, mas é código nosso).

## Status

- aceita

## Data

- 2026-10-30
