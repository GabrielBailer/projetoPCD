# Sistema Acadêmico Modular
Sistema de Gerenciamento Acadêmico composto por vários microsserviços independentes (alunos, turmas, disciplinas, notas e matrículas), organizados e acessados através de um API Gateway. O sistema permite cadastrar, listar, consultar e integrar informações acadêmicas.

### 🔗 Gateway
Ponto único de entrada do sistema, roteando requisições para os microsserviços e padronizando acessos.

### 📚 Disciplina
Administra as disciplinas disponíveis.

**Porta**
"disciplina:app", host="127.0.0.1", port=8000

**Campos**
"id_disciplina"
"disciplina"
"id_professor"
"ementa"
"carga_horaria"

**Endpoints**
- **GET /disciplinas** — Lista todas as disciplinas
- **GET /disciplina/{id}** — Busca disciplina por ID
- **POST /addDisciplinas** — Adiciona uma nova disciplina linkada com o professor

### 🏫 Salas
Gerencia salas.

**Porta**
"microservico_turmas:app", host="0.0.0.0", port=8004

**Campos**
"id"
"disciplina"
"nSala"
"isLab"

**Endpoints**
- **GET /salas** — Lista todas as turmas
- **GET /sala/{id}** — Busca turma por ID
- **GET /sala/disciplina/{disciplina}** — Filtra salas por disciplina
- **POST /addSala** - Adiciona uma nova sala


#### 🎓 Serviço de Matrículas
Faz a matrícula dos alunos à uma turma.

**Porta**
"turma_aluno:app", host="127.0.0.1", port=8003

**Campos**
"id_turma"
"id_aluno"
"n_matricula"

**Endpoints**
- **GET /matriculas** — Lista todas as matrículas
- **GET /matriculas/disciplina/{id_disciplina}** — Lista alunos por turma
- **POST /addMatriculas** — Cria uma nova matrícula
- **DELETE /matriculas/{id_turma}/{id_aluno}** — Remove uma matrícula

#### 📝 Notas
Controla notas.

**Porta**
"notas_server:app", host="0.0.0.0", port=8002

**Campos**
"id_nota"
"id_aluno"
"id_disciplina"
"nota"

**Endpoints**
- **GET /notas** — Lista todas as notas
- **GET /notas/{id}** — Busca nota por ID
- **POST /addNotas** — Adiciona uma nova nota 
- **GET /notas/completa/{id}** — Retorna nota + aluno + turma + disciplina

####  📓 Aluno
Gerencia informações dos alunos.

**Porta**
"aluno:app", host="127.0.0.1", port=8001

**Campos**
"id"
"nome"
"email"

**Endpoints**
- **GET /alunos** — Lista todos os alunos
- **GET /alunos/{id}** — Busca aluno por ID
- **POST /addAlunos** — Adiciona um novo aluno
- **DELETE /alunos/{id}** — Remove um aluno

### 📚 Professor
Gerencia professores.

**Porta**
"professor:app", host="0.0.0.0", port=8005

**Campos**
"id"
"nome"
"email"

**Endpoints**
- **GET /professores** — Lista todos os professores
- **GET /professor/{id}** — Busca professor por ID
- **POST /addProfessores** — Adiciona um novo professor
---
## Diagrama da arquitetura
<img width="670" height="506" alt="image" src="https://github.com/user-attachments/assets/cfd0096f-b9c3-4f10-87f5-4f6d3e0e54df" />


---
## Padrões utilizados

- Arquitetura de Microserviço:
Cada domínio (alunos, turmas, disciplinas, notas, matrículas) funciona como um serviço independente, com base de dados própria e APIs isoladas.
- RESTful API:
Todos os serviços seguem o modelo REST, utilizando métodos HTTP adequados (GET, POST, DELETE, etc.).
- Validação Distribuída:
Serviços como Notas e Matrículas validam recursos externos consumindo outros microsserviços via HTTP.

---
## Estrutura das pastas
```
project-root/
│
├── services/# Microsserviços independentes
│   ├── aluno.py                  
│   ├── disciplina.py              
│   ├── notas_server.py
│   ├── professor.py        
│   ├── turma_aluno.py             
│   ├── turma_service.py           
│   └── __pycache__/              
│
├── tests/                         
│
├── gateway.py # API Gateway que centraliza os serviços
├── run_all.py # Script para iniciar todos os serviços juntos
├── requirements.txt # Dependências do projeto
├── README.md # Documentação do sistema
└── .gitignore
```
*obs:*Foi adicionado um arquivo com os testes em um PostmanCollection
---
## Como instalar o serviço
Siga os passos abaixo para instalar o projeto localmente:

1. Clone o repositório: https://github.com/GabrielBailer/projetoPCD.git
2. Crie e ative um ambiente virtual:
python -m venv venv
    - Para Windows: venv\Scripts\activate
    - Para Linux/macOS: source venv/bin/activate
3. Instalar dependências: pip install -r requirements.txt

---
## Como iniciar o serviço
Siga os passos abaixo para iniciar todos os microserviços:

1. Executar todos de uma vez: python run_all.py
2. Ou iniciar manualmente cada serviço, por exemplo:
   - python services/aluno.py

