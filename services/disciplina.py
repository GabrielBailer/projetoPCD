from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

print("🎯 MICROSSERVIÇO DE DISCIPLINA")
print("=" * 60)

app = FastAPI(title="Microserviço de Disciplina")
# Config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================== MODELO ==================

class Disciplina(BaseModel):
    disciplina: str
    professor: str
    ementa: str
    carga_horaria: str

# ================== BANCO DE DADOS SIMULADO ==================
disciplina_db = [
    {"id_disciplina": 1, "disciplina": "Programação Concorrente e Distribuída", "professor": "Simone", "ementa": "ementa", "carga_horaria": "80h"},
    {"id_disciplina": 2, "disciplina": "Engenharia de Software", "professor": "Rogério", "ementa": "ementa", "carga_horaria": "80h"},
    {"id_disciplina": 3, "disciplina": "Projeto Integrador", "professor": "Leonardo", "ementa": "ementa", "carga_horaria": "40h"}
]

contador_id = 4

# ================== ROTAS DO SERVIÇO ==================

@app.get("/")
def home():
    return {
        "servico": "disciplinas",
        "status": "Online 🚀",
        "servicos": {
            "listar": "/disciplinas",
            "buscar": "/disciplinas/{id}",
            "adicionar": "/disciplinas",
        }
    }

@app.get("/disciplinas")
def listar_disciplinas():
    """Lista todas as disciplinas"""
    return {"total": len(disciplina_db), "disciplinas": disciplina_db}

@app.get("/disciplinas/{disciplina_id}")
def buscar_disciplina(disciplina_id: int):
    for d in disciplina_db:
        if d["id_disciplina"] == disciplina_id:
            return {"servico": "disciplina", "displina": disciplina}
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")

@app.post("/disciplinas")
def adicionar_disciplina(disciplina: Disciplina):
    global contador_id
    nova_disciplina = {
        "id_disciplina": contador_id,
        "disciplina": disciplina.disciplina,
        "professor": disciplina.professor,
        "ementa": disciplina.ementa,
        "carga_horaria": disciplina.carga_horaria
    }
    disciplina_db.append(nova_disciplina)
    contador_id += 1
    return {"mensagem": "Disciplina adicionada com sucesso!", "disciplina": nova_disciplina}