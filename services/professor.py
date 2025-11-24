from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

print("MICROSSERVIÇO DE PROFESSORES - Conectado")
print("=" * 60)

app = FastAPI(title="Microserviço de Professores")

class Professor(BaseModel):
    nome: str
    email: str

professor_db = [
    {"id": 1, "professor": "Simone", "email": "simone@email.com"},
    {"id": 2, "professor": "Ricardo", "email": "ricardo@email.com"},
    {"id": 3, "professor": "Mariana", "email": "mariana@email.com"}
]

def health() -> bool:
    try:
        for a in professor_db:
            if not all(k in a for k in ("id", "professor", "email")):
                return False
        return True
    except Exception:
        return False
    
@app.get("/health")
def health_check():
    return {"ok": health()}

contador_id = len(professor_db) + 1

@app.get("/")
def home():
    return {
        "servico": "professores",
        "status": "Online",
        "descricao": "Gerencia informações dos professores",
        "servicos": {
            "listar": "/professores",
            "buscar_por_id": "/professor/{id}",
            "adicionar": "/addProfessores"
        }
    }

@app.get("/professores")
def listar_professores():
    return {"total": len(professor_db), "professor": professor_db}

@app.get("/professor/{professor_id}")
def buscar_professor(professor_id: int):
    for professor in professor_db:
        if professor["id"] == professor_id:
            return professor
    raise HTTPException(status_code=404, detail="Professor não encontrado")

@app.post("/addProfessores")
def adicionar_professor(professor: Professor):
    global contador_id

    for p in professor_db:
        if p["email"].lower() == professor.email.lower():
            raise HTTPException(status_code=400, detail="Já existe um professor com este e-mail.")

    novo_professor = {
        "id": contador_id,
        "nome": professor.nome,
        "email": professor.email,
    }

    contador_id += 1
    professor_db.append(novo_professor)

    return {"mensagem": "Professor adicionado com sucesso!", "professor": novo_professor}

if __name__ == "__main__":
    uvicorn.run("professor:app", host="0.0.0.0", port=8005, reload=True)