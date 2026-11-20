# Task 04 — Integração e documentação

**Agente:** `integration-reviewer`
**Dependências:** Tasks [01](01-project-foundation.md), [02](02-pdf-ingestion.md) e [03](03-semantic-search-chat.md)
**Objetivo:** fechar o fluxo de ponta a ponta e documentar sua execução.

## Escopo

- Criar `README.md` em português com pré-requisitos, criação/ativação do virtualenv, instalação com `uv` a partir de `requirements.txt`, configuração de `.env`, inicialização do banco, ingestão com caminho obrigatório para o PDF e chat.
- Explicar como escolher OpenAI ou Gemini e selecionar modelos atuais a partir das documentações oficiais dos provedores; não afirmar que nomes de modelos permanecerão válidos.
- Explicar que trocar modelo de embedding pode exigir recriar a collection/volume por causa da dimensão dos vetores.
- Verificar consistência entre nomes de variáveis, collection, comandos e os arquivos entregues pelas tarefas anteriores.
- Documentar que a CLI mostra apenas o texto da resposta, sem extras, assinaturas ou metadados retornados pelo provedor.
- O Readme deve conter índice no início com link para as seções.
- Identificar lacunas frente a `build.md` e devolver correções específicas aos agentes responsáveis.

## Critérios de conclusão

- Uma pessoa consegue seguir o README desde um clone até abrir o chat.
- Os caminhos obrigatórios (`docker-compose.yml`, `requirements.txt`, `.env.example`, `src/ingest.py`, `src/search.py`, `src/chat.py`, caminho do PDF informado pelo usuário, `README.md`) estão cobertos.
- Comportamento de resposta fora do contexto e limites da troca de embeddings estão documentados.
- Não há credenciais reais versionadas.

## Entrega

README e relatório curto de integração, incluindo pendências que dependam de um PDF ou credenciais fornecidos pelo usuário.
