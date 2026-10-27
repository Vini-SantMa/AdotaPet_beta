# Patinhas — requisitos e progresso

## 1. Catálogo demonstrativo e transparência
- [x] A aplicação deve mostrar um catálogo demonstrativo de cães e gatos.
- [x] Deve deixar explícito e visível que todos os pets e dados exibidos são fictícios e não representam abrigos ou anúncios reais.
- [x] Deve apresentar uma listagem de pets com dados que permitam comparar suas características.

## 2. Busca e filtros
- [x] O catálogo deve oferecer filtros simples por atributos relevantes, incluindo espécie, porte, idade e nível de energia.
- [x] Os filtros devem atualizar a listagem sem exigir que o usuário conheça o nome de um pet.

## 3. Cartões e detalhes dos pets
- [x] Deve existir um cartão de pet reutilizável na interface, apresentando imagem ilustrativa, nome e características principais.
- [x] O cartão deve oferecer acesso aos detalhes do pet.
- [x] A visualização de detalhes deve apresentar informações de exemplo úteis para avaliar a compatibilidade com uma rotina de adoção.

## 4. Questionário de preferências
- [x] Deve existir um questionário curto, em português e sem login, para recolher critérios do adotante, incluindo espécie, porte, rotina e nível de atividade desejados.
- [x] As respostas devem poder ser usadas pelo serviço de recomendações.

## 5. Recomendações explicáveis
- [x] O sistema deve apresentar recomendações calculadas por regras compreensíveis, com uma pontuação de compatibilidade.
- [x] Cada recomendação deve exibir justificativas claras sobre por que o pet combina com as preferências informadas.
- [x] A pontuação deve ser determinística e explicável, sem depender de IA generativa ou de uma API externa.

## 6. Indicador de compatibilidade
- [x] Deve existir um indicador de compatibilidade reutilizável para apresentar visualmente a pontuação nas recomendações e nos componentes pertinentes.
- [x] O indicador deve continuar legível e acompanhado de texto, não depender apenas da cor.

## 7. Favoritos persistentes
- [x] Sem autenticação, deve ser possível adicionar, remover e consultar pets favoritos no contexto demonstrativo.
- [x] Os favoritos devem persistir em banco SQLite local após reiniciar os serviços.

## 8. Microserviços e API Gateway
- [x] A arquitetura deve conter microserviços independentes de Pets, Preferências/Favoritos e Recomendações, todos acessados pela interface através de um API Gateway.
- [x] O Gateway deve encaminhar chamadas à API correta e mostrar uma lista/estado dos microserviços em execução.
- [x] Cada microserviço deve executar como aplicação FastAPI independente; nenhum serviço deve acessar diretamente o banco de dados de outro.

## 9. APIs, persistência e tecnologia
- [x] As APIs de cada microserviço devem ser documentadas com OpenAPI/Swagger UI.
- [x] O microserviço Pets deve persistir seus dados em SQLite; o microserviço Preferências/Favoritos deve persistir suas respostas e favoritos em SQLite; Recomendações pode permanecer sem banco próprio.
- [x] O sistema deve usar Python/FastAPI, SQLite e uma interface HTML/CSS/JavaScript simples.
- [x] O README deve explicar passo a passo a instalação, execução local, portas, documentação das APIs e funcionamento da demonstração acadêmica.

## 10. Interface e componentes reutilizáveis
- [x] A interface deve usar português, ser visualmente acolhedora, apresentar navegação clara e adaptar-se a telas estreitas.
- [x] Deve incluir componentes reutilizáveis de cartão de pet e indicador de compatibilidade.
- [x] A direção deve usar mascote original e tom positivo, sem copiar personagens, nome, logotipo ou identidade visual do Duolingo.

## 11. Manifesto e entrega
- [x] Deve existir `public/manus-routes.json` com as rotas de páginas existentes, sincronizado com o código.
- [x] O projeto não deve ser publicado sem pedido explícito do usuário.

## 12. Relatório conforme o enunciado do professor
- [x] O relatório deve declarar o projeto, a metodologia ágil escolhida, as técnicas de reuso e descrever o desenvolvimento segundo essas escolhas; incluir Product Backlog e Sprint Backlog de cada Sprint.
- [x] Deve apresentar a arquitetura de microserviços, o API Gateway com código documentado e a especificação com código documentado de cada microserviço e componente de software.
- [x] Deve especificar e documentar o código do sistema de recomendação e incluir uma tela que mostre todos os microserviços em execução.
- [x] Deve informar as tecnologias, linguagens e bancos usados por microserviço; explicar passo a passo as telas e destacar a arquitetura na interface principal; incluir referências bibliográficas.
- [ ] A capa do relatório deve receber o link real do repositório GitHub depois que o projeto estiver enviado para a conta autorizada.

## 13. Itens finais que dependem do estudante
- [ ] O código completo deve estar funcionando no GitHub, acompanhado das instruções para executar o sistema; o endereço do repositório também deve aparecer na capa do relatório.
- [ ] Preencher na capa nome do discente, instituição/curso e docente. Esses dados ainda não foram informados.
