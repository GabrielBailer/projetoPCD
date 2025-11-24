from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import requests

print("MICROSSERVIÇO DE NOTAS - Conectado")
print("=" * 60)

app = FastAPI(title="Microserviço de Nota")

# CONFIGURAÇÃO DAS URLS EXTERNAS
DISCIPLINAS_URL = "http://localhost:8000/disciplina"
ALUNOS_URL = "http://localhost:8001/aluno"

class NotaInput (BaseModel):
    aluno_id: int
    disciplina_id: int
    nota: float

def validar_recurso(url: str, recurso_id: int, nome_recurso: str):
    try:
        resposta = requests.get(f"{url}/{recurso_id}")  # Corrigido: use requests.get ao invés de request.get
        if resposta.status_code != 200:
            raise HTTPException(status_code=404, detail=f"{nome_recurso} não encontrado")
    except:
        raise HTTPException(status_code=503, detail=f"Serviço de {nome_recurso.lower()} indisponível")

# ================== BANCO DE DADOS SIMULADO ==================
notas_db = [
    {"id_nota": 1,"id_aluno": 1, "id_disciplina": 1, "nota": 8},
    {"id_nota": 2,"id_aluno": 2, "id_disciplina": 2, "nota": 5},
    {"id_nota": 3,"id_aluno": 3, "id_disciplina": 3, "nota": 4}
]

def health() -> bool:
    try:
        for a in notas_db:
            if not all(k in a for k in ("id_nota", "id_aluno", "id_disciplina", "nota")):
                return False
        return True
    except Exception:
        return False
    
@app.get("/health")
def health_check():
    return {"ok": health()}

# ================== ROTAS DO SERVIÇO DE NOTAS ==================
@app.get("/")
def home():
    return {
        "serviço": "notas",
        "status": "Online",
        "descricao": "Controla notas.",
        "serviços": {
            "listar": "/notas",
            "buscar": "/notas/{id}",
            "adicionar": "/addNotas",
            "nota_completa": "/notas/completa/{id}"
        }
    }

@app.get("/notas")
def listar_notas():
    """Serviço de Notas - Lista notas"""
    return {"total": len(notas_db), "notas": notas_db}

@app.get("/nota/{nota_id}")
def buscar_nota(nota_id: int):
    for nota in notas_db:
        if nota["id_nota"] == nota_id:
            return nota
    raise HTTPException(status_code=404, detail="Nota não encontrada")

contador_id = len(notas_db) + 1
@app.post("/addNotas")
def adicionar_nota(nota: NotaInput):
    global contador_id

    validar_recurso(ALUNOS_URL, nota.aluno_id, "aluno")
    validar_recurso(DISCIPLINAS_URL, nota.disciplina_id, "disciplina")

    for n in notas_db:
        if n["id_aluno"] == nota.aluno_id and n["id_disciplina"] == nota.disciplina_id:
            raise HTTPException(
                status_code=400,
                detail="Este aluno já possui uma nota cadastrada para essa disciplina."
            )

    nova_nota = {
        "id_nota": contador_id,
        "id_aluno": nota.aluno_id,
        "id_disciplina": nota.disciplina_id,
        "nota": nota.nota
    }

    notas_db.append(nova_nota)
    contador_id += 1
    return {"mensagem": "Nota adicionada com sucesso!", "nota": nova_nota}

@app.get("/notas/completa/{nota_id}")
def nota_completa(nota_id: int):
    nota = next((n for n in notas_db if n["id_nota"] == nota_id), None)

    if not nota:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    
    try:
        aluno = requests.get(f"{ALUNOS_URL}/{nota['id_aluno']}").json().get("aluno")
    except:
        aluno = {"erro": "Serviço de alunos indisponível"}

    try:
        disciplina = requests.get(f"{DISCIPLINAS_URL}/{nota['id_disciplina']}").json().get("disciplina")
    except:
        disciplina = {"erro": "Serviço de disciplinas indisponível"}

    return {
        "nota": nota,
        "aluno": aluno,
        "disciplina": disciplina
    }

    

if __name__ == "__main__":  # Corrigido a indentação
    uvicorn.run("notas_server:app", host="0.0.0.0", port=8002, reload=True)  # Correção do nome do módulo
