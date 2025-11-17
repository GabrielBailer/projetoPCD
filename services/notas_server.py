from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import requests

print("MICROSSERVIÇO DE NOTAS")
print("=" * 60)

app = FastAPI(title="Microserviço de Nota")

# CONFIGURAÇÃO DAS URLS EXTERNAS
ALUNOS_URL = "http://localhost:8001/alunos"
TURMAS_URL = "http://localhost:8004/turmas"
DISCIPLINAS_URL = "http://localhost:8000/disciplinas"

class NotaInput (BaseModel):
    aluno_id: int
    turma_id: int 
    disciplina_id: int
    valor: float

def validar_recurso(url: str, recurso_id: int, nome_recurso: str):
    try:
        resposta = requests.get(f"{url}/{recurso_id}")  # Corrigido: use requests.get ao invés de request.get
        if resposta.status_code != 200:
            raise HTTPException(status_code=404, detail=f"{nome_recurso} não encontrado")
    except:
        raise HTTPException(status_code=503, detail=f"Serviço de {nome_recurso.lower()} indisponível")

# ================== BANCO DE DADOS SIMULADO ==================
notas_db = [
    {"id_nota": 1, "id_turma": 1, "Nota": 8},
    {"id_nota": 2, "id_turma": 1,"id_disciplina": 2, "Nota": 5},
    {"id_nota": 3, "id_turma": 1,"id_aluno": 3, "Nota": 4}
]

# ================== ROTAS DO SERVIÇO DE NOTAS ==================
@app.get("/")
def home():
    return {
        "serviço": "notas",
        "status": "Online",
        "serviços": {
            "listar": "/notas",
            "buscar": "/notas/{id}",
            "adicionar": "/notas",
            "nota_completa": "/notas/completa/{id}"
        }
    }

@app.get("/notas")
def listar_notas():
    """Serviço de Notas - Lista notas"""
    return {"total": len(notas_db), "notas": notas_db}

@app.get("/notas/{nota_id}")
def buscar_nota(nota_id: int):
    for nota in notas_db:
        if nota["id_nota"] == nota_id:
            return nota
    raise HTTPException(status_code=404, detail="Nota não encontrada")

contador_id = len(notas_db) + 1
@app.post("/notas")
def adicionar_nota(nota: NotaInput):
    global contador_id

    validar_recurso(ALUNOS_URL, nota.aluno_id, "Aluno")
    validar_recurso(TURMAS_URL, nota.turma_id, "Turma")
    validar_recurso(DISCIPLINAS_URL, nota.disciplina_id, "Disciplina")

    nova_nota = {
        "id_nota": contador_id,
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
    nota = next((n for n in notas_db if n["id_nota"] == nota_id), None)

    if not nota:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    
    try:
        aluno = requests.get(f"{ALUNOS_URL}/{nota['id_alunos']}").json().get("alunos")
    except:
        aluno = {"erro": "Serviço de alunos indisponível"}

    try:
        turma = requests.get(f"{TURMAS_URL}/{nota['id_turma']}").json().get("turma")
    except:
        turma = {"erro": "Serviço de turmas indisponível"}

    try:
        disciplina = requests.get(f"{DISCIPLINAS_URL}/{nota['id_disciplina']}").json().get("disciplina")
    except:
        disciplina = {"erro": "Serviço de disciplinas indisponível"}

    return {
        "nota": nota,
        "aluno": aluno,
        "turma": turma,
        "disciplina": disciplina
    }

if __name__ == "__main__":  # Corrigido a indentação
    uvicorn.run("notas_server:app", host="0.0.0.0", port=8002, reload=True)  # Correção do nome do módulo
