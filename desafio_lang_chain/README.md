# Busca semântica de PDF com LangChain e pgVector

Aplicação de linha de comando para ingerir um PDF no PostgreSQL com pgVector e responder perguntas com base somente nos trechos recuperados.

## Índice

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Escolha dos modelos](#escolha-dos-modelos)
- [Executar](#executar)
- [Como as respostas são produzidas](#como-as-respostas-são-produzidas)
- [Trocar o modelo de embeddings](#trocar-o-modelo-de-embeddings)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Limitações conhecidas](#limitações-conhecidas)

## Pré-requisitos

- Python 3.10 ou superior e [uv](https://docs.astral.sh/uv/).
- Docker com Docker Compose.
- Uma chave de API da OpenAI ou do Gemini.
- O caminho para o arquivo PDF a ser consultado.

## Instalação

Clone o repositório e, na pasta do projeto, crie e ative o ambiente virtual:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

No Windows PowerShell, ative com `.venv\Scripts\Activate.ps1`.

## Configuração

Copie o arquivo de exemplo e edite `.env`:

```bash
cp .env.example .env
```

Defina `LLM_PROVIDER` como `openai` ou `gemini` e preencha somente a chave correspondente (`OPENAI_API_KEY` ou `GEMINI_API_KEY`). Ajuste, se necessário, os modelos de chat e embedding e `DATABASE_URL`. `.env` está no `.gitignore`; não coloque chaves em arquivos versionados ou logs.

O Docker Compose lê também as variáveis `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` e `POSTGRES_PORT`. A URL de conexão usada pelo app deve apontar para o banco do Compose (por padrão `postgresql+psycopg://langchain:langchain@localhost:5432/langchain`).

## Escolha dos modelos

Os nomes e a disponibilidade dos modelos mudam. Consulte a documentação oficial no momento da configuração e selecione modelos compatíveis com seu acesso:

- OpenAI: [modelos disponíveis](https://platform.openai.com/docs/models) e [embeddings](https://platform.openai.com/docs/guides/embeddings).
- Google: [modelos Gemini](https://ai.google.dev/gemini-api/docs/models) e [embeddings Gemini](https://ai.google.dev/gemini-api/docs/embeddings).

O `.env.example` traz nomes ilustrativos para facilitar a configuração; confirme que ainda estão disponíveis para sua conta antes de usar.

## Executar

Suba o banco:

```bash
docker compose up -d
```

Inicie a ingestão e depois o chat:

```bash
python src/ingest.py caminho/para/arquivo.pdf
python src/chat.py
```

A ingestão recebe como argumento obrigatório o caminho do PDF. O caminho pode ser relativo à pasta do projeto ou absoluto; coloque-o entre aspas se contiver espaços. Por exemplo: `python src/ingest.py "./meus documentos/relatorio.pdf"`. O script usa `PyPDFLoader` e divide o texto em trechos de 1000 caracteres com sobreposição de 150. O processo recria a collection configurada em cada execução para substituir os dados anteriores sem deixar trechos antigos.

No chat, faça perguntas sucessivas e digite `sair` para encerrar.

## Como as respostas são produzidas

Para cada pergunta, a aplicação busca até 10 trechos na collection com os mesmos embeddings e configuração usados na ingestão. A LLM recebe esses trechos como contexto e a instrução de não usar conhecimento externo. Quando não há nenhum trecho, a aplicação retorna diretamente `Não tenho informações necessárias para responder sua pergunta.`

A CLI exibe somente o texto da resposta. Blocos de conteúdo estruturado e metadados do provedor, como `extras` ou assinaturas, são descartados.

## Trocar o modelo de embeddings

Os modelos podem gerar vetores com dimensões diferentes. Alterar o embedding depois de ingerir dados pode causar incompatibilidade com a collection. Apague/recrie a collection ou o volume do banco e ingira o PDF novamente. O comando de ingestão recria a collection selecionada antes de gravar os chunks.

## Estrutura do projeto

```text
docker-compose.yml
requirements.txt
.env.example
src/
  config.py
  ingest.py
  search.py
  chat.py
# PDF informado pelo usuário na linha de comando; não incluído no repositório
```

## Limitações conhecidas

O caminho para o PDF e as chaves de API são entradas que precisam ser fornecidas pelo usuário. Sem um arquivo PDF acessível no caminho informado, não é possível executar uma ingestão real. A aplicação depende de acesso ao provedor escolhido e ao serviço PostgreSQL para completar as operações.
