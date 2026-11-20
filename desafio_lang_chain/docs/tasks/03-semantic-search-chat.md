# Task 03 — Busca semântica e chat CLI

**Agente:** `semantic-chat`
**Dependências:** [Task 01](01-project-foundation.md), [Task 02](02-pdf-ingestion.md)
**Objetivo:** implementar recuperação vetorial e interação conversacional no terminal.

## Escopo

- Criar `src/search.py` para consultar a collection pgVector com os mesmos embeddings/modelo usados na ingestão.
- Recuperar os 10 resultados mais relevantes (`similarity_search_with_score`, `k=10`).
- Criar `src/chat.py` com interface `click`, prompt de pergunta e resposta, e saída legível.
- Chamar a LLM do provedor selecionado por ambiente, suportando OpenAI e Gemini conforme configuração disponível.
- Usar o prompt de `build.md` como contrato: responder exclusivamente com evidência do contexto; quando ausente, retornar exatamente `Não tenho informações necessárias para responder sua pergunta.`
- Tratar collection vazia, conexão/configuração inválida e erros do provedor com mensagens úteis.
- Exibir somente o texto dos blocos de resposta da LLM, descartando metadados do provedor (por exemplo, `extras`, assinaturas e qualificações estruturais).

## Critérios de conclusão

- O fluxo da pergunta vetorializa, recupera até 10 trechos, monta o contexto e chama a LLM.
- A resposta de insuficiência permanece exatamente igual à definida na especificação.
- Os modelos e credenciais vêm das variáveis de ambiente e são consistentes com ingestão.
- A CLI informa como sair e permite fazer perguntas sucessivas até o usuário encerrar.
- A saída `RESPOSTA:` contém apenas o texto da resposta, sem serialização de blocos ou metadados do provedor.

## Entrega

`src/search.py`, `src/chat.py` e quaisquer ajustes pequenos de integração necessários, relatados ao coordenador.
