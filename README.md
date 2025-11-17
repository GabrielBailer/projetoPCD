# Sistema Acadêmico Modular
Sistema de Gerenciamento Acadêmico composto por vários microsserviços independentes (alunos, turmas, disciplinas, notas e matrículas), organizados e acessados através de um API Gateway. O sistema permite cadastrar, listar, consultar e integrar informações acadêmicas.

### 🔗 Gateway
Ponto único de entrada do sistema, roteando requisições para os microsserviços e padronizando acessos.

### 📚 Disciplina
Administra as disciplinas disponíveis.

**Endpoints**
- **GET /disciplinas** — Lista todas as disciplinas
- **GET /disciplinas/{id}** — Busca disciplina por ID
- **POST /disciplinas** — Adiciona uma nova disciplina

### 🏫 Turmas
Gerencia turmas, horários e salas.

**Endpoints**
- **GET /turmas** — Lista todas as turmas
- **GET /turmas/{id}** — Busca turma por ID
- **GET /turmas/sala/{sala}** — Filtra turmas por sala
- **GET /turmas/discip/{discip}** — Filtra turmas por disciplina


#### 🎓 Serviço de Matrículas (Turma-Aluno)
Relaciona alunos às turmas.

**Endpoints**
- **GET /matriculas** — Lista todas as matrículas
- **GET /matriculas/turma/{id_turma}** — Lista alunos por turma
- **POST /matriculas** — Cria uma nova matrícula
- **DELETE /matriculas** — Remove uma matrícula

#### 📝 Notas
Controla notas.

**Endpoints**
- **GET /notas** — Lista todas as notas
- **GET /notas/{id}** — Busca nota por ID
- **POST /notas** — Adiciona uma nova nota 
- **GET /notas/completa/{id}** — Retorna nota + aluno + turma + disciplina

####  📓 Aluno
Gerencia informações dos alunos.

**Endpoints**
- **GET /alunos** — Lista todos os alunos
- **GET /alunos/{id}** — Busca aluno por ID
- **POST /alunos** — Adiciona um novo aluno
- **DELETE /alunos/{id}** — Remove um aluno
- **GET /health** — Health check
---
## Diagrama da arquitetura

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
   - python services/disciplina.py
   - python services/notas_server.py
   - python gateway.py
---
## Portas utilizadas por cada serviço
Cada microserviço roda em uma porta própria, conforme mapeamento abaixo:

**Serviço - Porta**
- Gateway (Acadêmico) - 8010
- Disciplinas - 8000
- Alunos - 8001
- Notas - 8002
- Turmas - 8004
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

---
## Como cada serviço valida recursos externos
Alguns microsserviços precisam confirmar que dados relacionados realmente existem em outros serviços antes de realizar uma operação.

```
def validar_recurso(url_base: str, recurso_id: int, nome_recurso: str):
    try:
        resposta = requests.get(f"{url_base}/{recurso_id}")
        if resposta.status_code != 200:
            raise HTTPException(status_code=404, detail=f"{nome_recurso} não encontrado no serviço correspondente.")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail=f"Serviço de {nome_recurso.lower()} indisponível no momento.")
```
---
## Responsáveis

---
