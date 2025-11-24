from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import requests

print("MICROSSERVIÇO DE DISCIPLINA - Conectado")
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
    id_professor: int
    ementa: str
    carga_horaria: str

def validar_recurso(url: str, recurso_id: int, nome_recurso: str):
    try:
        resposta = requests.get(f"{url}/{recurso_id}")  
        if resposta.status_code != 200:
            raise HTTPException(status_code=404, detail=f"{nome_recurso} não encontrado")
    except:
        raise HTTPException(status_code=503, detail=f"Serviço de {nome_recurso.lower()} indisponível")

# ================== BANCO DE DADOS SIMULADO ==================
disciplina_db = [
    {"id_disciplina": 1, "disciplina": "Programação Concorrente e Distribuída", "id_professor": 1, "ementa": "ementa", "carga_horaria": "80h"},
    {"id_disciplina": 2, "disciplina": "Engenharia de Software", "id_professor": 2, "ementa": "ementa", "carga_horaria": "80h"},
    {"id_disciplina": 3, "disciplina": "Projeto Integrador", "id_professor": 3, "ementa": "ementa", "carga_horaria": "40h"}
]

contador_id = len(disciplina_db) + 1

def health() -> bool:
    try:
        for a in disciplina_db:
            if not all(k in a for k in ("id_disciplina", "disciplina", "id_professor", "ementa", "carga_horaria")):
                return False
        return True
    except Exception:
        return False
    
@app.get("/health")
def health_check():
    return {"ok": health()}

# ================== ROTAS DO SERVIÇO ==================

@app.get("/")
def home():
    return {
        "servico": "disciplinas",
        "status": "Online",
        "descricao": "Administra as disciplinas disponíveis.",
        "servicos": {
            "listar": "/disciplinas",
            "buscar": "/disciplina/{id}",
            "adicionar": "/addDisciplinas",
        }
    }

@app.get("/disciplinas")
def listar_disciplinas():
    """Lista todas as disciplinas"""
    return {"total": len(disciplina_db), "disciplinas": disciplina_db}

@app.get("/disciplina/{disciplina_id}")
def buscar_disciplina(disciplina_id: int):
    for disciplina in disciplina_db:
        if disciplina["id_disciplina"] == disciplina_id:
            return {"servico": "disciplina", "disciplina": disciplina}
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")

@app.post("/addDisciplinas")
def adicionar_disciplina(disciplina: Disciplina):
    global contador_id

    validar_recurso("http://127.0.0.1:8005/professor", disciplina.id_professor, "professor")

    for d in disciplina_db:
        if d["disciplina"].lower() == disciplina.disciplina.lower() and d["id_professor"] == disciplina.id_professor:
            raise HTTPException(status_code=400, detail="Esta disciplina já está cadastrada para este professor.")


    nova_disciplina = {
        "id_disciplina": contador_id,
        "disciplina": disciplina.disciplina,
        "id_professor": disciplina.id_professor,
        "ementa": disciplina.ementa,
        "carga_horaria": disciplina.carga_horaria
    }

    disciplina_db.append(nova_disciplina)
    contador_id += 1
    return {"mensagem": "Disciplina adicionada com sucesso!", "disciplina": nova_disciplina}

if __name__ == "__main__":
    uvicorn.run("disciplina:app", host="127.0.0.1", port=8000, reload=True)