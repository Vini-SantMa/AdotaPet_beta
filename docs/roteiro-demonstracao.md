# Roteiro da demonstração do Patinhas

Use este roteiro como guia da apresentação em sala e da seção de funcionamento no relatório.

1. **Página inicial.** Mostre a proposta, o CTA “Fazer meu match” e o aviso de que pets, fotografias e dados são fictícios. Explique que este protótipo não anuncia animais reais.
2. **Questionário.** Selecione tipo de companhia, porte, moradia, ritmo e convivência com crianças. Não é necessário criar conta. Envie “Ver quem combina comigo”.
3. **Recomendações.** Compare os cartões e mostre a nota, o rótulo e os motivos. Explique que a pontuação é calculada por regras determinísticas, não por IA.
4. **Explorar.** Aplique filtros de espécie, porte, idade e energia; limpe os filtros; compare nome, idade, temperamento, porte e energia.
5. **Detalhes.** Toque em “Conhecer [nome]” para abrir o perfil demonstrativo com história e características de convivência.
6. **Favoritos.** Toque no coração para adicionar um pet. Mostre contador e mural de favoritos. Se atualizar a página ou reiniciar o processo, o estado permanece no banco SQLite local do microserviço Preferências/Favoritos. Remova o favorito se quiser devolver a demonstração ao estado limpo.
7. **Microserviços.** Role até “Por trás das Patinhas”. Mostre Gateway online e os três serviços. Abra a documentação Swagger a partir do painel e explique a rota `/api/status`.
8. **Documentação do código.** Mostre o diagrama, `README.md`, diretórios `gateway/`, `services/`, `web/js/`, testes e backlog. Cada serviço tem seu OpenAPI e banco independente quando aplicável.

**Comando da execução local:** `python -m pip install -r requirements.txt`, depois `python run.py`; abrir `http://127.0.0.1:3000`. APIs: Gateway `:3000/docs`, Pets `:8001/docs`, Preferências/Favoritos `:8002/docs`, Recomendações `:8003/docs`.

**Nota para a apresentação:** use o mesmo navegador ou ambiente após salvar um favorito. A aplicação usa o identificador demonstrativo `demo`; esse estado não representa contas independentes de vários usuários.
