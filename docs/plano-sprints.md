# Planejamento acadêmico — Product Backlog e Sprint Backlog

**Metodologia escolhida:** Scrum simplificado, com backlog ordenado, ciclos curtos, incrementos demonstráveis e revisão das prioridades ao fim de cada sprint. Como o calendário e as aulas são limitados, as sprints são organizadas por entregas pequenas, não por cerimônias extensas. O registro não afirma que reuniões ou eventos não realizados tenham ocorrido.

## Product Backlog ordenado

**PB1 — Catálogo e transparência:** mostrar pets de demonstração, características comparáveis e aviso de que os dados são fictícios.

**PB2 — Busca:** filtrar catálogo por espécie, porte, idade e energia.

**PB3 — Perfil:** abrir detalhes do pet e apresentar história e condições de convivência.

**PB4 — Preferências:** preencher questionário sem conta e salvar critérios úteis para o match.

**PB5 — Recomendação:** ordenar pets por compatibilidade e explicar os fatores de cada nota.

**PB6 — Favoritos:** salvar, consultar e remover pets favoritos com persistência.

**PB7 — Microserviços e Gateway:** executar três APIs independentes atrás de uma entrada pública e apresentar health checks.

**PB8 — Componentes reutilizáveis:** implementar cartão de pet e indicador de compatibilidade reutilizáveis.

**PB9 — Documentação técnica:** publicar OpenAPI/Swagger, diagrama de arquitetura, regras do recomendador e README de execução.

**PB10 — Relatório e demonstração:** inserir telas, tecnologias, passos de uso, backlog e referências bibliográficas.

**PB11 — Distribuição:** sincronizar código em um repositório GitHub apropriado, com instruções de execução e link na capa.

## Sprint 1 — recorte e arquitetura, 27–29 de outubro

**Objetivo:** fechar um problema pequeno, modelar fronteiras de serviço e escolher dados demonstrativos seguros.

**Itens:** PB1 (modelo dos registros fictícios e aviso), PB7 (topologia Gateway/3 serviços), PB8 (definição dos dois componentes), PB9 (estrutura e rotas planejadas).

**Incremento já demonstrado em 27 de outubro:** estrutura inicial, APIs FastAPI, configuração SQLite por proprietário, Gateway e manifesto de rotas. O primeiro incremento funcional já foi executado antes do término do intervalo; o restante da sprint é refinamento da modelagem e documentação.

## Sprint 2 — fluxo funcional, 30 de outubro–2 de novembro

**Objetivo:** concluir e demonstrar o caminho principal de descoberta e compatibilidade.

**Itens:** PB1, PB2, PB3, PB4 e PB5; preservar justificativas de recomendação e os limites de escopo. Testar casos de espécie/porte incompatíveis, filtros sem resultados e ausência de pets.

## Sprint 3 — estado, reutilização e integração, 3–5 de novembro

**Objetivo:** estabilizar dados, componentes e evidências dos serviços.

**Itens:** PB6, PB7, PB8 e PB9; verificar persistência após reiniciar processos, rotas do Gateway, saúde independente de cada serviço e comportamento móvel.

## Sprint 4 — relatório e entrega, 6–9 de novembro

**Objetivo:** tornar o trabalho reprodutível e apresentável.

**Itens:** PB9, PB10 e PB11; executar a suíte de testes, revisar o roteiro de tela, preencher dados de identificação acadêmica, salvar o código no GitHub e colocar o link do repositório na capa antes da entrega de 9 de novembro.

## Reuso de software observado

A arquitetura usa microserviços como unidades independentes e um API Gateway para consolidar acesso. `PetCard` e `MatchScore` são componentes visuais reutilizados no catálogo, nas recomendações e nos favoritos. APIs FastAPI geram documentação OpenAPI/Swagger. O SQLite é isolado por serviço para evitar leitura direta do banco de outro proprietário. As bibliotecas utilizadas são FastAPI, Uvicorn e HTTPX; não foram copiados templates de adoção nem código das páginas consultadas.
