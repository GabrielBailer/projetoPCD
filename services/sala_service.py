from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import requests

print("MICROSSERVIÇO DE Sala - Conectado")
print("=" * 60)

app = FastAPI(
    title="Serviço de Sala",
    description="Microserviço responsável pelo gerenciamento das salas no sistema acadêmico.",
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
sala_db = [
    {"id": 1, "disciplina": 1, "nSala": 1, "isLab": True},
    {"id": 2, "disciplina": 2, "nSala": 2, "isLab": False},
    {"id": 3, "disciplina": 3, "nSala": 3, "isLab": True},
]

def health() -> bool:
    try:
        for a in turmas_db:
            if not all(k in a for k in ("id", "disciplina", "nSala", "isLab")):
                return False
        return True
    except Exception:
        return False
    
@app.get("/health")
def health_check():
    return {"ok": health()}

# ================== MODELO (Pydantic) ==================
class SalaInput(BaseModel):
    disciplina: int
    nSala: int
    tipoSala: bool

# ================== ROTAS ==================
@app.get("/")
def home():
    return {
        "servico": "salas",
        "status": "Online",
        "descricao": "Gerencia salas",
        "serviços": {
            "listar_sala": "/salas",
            "buscar_por_sala": "/sala/{id}",
            "filtrar_por_disciplina": "/sala/disciplina/{disciplina}",
            "adicionar_sala": "/addSala"
        }
    }

@app.get("/salas")
def listar_salas():
    return {"servico": "sala", "total": len(sala_db), "dados": sala_db}

@app.get("/sala/{id}")
def buscar_sala(id: int):
    sala = next((s for s in sala_db if s["id"] == id), None)
    if not sala:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    return {"servico": "sala", "sala": sala}

@app.get("/sala/disciplina/{disciplina}")
def turmas_por_disciplina(disciplina: int):
    filtradas = [s for s in sala_db if s["disciplina"] == disciplina]
    return {"servico": "sala", "filtro": f"disciplina={disciplina}", "dados": filtradas}

@app.post("/addSala")
def adicionar_sala(sala: SalaInput):

    validar_recurso("http://localhost:8000/disciplina", sala.disciplina, "disciplina")

    # Verificar duplicado: disciplina + sala + horários
    for s in sala_db:
        if (s["disciplina"] == sala.disciplina and
            s["nSala"].lower() == turma.sala.lower() and
            s["tipoSala"] == turma.horarioIni):
            raise HTTPException(
                status_code=400,
                detail="Esta sala já está cadastrada com mesmo horário, sala e disciplina."
            )

    novo_id = max(t["id"] for s in sala_db) + 1 if sala_db else 1
    nova_sala = {
        "id": novo_id,
        "disciplina": sala.disciplina,
        "nSala": sala.nSala,
        "isLab": sala.isLab
    }

    sala_db.append(nova_sala)

    return {"mensagem": "Sala adicionada com sucesso!", "sala": nova_sala}

# ================== EXECUÇÃO ==================
if __name__ == "__main__":
    uvicorn.run("microservico_sala:app", host="0.0.0.0", port=8004, reload=True)
