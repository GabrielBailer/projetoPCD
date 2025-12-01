from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests as request
from pydantic import BaseModel

print("MICROSSERVIÇO DE NOTAS")
print("=" * 60)

class Nota(BaseModel):
    aluno_id: int
    turma_id: int
    disciplina_id: int
    valor: float

app = FastAPI(title="Microserviço de Nota")

# ================== CONFIGURAÇÃO DE CORS ==================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CONFIGURAÇÃO DAS URLS EXTERNAS
ALUNOS_URL = "http://localhost:8001/alunos"
TURMAS_URL = "http://localhost:8004/turmas"
DISCIPLINAS_URL = "http://localhost:8000/disciplinas"

def validar_recurso(url: str, recurso_id: int, nome_recurso: str):
    try:
        resposta = request.get(f"{url}/{recurso_id}", timeout=3)

        if resposta.status_code != 200:
            raise HTTPException(status_code=404, detail=f"{nome_recurso} não encontrado")
    except:
        raise HTTPException(status_code=503, detail=f"Serviço de {nome_recurso.lower()} indisponível")

# ================== BANCO DE DADOS SIMULADO ==================
notas_db = [
  {"id": 1, "aluno_id": 1, "turma_id": 1, "disciplina_id": 1, "valor": 8},
  {"id": 2, "aluno_id": 2, "turma_id": 1, "disciplina_id": 2, "valor": 5},
  {"id": 3, "aluno_id": 3, "turma_id": 1, "disciplina_id": 3, "valor": 4}
]

# ================== ROTAS DO SERVICO DE USUÁRIOS ==================
@app.get("/")
def home():
    return {
        "servico": "notas",
        "status": "Online",
        "servicos": {
            "listar": "/notas",
            "buscar": "/notas/{id}",
            "adicionar": "/notas",
            "nota_completa": "/notas/completa/{id}"
        }
    }

@app.get("/notas")
def listar_notas():
    """Serviço de Notas - Lista notas"""
    return {"total": len(notas_db), "notas":notas_db}

@app.get("/notas/{nota_id}")
def buscar_nota(nota_id: int):
    for nota in notas_db:
        if nota["id"] == nota_id:
            return nota
    raise HTTPException(status_code=404, detail="Nota não encontrada")


contador_id = len(notas_db) + 1
@app.post("/notas")
def adicionar_nota(nota: Nota):
    global contador_id

    validar_recurso(ALUNOS_URL, nota.aluno_id, "Aluno")
    validar_recurso(TURMAS_URL, nota.turma_id, "Turma")
    validar_recurso(DISCIPLINAS_URL, nota.disciplina_id, "Disciplina")

    nova_nota = {
        "id": contador_id,
        "aluno_id": nota.aluno_id,
        "disciplina_id": nota.disciplina_id,
        "turma_id": nota.turma_id,
        "valor": nota.valor
    }

    notas_db.append(nova_nota)
    contador_id += 1
    return {"mensagem": "Nota adicionada com sucesso!", "nota": nova_nota}


@app.get("/notas/completa/{nota_id}")
def nota_completa(nota_id: int):
    nota = next((n for n in notas_db if n["id"] == nota_id), None)

    if not nota:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    try:
        aluno = request.get(f"{ALUNOS_URL}/{nota['aluno_id']}").json().get("aluno")
    except:
        aluno = {"erro": "Serviço de alunos indisponível"}
    try:
        turma = request.get(f"{TURMAS_URL}/{nota['turma_id']}").json().get("turma")
    except:
        turma = {"erro": "Serviço de turmas indisponível"}
    try:
        disciplina = request.get(f"{DISCIPLINAS_URL}/{nota['disciplina_id']}").json().get("disciplina")
    except:
        disciplina = {"erro": "Serviço de disciplinas indisponível"}

    return {
        "nota": nota,
        "aluno": aluno,
        "turma": turma,
        "disciplina": disciplina
    }