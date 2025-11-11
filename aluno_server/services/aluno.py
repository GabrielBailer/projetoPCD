from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import requests 


print("🎯 MICROSSERVIÇO DE ALUNOS")
print("=" * 60)


class AlunoIn(BaseModel):
    nome: str
    matricula: str
    email: str

app = FastAPI(title="Microserviço de Alunos")

aluno_db = [
    {"id": 1, "nome": "Ana Silva", "matricula": "202501", "email": "ana@email.com"},
    {"id": 2, "nome": "Carlos Pereira", "matricula": "202502", "email": "carlos@email.com"},
    {"id": 3, "nome": "Carla Costa", "matricula": "202503", "email": "carla@email.com"},
]

contador_id = 16 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def health() -> bool:
    try:
        for a in aluno_db:
            if not all(k in a for k in ("id", "nome", "matricula", "email")):
                return False
        return True
    except Exception:
        return False
    
@app.get("/health")
def health_check():
    return {"ok": health()}

@app.get("/")
def home():
    return {
        "servico": "alunos",
        "status": "Online 🚀",
        "servicos": {
            "listar": "/alunos",
            "buscar_por_id": "/alunos/{id}",
            "adicionar": "/alunos",
            "remover": "/alunos/{id}"
        }
    }

@app.get("/alunos")
def listar_alunos():
    """Serviço de Alunos - Lista todos os alunos"""
    return {"total": len(aluno_db), "alunos": aluno_db}

@app.get("/alunos/{aluno_id}")
def buscar_aluno(aluno_id: int):
    """Busca um aluno pelo ID"""
    for aluno in aluno_db:
        if aluno["id"] == aluno_id:
            return aluno
    raise HTTPException(status_code=404, detail="Aluno não encontrado")

@app.post("/alunos")
def adicionar_aluno(aluno: AlunoIn):
    """Adiciona um novo aluno"""
    global contador_id
    
    novo_aluno = aluno.dict()
    novo_aluno["id"] = contador_id
    
    aluno_db.append(novo_aluno)
    contador_id += 1
    
    return {"mensagem": "Aluno adicionado com sucesso!", "aluno": novo_aluno}

@app.delete("/alunos/{aluno_id}")
def remover_aluno(aluno_id: int):
    """Remove um aluno pelo ID"""
    global aluno_db
    
    aluno_para_remover = next((a for a in aluno_db if a["id"] == aluno_id), None)
    
    if not aluno_para_remover:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    aluno_db.remove(aluno_para_remover)
    
    return {"mensagem": f"Aluno ID {aluno_id} removido com sucesso."}

if __name__ == "__main__":
    print("🚀 Iniciando servidor FastAPI...")
    uvicorn.run(app, host="127.0.0.1", port=8013)