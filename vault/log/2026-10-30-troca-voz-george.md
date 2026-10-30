---
tipo: log
data: 2026-10-30
agente: claude-code
tarefa: Ajustar a voz do Jarvis (mais velha)
tags: [log, fase-1, tts, elevenlabs]
---

# 2026-10-30 — Troca da voz para George

## O que foi feito

- Teste com Daniel tocado; usuário gostou, mas achou jovem demais.
- Buscadas vozes britânicas masculinas mais velhas na biblioteca da ElevenLabs; usuário escolheu Oliver.
- Oliver falhou: chave sem permissão `voices_write` e plano gratuito não usa vozes da biblioteca pela API (402).
- Padrão trocado para **George** (`JBFqnCBsd6RMkjVDRZzb`); teste tocado com sucesso. 28 testes passando.

## Decisões tomadas

- [[decisoes/0010-voz-daniel-e-streaming-http]] atualizada (voz George).

## Problemas encontrados

- Vozes da biblioteca exigem plano Creator ou US$ 5 em créditos.

## O que falta / próximo passo

- Usuário decidir o harness: núcleo próprio (recomendado, itens 8–9) ou Hermes Agent.
- Se o usuário assinar plano pago, dá para trocar para Oliver (`L1aJrPa7pLJEyYlh3Ilq`).

## Arquivos principais tocados

- `src/jarvis/config.py`, `.env.example`
- `vault/decisoes/0010-voz-daniel-e-streaming-http.md`, `vault/00-Indice.md`, `vault/backlog.md`
