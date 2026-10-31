---
tipo: decisao
numero: 0020
titulo: Sessão contínua durante pausas e confirmação direta da ferramenta
status: aceita
data: 2026-10-31
agente: codex
tags: [decisao, voz, confirmacao, fase-2]
---

# 0020 — Sessão contínua durante pausas e confirmação direta da ferramenta

## Contexto

- Usuário confirmou que a inicialização voltou a funcionar, mas relatou incômodo com reativação após silêncio enquanto esperava uma tarefa.
- O gravador encerrava a sessão se ninguém começasse a falar em 5 s ([[0013-fluxo-da-sessao-de-voz]]).
- Log real mostrou três perguntas antes do início: o modelo pode descrever uma ação sem preparar a ferramenta; a frase "Yes, start it and send the result" também não estava na lista de afirmações simples.

## Decisão

- Serviço escuta sem tempo limite por padrão após ativação; despedidas explícitas retornam ao gatilho. Sem repetir música ou saudação entre pausas.
- `SESSION_IDLE_SECONDS=0` ou ausente significa sem limite; valor positivo configura retorno ao gatilho por silêncio. Valores negativos ou não finitos são rejeitados.
- Scripts de captura avulsa mantêm os 5 s originais; somente o serviço passa o novo tempo de escuta.
- Áudio sem texto reconhecido volta à captura, sem encerrar a sessão. Silêncio não chama Whisper nem Anthropic.
- Prompt e ferramenta de encerramento distinguem espera de despedida: "Okay, I'll wait" não encerra.
- Ferramentas de envio ao Telegram e tarefa em segundo plano retornam pergunta de confirmação pronta, após registrar `PendingAction`, com `reply_directly` no contrato de ferramentas.
- `Assistant` usa o resultado direto somente em sucesso; erros voltam ao modelo. Perguntas registradas não passam por mais uma rodada de reformulação do modelo.
- Prompt exige preparar a ferramenta antes de pedir autorização; nenhuma tarefa inicia só pela resposta textual do modelo.
- `ConfirmationGate` aceita afirmações simples adicionais, incluindo "Yes, start it and send the result" e "sim"; frases com ressalvas continuam sem autorizar.
- Ação pendente não pode ser substituída enquanto ainda válida. Confirmação expira em 60 s por relógio monotônico, mesmo com sessão aberta; resposta tardia não executa nada.

## Alternativas consideradas

- **Aumentar apenas de 5 para 30 s** — continuaria exigindo reativação durante tarefas ou pausas maiores.
- **Deixar o modelo perguntar e preparar depois do sim** — permite confirmação de ação que ainda não existe no código.
- **Manter autorização pendente indefinidamente** — um "yes" tardio poderia executar uma ação antiga.

## Consequências

- Usuário pode retomar fala depois de esperar o Telegram, até pedir despedida. Ctrl+C encerra todo o serviço e pode impedir a entrega de trabalho incompleto.
- Microfone permanece capturando na sessão ativa; barge-in durante a fala do Jarvis continua fora do escopo.
- 160 testes passaram, incluindo captura depois de 30 s sintéticos de silêncio, configuração, aprovação única e expiração.
- Teste com Anthropic real preparou a tarefa antes da pergunta, iniciou com uma aprovação e não encerrou com "Okay, I'll wait". Trabalho e entrega foram simulados, sem Telegram real.

## Status

- aceita; atualiza o comportamento de silêncio de [[0013-fluxo-da-sessao-de-voz]] e a apresentação/validade da confirmação de [[0015-confirmacao-e-telegram]].

## Data

- 2026-10-31
