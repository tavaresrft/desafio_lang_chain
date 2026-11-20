# Task 01 — Fundação do projeto

**Agente:** `python-project`
**Dependências:** nenhuma
**Objetivo:** preparar a estrutura de execução e configuração descrita em [`build.md`](build.md).

## Escopo

- Criar `requirements.txt` com LangChain, integração PostgreSQL/pgVector, loaders e provedores, `click`, `python-dotenv` e dependências necessárias.
- Criar `.env.example` documentando provedor, chaves, modelos, URL de conexão e nome da collection sem incluir segredos reais.
- Criar `docker-compose.yml` com PostgreSQL e pgVector, volume persistente e configuração via ambiente.
- Criar a estrutura `src/` e garantir que a execução documentada use `uv` para instalar os pacotes definidos no requirements.
- Definir configuração centralizada compartilhada por ingestão e busca quando isso evitar duplicação.

## Restrições

- Python; usar `uv` como gerenciador e `requirements.txt` como fonte de dependências.
- Não fixar um provedor único: receber provedor e credenciais pelas variáveis de ambiente.
- Não inserir chaves reais no repositório.
- Manter compatibilidade entre dimensões de embedding e collection; tornar a configuração do embedding explícita.

## Critérios de conclusão

- O compose sobe um serviço PostgreSQL com pgVector habilitado.
- Há instruções de configuração sem valores secretos.
- Dependências e variáveis cobrem os provedores escolhidos pelo projeto.
- Os agentes de ingestão e busca conseguem reutilizar as mesmas definições de configuração.

## Entrega

Arquivos de dependências, configuração de ambiente e Docker Compose; registrar decisões que afetem tarefas dependentes.
