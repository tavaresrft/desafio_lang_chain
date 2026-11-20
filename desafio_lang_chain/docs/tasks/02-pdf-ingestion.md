# Task 02 — Ingestão do PDF

**Agente:** `pdf-ingestion`
**Dependências:** [Task 01](01-project-foundation.md)
**Objetivo:** implementar `src/ingest.py` para carregar, dividir, vetorizar e armazenar um PDF.

## Escopo

- Receber o caminho do arquivo PDF como argumento obrigatório da CLI e carregá-lo com `PyPDFLoader`.
- Dividir o conteúdo com `RecursiveCharacterTextSplitter`, chunk de 1000 caracteres e overlap de 150.
- Gerar embeddings através do provedor configurado por ambiente (OpenAI ou Gemini).
- Persistir os chunks e metadados no PostgreSQL/pgVector com `langchain_postgres.PGVector`.
- Tornar a execução repetível sem inserir cópias dos mesmos chunks a cada ingestão, dentro das capacidades da integração escolhida.
- Validar a existência e a extensão `.pdf` do caminho informado; exibir mensagens CLI claras para arquivo ausente, conexão indisponível ou configuração incompleta.

## Critérios de conclusão

- `python src/ingest.py caminho/para/arquivo.pdf` processa o PDF informado e grava vetores na collection configurada.
- Tamanho, overlap, loader, embeddings e armazenamento seguem `build.md`.
- A dimensão do embedding é consistente com o modelo configurado e incompatibilidades são explicadas ao usuário.
- Nenhuma credencial aparece em logs ou no código.

## Entrega

Implementação de ingestão e atualização das instruções de uso necessárias.