---
## Portas utilizadas por cada serviço
Cada microserviço roda em uma porta própria, conforme mapeamento abaixo:

**Serviço - Porta**
- Gateway (Acadêmico) - 8010
- Disciplinas - 8000
- Alunos - 8001
- Notas - 8002
- Turmas - 8004
- Professor - 8005
- Matrícula(Turma-Aluno) - 8003

**Modelo URL das rotas**
http://127.0.0.1:8000

## Como o gateway roteia as requisições
Passos para o funcionamento do serviços:
1. Cliente faz uma requisição para o gateway: POST /disciplinas
2. Gateway identifica para qual microserviço a requisição pertence:
      - Verifica a base de portas para cada microderviço
      - Disciplinas = 8000
3. Gateway repassa a requisição:
      - http://127.0.0.1:8000/disciplinas
      - Headers $h
      - Body '{"id_disciplina":1,"disciplina":"Teste", "professor": "Nome Generico", "ementa": "100", "carga_horaria": "20"}'
4. Gateway recebe resposta do microserviço:
      -   Disciplina adicionada com sucesso! @{id_disciplina=4; disciplina=Teste; professor=Nome Generico; ementa=100; carga_h...
5. Gateway devolve a resposta para o cliente

##Em execução

Qunado iniciamos o serviço do gateway utilizando python gateway.py nós recebemos o menu abaixo, nele podemos ver todos as chamadas dos microserviços que temos:
<img width="246" height="447" alt="image" src="https://github.com/user-attachments/assets/bc6429a7-93f5-4568-9e23-5712827bf59f" />

Vou mostrar como funcionam alguns dos serviços quando chamamos ele pelo menu:
1) Health, o health retorna os status de todos os microserviços, assim podemos ver se eles estão rodando corretamente:
<img width="245" height="133" alt="image" src="https://github.com/user-attachments/assets/6e2627ad-6872-48c7-9168-d51c1c357e45" />

As chamadas para os microserviços todos possuem um médodo REST de listar para retonar uma lista json com todas as informações que estão cadastradas no banco de cada uma delas
- 2 Listar disciplinas
- 5 Listar alunos
- 9 Listar notas
- 13 Listar salas
- 17 Listar matrículas
- 22 Listar professor
Selecionando qualquer uma das opções acima o resultado seria parecido com esse, exemplo: selecionando 2, temos uma lista com todas as disciplinas2 cadastradas:
<img width="431" height="448" alt="image" src="https://github.com/user-attachments/assets/dab4d7c3-2176-413f-b6c2-187b180459e7" />


As chamadas para alguns microserviços possuem um médodo REST de buscar por ID para retonar uma lista json com as informações que estão cadastradas no banco com aquele ID
- 3 Buscar disciplina por ID
- 6 Buscar aluno por ID
- 10 Buscar nota por ID
- 14 Buscar sala por ID
- 23 Buscar professor por ID
Selecionando qualquer uma das opções acima o resultado seria parecido com esse, exemplo: selecionando 6 com id 3, temos uma lista com todas as disciplinas2 cadastradas:
<img width="217" height="174" alt="image" src="https://github.com/user-attachments/assets/efc989d6-f8d4-4ffd-a03b-6a2ccc25b872" />

As chamadas para os microserviços possuem um médodo REST de adicionar para criar novas informações que estão cadastradas no banco:
- 4 Adicionar disciplina
- 7 Adicionar aluno
- 11 Adicionar nota
- 15 Adicionar sala
- 19 Adicionar matrícula
- 21 Adiconar professor
Selecionando qualquer uma das opções acima o resultado seria parecido com esse, exemplo: selecionando 11 e inserindo os campos solicitados, temos um retorno da nova informação que cadastramos:
<img width="322" height="221" alt="image" src="https://github.com/user-attachments/assets/73b12d7d-a48b-4db3-9527-d36222b675cb" />

As chamadas para os microserviços  Aluno e Matrícula possuem um médodo REST de remover por id para excluir informações que estão cadastradas no banco:
- 8 Remover aluno
- 20 Remover matrícula
Selecionando qualquer uma das opções acima o resultado seria parecido com esse, exemplo: selecionando 20 com id , temos um retorno da nova informação que excluimos:
<img width="339" height="108" alt="image" src="https://github.com/user-attachments/assets/51820bcc-02f8-458a-b2dd-3163a9a9326a" />

Temos também duas chamadas de "relatórios" eles trazem um retorno filtrados das informações:
- 16 Salas por disciplina
- 18 Matrículas por disciplina
Selecionando qualquer uma das opções acima o resultado seria parecido com esse, exemplo: selecionando 16 com id 1, temos um retorno das salas onde esta disciplina está cadastrada
<img width="229" height="345" alt="image" src="https://github.com/user-attachments/assets/30d9c660-399a-4cfb-9909-cd89a9fffd1d" />

---
## Responsáveis
Luis---------Gateway
Matheo-------Disciplina
Gabriel------Professor
Gabriel------Revisar e modificar erros
Gabriel------Turmas
Gabrielle----Turma_aluno
Ana----------Notas
Amanda-------Aluno
Amanda-------Coleçao postman
Amanda-------Documentação (readme)


---
