# Plano inicial — Patinhas

## Objetivo e escopo

Construir uma aplicação web acadêmica, em português, para demonstrar a descoberta e recomendação de cães e gatos para adoção. Os pets são dados fictícios de demonstração, não representam animais, abrigos ou anúncios reais; essa informação deve aparecer claramente na interface.

O fluxo obrigatório é: explorar catálogo → filtrar → abrir detalhes → preencher um questionário curto sem login → ver recomendações com pontuação e motivos → salvar/remover favoritos. O recomendador usa regras locais explicáveis, não IA generativa. Login e chat ficam fora do escopo inicial e só podem ser considerados como melhorias futuras quando todo o fluxo obrigatório estiver funcional e documentado. Não publicar o site sem pedido explícito.

## Implementação e arquitetura

- **Interface:** HTML, CSS e JavaScript sem framework, servida pelo API Gateway. Cartão de pet e indicador de compatibilidade serão componentes reutilizáveis em Web Components simples.
- **API Gateway:** aplicação FastAPI que serve os arquivos da interface, recebe chamadas do navegador, encaminha-as aos microserviços e oferece um endpoint de status para mostrar quais estão em execução.
- **Microserviço Pets:** FastAPI próprio e banco SQLite próprio; fornece listagem, detalhes e filtros. Na primeira inicialização, prepara um conjunto pequeno de registros fictícios.
- **Microserviço Preferências/Favoritos:** FastAPI próprio e banco SQLite próprio; guarda respostas do questionário e favoritos em contexto demonstrativo, sem autenticação.
- **Microserviço Recomendações:** FastAPI próprio; consulta Pets e Preferências por HTTP interno, calcula uma pontuação determinística por atributos compatíveis e retorna pontuação e explicações. Não precisa de banco próprio.
- **Execução:** Python, FastAPI, Uvicorn e HTTPX. Um `run.py` inicia os quatro processos localmente, com o Gateway na porta 3000 e os serviços internos em portas separadas. O SQLite fica em arquivos locais por serviço; nenhum serviço acessa diretamente o banco de outro.
- **Documentação:** FastAPI publica OpenAPI e Swagger UI para cada serviço. O README explicará como executar e acessar `/docs` para o Gateway e para cada microserviço nas portas locais.

## Estrutura prevista

```text
patinhas/
├── plan.md                         # Plano técnico e direção de design
├── TODO.md                         # Requisitos aprovados e estado de conclusão
├── README.md                       # Instalação, execução, arquitetura e demonstração
├── requirements.txt                # Dependências Python
├── run.py                           # Inicialização coordenada dos serviços
├── gateway/
│   └── main.py                     # Interface estática, proxy HTTP e status
├── services/
│   ├── pets/                       # API, lógica e repositório SQLite de pets
│   ├── preferences/                # API, lógica e repositório SQLite de preferências/favoritos
│   └── recommendations/            # API de pontuação e justificativas
├── data/                            # Bancos SQLite gerados em execução; ignorados pelo Git
├── web/
│   ├── index.html
│   ├── css/styles.css
│   └── js/                          # Aplicação e componentes reutilizáveis
├── design/design-system.json       # Brief visual estruturado para a implementação
└── public/manus-routes.json        # Manifesto das rotas web
```

## Direção visual

### Identidade

Estética **editorial lúdica e acolhedora**, usando a ideia pedida pelo usuário de mascote expressiva e pequenos sinais de progresso, mas sem copiar o Duolingo, seus personagens, logotipo ou identidade. A marca será “Patinhas”: próxima, esperançosa e prática.

### Princípios

1. Fazer o próximo passo de adoção parecer simples e seguro.
2. Priorizar fotos/ilustrações expressivas dos pets e informações fáceis de comparar.
3. Usar humor leve e incentivo sem infantilizar o tema ou prometer adoções reais.
4. Manter contraste, navegação responsiva e justificativas visíveis para cada recomendação.

### Paleta e layout

Fundo creme como uma folha quente; verde profundo para navegação e textos; coral-terra como cor proprietária de ação; amarelo-manteiga e verde-sálvia para estados e destaques. O topo usa uma composição assimétrica, com texto e CTA em uma coluna e ilustração original do lado oposto; a área de descoberta tem filtros compactos e cartões de pets com bastante espaço para imagem. Em dispositivos estreitos, filtros e questionário se reorganizam em uma coluna e os cartões permanecem fáceis de percorrer.

### Elementos distintivos e movimento

Uma pequena mascote original (filhote de orelhas caídas, com traços próprios) acompanha estados vazios e o início do questionário; pequenos arcos/pegadas podem funcionar como marcadores de progresso. Cartões têm bordas macias e sombra curta; compatibilidade usa um selo com número e texto explicativo. Animações curtas de entrada e de confirmação (150–220 ms), sem movimento contínuo que distraia; respeitar `prefers-reduced-motion`.

### Tipografia e voz

Títulos com uma serif display arredondada ou de alto contraste, corpo com sans-serif legível e amigável; pilha com fallback de sistema para funcionar sem fontes externas. Hierarquia: título hero amplo, título de seção médio, nome do pet em destaque, metadados pequenos mas legíveis. Voz curta, otimista e honesta. Exemplos: “Vamos achar um companheiro que combine com sua rotina.” e “A Mel combina com você: porte pequeno, energia tranquila.”

### Marca

Wordmark “Patinhas” acompanhado de uma marca original simples de pata/coração, desenhada em SVG/CSS e legível em tamanhos pequenos. Cor proprietária: coral-terra. A mascote é um apoio visual, não substitui sinais de navegação nem informação.

## Referências visuais consultadas

As fontes abaixo servem como inspiração de padrões; não estamos extraindo nem reutilizando código, marca ou imagens desses projetos.

1. [Petfinder — página inicial](https://www.petfinder.com/): categorias para cães e gatos, entrada direta para descoberta, listagem e favoritos.
2. [Adopt a Pet — como filtros ajudam na busca](https://www.adoptapet.com/blog/adoption/how-filters-work): filtros por idade, porte e convivência ajudam a aproximar resultados da rotina da família.
3. [Troakly — Dog Rescue & Adoption Landing Page, Dribbble](https://dribbble.com/shots/26268858-Dog-Rescue-Adoption-Landing-Page-Design-UI-for-Animal-Shelters): referência de composição de landing page, apelo emocional e cores quentes.
4. [HALO LAB — PawHome, Behance](https://www.behance.net/gallery/220657513/PawHome-Pet-Adoption-Platform-UXUI-Branding?locale=en_US): referência de linguagem amigável, hierarquia simples e apresentação orientada a necessidades.

A síntese visual final está em `design/design-system.json`; ela é um briefing próprio em JSON, não uma extração automática das páginas.