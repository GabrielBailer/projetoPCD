from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import requests

print("MICROSSERVIÇO DE TURMAS - Conectado")
print("=" * 60)

app = FastAPI(
    title="Serviço de Turmas",
    description="Microserviço responsável pelo gerenciamento das turmas no sistema acadêmico.",
    version="1.0.0"
)

def validar_recurso(url: str, recurso_id: int, nome_recurso: str):
    try:
        resposta = requests.get(f"{url}/{recurso_id}")  
        if resposta.status_code != 200:
            raise HTTPException(status_code=404, detail=f"{nome_recurso} não encontrado")
    except:
        raise HTTPException(status_code=503, detail=f"Serviço de {nome_recurso.lower()} indisponível")

# ================== CONFIG CORS ==================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================== BANCO DE DADOS ==================
turmas_db = [
    {"id": 1, "disciplina": 1, "horarioIni": "18h30", "horarioFim": "22h30", "sala": "Lab 6"},
    {"id": 2, "disciplina": 2, "horarioIni": "18h30", "horarioFim": "22h30", "sala": "Lab 3"},
    {"id": 3, "disciplina": 3, "horarioIni": "18h30", "horarioFim": "22h30", "sala": "Lab 2"},
]

def health() -> bool:
    try:
        for a in turmas_db:
            if not all(k in a for k in ("id", "disciplina", "horarioIni", "horarioFim", "sala")):
                return False
        return True
    except Exception:
        return False
    
@app.get("/health")
def health_check():
    return {"ok": health()}

# ================== MODELO (Pydantic) ==================
class TurmaInput(BaseModel):
    disciplina: int
    horarioIni: str
    horarioFim: str
    sala: str

# ================== ROTAS ==================
@app.get("/")
def home():
    return {
        "servico": "turmas",
        "status": "Online",
        "descricao": "Gerencia turmas, horários e salas",
        "serviços": {
            "listar_turmas": "/turmas",
            "buscar_turma_por_id": "/turmas/{id}",
            "filtrar_por_sala": "/turmas/sala/{sala}",
            "filtrar_por_disciplina": "/turmas/disciplina/{disciplina}",
            "adicionar_turma": "/addTurmas"
        }
    }

@app.get("/turmas")
def listar_turmas():
    return {"servico": "turmas", "total": len(turmas_db), "dados": turmas_db}

@app.get("/turmas/{turma_id}")
def buscar_turma(turma_id: int):
    turma = next((t for t in turmas_db if t["id"] == turma_id), None)
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return {"servico": "turmas", "turma": turma}

@app.get("/turmas/sala/{sala}")
def turmas_por_sala(sala: str):
    filtradas = [t for t in turmas_db if t["sala"].lower() == sala.lower()]
    return {"servico": "turmas", "filtro": f"sala={sala}", "dados": filtradas}

@app.get("/turmas/disciplina/{disciplina}")
def turmas_por_disciplina(disciplina: int):
    filtradas = [t for t in turmas_db if t["disciplina"] == disciplina]
    return {"servico": "turmas", "filtro": f"disciplina={disciplina}", "dados": filtradas}

@app.post("/addTurmas")
def adicionar_turma(turma: TurmaInput):

    validar_recurso("http://localhost:8000/disciplina", turma.disciplina, "disciplina")

    # Verificar duplicado: disciplina + sala + horários
    for t in turmas_db:
        if (t["disciplina"] == turma.disciplina and
            t["sala"].lower() == turma.sala.lower() and
            t["horarioIni"] == turma.horarioIni and
            t["horarioFim"] == turma.horarioFim):
            raise HTTPException(
                status_code=400,
                detail="Esta turma já está cadastrada com mesmo horário, sala e disciplina."
            )

    novo_id = max(t["id"] for t in turmas_db) + 1 if turmas_db else 1
    nova_turma = {
        "id": novo_id,
        "disciplina": turma.disciplina,
        "horarioIni": turma.horarioIni,
        "horarioFim": turma.horarioFim,
        "sala": turma.sala
    }

    turmas_db.append(nova_turma)

    return {"mensagem": "Turma adicionada com sucesso!", "turma": nova_turma}

# ================== EXECUÇÃO ==================
if __name__ == "__main__":
    uvicorn.run("microservico_turmas:app", host="0.0.0.0", port=8004, reload=True)
