---
tipo: decisao
numero: 0018
titulo: Análise em segundo plano com aviso autorizado
status: aceita
data: 2026-10-31
agente: codex
tags: [decisao, fase-2, telegram, seguranca]
---

# 0018 — Análise em segundo plano com aviso autorizado

## Contexto

- Item 16 do [[../backlog|backlog]]: "me chama" quando uma tarefa longa termina.
- O usuário precisa continuar conversando ou encerrar a sessão sem aguardar a análise.
- [[0015-confirmacao-e-telegram]] exige autorização explícita para ações externas.

## Decisão

- Ferramenta `start_background_task` disponível no canal de voz quando Telegram está configurado.
- A ferramenta só cria uma `PendingAction`: ler tarefa e pedir confirmação para **iniciar e enviar resultado ou falha** ao Telegram. O código inicia somente após "yes".
- Essa confirmação vale para o aviso posterior daquela tarefa, mesmo depois do encerramento da sessão de voz; não autoriza outras ações.
- Executor em thread daemon, uma tarefa por vez, sem fila, persistência ou novas dependências.
- O serviço cria um `Assistant` por tarefa, com histórico vazio, relógio e advisor. Sem acesso a arquivos, comandos, web ou ferramentas de envio.
- O pedido deve conter o contexto necessário e o idioma; resultados são dados enviados pelo executor, sem novas chamadas de ferramentas.
- Resultado longo dividido em blocos de até 2000 caracteres, preservando o conteúdo e respeitando o limite do Telegram mesmo com emojis.
- Falha na análise gera aviso; falha de entrega gera log apenas com tipo da exceção, sem repetição automática.
- Encerrar o serviço impede novos trabalhos e suprime avisos ainda não iniciados. Chamadas já em andamento podem terminar; tarefas não são retomadas ao reiniciar.

## Alternativas consideradas

- **Só marcar a próxima resposta para envio** — continuaria bloqueando a conversa enquanto o cérebro pensa.
- **Fila persistente ou executor externo** — complexidade desnecessária nesta versão de usuário único.
- **Aviso sem confirmação** — incompatível com a regra de ações externas.

## Consequências

- Voz, chat e análise têm históricos separados; uma tarefa confirmada sobrevive ao encerramento da sessão, mas depende de o serviço continuar ligado.
- Nesta versão, tarefas são análises de planejamento, escrita, matemática e raciocínio; não executam trabalhos no computador.
- Início pelo Telegram, lembretes agendados, recuperação após reinício e consulta posterior do resultado ficam para outra etapa.
- Testes simulados cobrem confirmação, cancelamento, concorrência, falhas, entrega longa e encerramento. Validação real por voz pendente.

## Status

- aceita

## Data

- 2026-10-31
