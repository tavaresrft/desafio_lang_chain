# Plano de implementação

Implemente as tarefas na ordem indicada. A especificação de produto e os requisitos mandatórios estão em [`build.md`](build.md); estas tarefas apenas distribuem o trabalho.

| Ordem | Task | Agente | Bloqueada por |
|---|---|---|---|
| 1 | [Fundação do projeto](01-project-foundation.md) | `python-project` | — |
| 2 | [Ingestão do PDF](02-pdf-ingestion.md) | `pdf-ingestion` | 1 |
| 3 | [Busca semântica e chat CLI](03-semantic-search-chat.md) | `semantic-chat` | 1 e 2 |
| 4 | [Integração e documentação](04-documentation-and-integration.md) | `integration-reviewer` | 1, 2 e 3 |

## Coordenação

O coordenador mantém `build.md` como fonte de verdade, distribui cada tarefa ao agente nomeado, passa os arquivos já produzidos como contexto, resolve conflitos de interface (variáveis de ambiente, nomes de collection e configuração de modelos) e aceita a entrega quando todos os critérios de conclusão forem atendidos. Não delegar tarefas dependentes antes de suas dependências estarem disponíveis.

## Pontos externos

- O PDF é um insumo do usuário e pode não existir inicialmente; a ingestão recebe seu caminho como argumento obrigatório. Não inventar conteúdo de demonstração como se fosse o PDF final.
- A chave de provedor deve ser fornecida localmente em ambiente/`.env` e não deve ser commitada.
- Nomes e versões de modelos mudam. Consultar documentação oficial do provedor na implementação, em vez de presumir nomes permanentes.
