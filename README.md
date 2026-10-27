# Patinhas — protótipo acadêmico

O Patinhas demonstra um catálogo de cães e gatos fictícios, filtros, favoritos e recomendações explicáveis. **Os pets, fotos e informações apresentados são dados de demonstração e não são anúncios reais de adoção.**

## Tecnologias

Python 3.10 ou superior, FastAPI, Uvicorn, HTTPX, SQLite e HTML/CSS/JavaScript sem framework.

## Executar localmente

1. Crie e ative um ambiente virtual, se desejar: `python -m venv .venv`.
2. Instale as dependências: `python -m pip install -r requirements.txt`.
3. Inicie os quatro processos: `python run.py`.
4. Abra `http://127.0.0.1:3000` no navegador. O API Gateway serve a interface e recebe as chamadas do navegador.
5. Para encerrar, pressione `Ctrl+C` no terminal.

O script inicia os microserviços Pets (8001), Preferências/Favoritos (8002) e Recomendações (8003) em portas internas, além do Gateway na porta 3000. O Gateway consulta o estado dos três serviços e apresenta os links da documentação na tela. Os bancos SQLite são criados em `data/` na primeira execução; o conteúdo de demonstração é inserido automaticamente e os bancos são ignorados pelo Git. Em outro ambiente, a aplicação pode usar a variável `PORT` para escolher a porta pública do Gateway.

## Documentação das APIs

- Gateway: `http://127.0.0.1:3000/docs`.
- Pets: `http://127.0.0.1:8001/docs`.
- Preferências/Favoritos: `http://127.0.0.1:8002/docs`.
- Recomendações: `http://127.0.0.1:8003/docs`.

Na interface, os links de documentação dos microserviços também podem ser abertos pelo painel “Por trás das Patinhas”, por meio do proxy de documentação do Gateway.

## Arquitetura

```text
Navegador
   │ HTTP
   ▼
API Gateway :3000 ── serve a interface e roteia as APIs
   ├── Pets :8001 ── SQLite próprio: data/pets.sqlite3
   ├── Preferências/Favoritos :8002 ── SQLite próprio: data/preferences.sqlite3
   └── Recomendações :8003 ── consulta Pets e Preferências por HTTP
```

Nenhum serviço lê o banco de outro microserviço. O Gateway é a única entrada da interface. Recomendações consulta os serviços de Pets e Preferências por HTTP interno. Cada aplicação FastAPI fornece OpenAPI e Swagger UI.

## Regras de recomendação

A pontuação é uma regra determinística sobre 100 pontos: espécie (25), porte (20), nível de atividade (até 30), compatibilidade com o tipo de moradia (15) e convivência com crianças quando informada (10). Para atividade, uma combinação exata vale 30; diferença de um nível vale 19; diferença de dois vale 8. Preferências abertas de espécie ou porte recebem pontuação integral naquele critério. O resultado lista os motivos junto da pontuação; não usa um modelo de IA.

## Rotas principais do Gateway

- `GET /api/pets` aceita `species`, `size`, `age` e `energy` como filtros.
- `GET /api/pets/{id}` retorna detalhes de um pet.
- `GET` e `PUT /api/preferences?visitor_id=demo` consultam/salvam o questionário.
- `GET /api/favorites?visitor_id=demo`, `PUT /api/favorites/{id}` e `DELETE /api/favorites/{id}` consultam, adicionam e removem favoritos.
- `GET /api/recommendations?visitor_id=demo` retorna pontuações e justificativas.
- `GET /api/status` mostra quais microserviços respondem ao health check.

O identificador `demo` evita cadastro e senha neste protótipo. A aplicação serve a mesma demonstração local para quem estiver usando o ambiente.

As ilustrações são assets gerenciados do projeto e aparecem no Preview da plataforma. Fora do Manus, um clone local ainda executa as APIs; se os endereços de armazenamento não estiverem disponíveis, os cartões mostram um fallback tipográfico até que sejam substituídos por imagens locais.

## Testes automatizados

Com as dependências instaladas, execute `python -m unittest discover -s tests -v`. A suíte cobre regras e justificativas do recomendador, filtros e 404 do catálogo, preferências/favoritos após reiniciar o serviço e o encaminhamento de filtros pelo Gateway.

## Limitações intencionais

Não há login, chat, integração com abrigos, geolocalização ou anúncios reais. Os favoritos e preferências são persistidos em SQLite local para a demonstração. Antes de reiniciar o trabalho em outro computador, copie o projeto e preserve os bancos locais caso queira manter seus dados de teste. O site não foi publicado.

## Materiais da apresentação e do relatório

- `docs/relatorio/main.pdf`: relatório acadêmico com modelagem, backlog, arquitetura, tecnologias, trechos de código, roteiro das telas e referências. A capa deixa campos de identificação para preencher antes de entregar.
- `docs/relatorio/main.typ`: fonte Typst editável do relatório.
- `docs/roteiro-demonstracao.md`: passos sugeridos para apresentar o protótipo em sala.
- `docs/plano-sprints.md`: Product Backlog e proposta de Sprint Backlog até a entrega.
- `docs/architecture.png`, `docs/recommendation-sequence.png` e `docs/favorites-sequence.png`: diagramas de arquitetura e fluxos.
- `docs/screenshots/`: capturas de desktop, celular, status dos microserviços, recomendações e detalhes.
- `docs/referencias-visuais.md`: registro das quatro referências visuais consultadas.

O PDF é uma versão de trabalho: antes da entrega de 9/11/2026, preencha discente, instituição/curso, docente e substitua a seção de repositório quando o link GitHub estiver disponível.
