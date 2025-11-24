"""Microserviço de Notas - Versão corrigida
- FastAPI
- requests para chamadas HTTP externas
- Pydantic para validação de payloads
- CORS habilitado

Como rodar:
$ pip install fastapi uvicorn requests
$ python microservico_notas.py
ou
$ uvicorn microservico_notas:app --reload --port 8002

Exemplos de teste (curl):
- Listar: curl http://localhost:8002/notas
- Buscar: curl http://localhost:8002/notas/1
- Adicionar: curl -X POST "http://localhost:8002/notas" -H "Content-Type: application/json" -d '{"aluno_id":1,"disciplina_id":1,"turma_id":1,"valor":7.5}'
"""

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional

print("MICROSSERVIÇO DE NOTAS")
print("=" * 60)

app = FastAPI(title="Microserviço de Nota")

# Configurar CORS para permitir todas as origens (apenas para desenvolvimento)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CONFIGURAÇÃO DAS URLS EXTERNAS (ajuste conforme seus serviços)
ALUNOS_URL = "http://localhost:8001/alunos"
TURMAS_URL = "http://localhost:8004/turmas"
DISCIPLINAS_URL = "http://localhost:8000/disciplinas"


def validar_recurso(url: str, recurso_id: int, nome_recurso: str, timeout: float = 3.0):
    """Verifica se recurso existe consultando o serviço externo.
    Lança HTTPException(503) se o serviço estiver indisponível e 404 se o recurso não for encontrado.
    """
    try:
        resp = requests.get(f"{url}/{recurso_id}", timeout=timeout)
    except requests.RequestException:
        # Problema de conexão com o serviço
        raise HTTPException(status_code=503, detail=f"Serviço de {nome_recurso.lower()} indisponível")

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail=f"{nome_recurso} não encontrado")
    if resp.status_code != 200:
        # Outros códigos HTTP do serviço externo
        raise HTTPException(status_code=503, detail=f"Serviço de {nome_recurso.lower()} retornou {resp.status_code}")


# ================== BANCO DE DADOS SIMULADO ==================
notas_db: List[dict] = [
    {"id": 1, "aluno_id": 1, "disciplina_id": 1, "turma_id": 1, "valor": 8.0},
    {"id": 2, "aluno_id": 2, "disciplina_id": 2, "turma_id": 1, "valor": 5.0},
    {"id": 3, "aluno_id": 3, "disciplina_id": 2, "turma_id": 1, "valor": 4.0},
]

# Contador de IDs (inicia após o maior ID existente)
contador_id = max(n["id"] for n in notas_db) if notas_db else 0


# ================== MODELOS ==================
class NotaCreate(BaseModel):
    aluno_id: int = Field(..., gt=0)
    disciplina_id: int = Field(..., gt=0)
    turma_id: int = Field(..., gt=0)
    valor: float = Field(..., ge=0, le=10)


class Nota(BaseModel):
    id: int
    aluno_id: int
    disciplina_id: int
    turma_id: int
    valor: float


# ================== ROTAS DO SERVICO DE NOTAS ==================
@app.get("/", tags=["status"])  # raiz
def home():
    return {
        "servico": "notas",
        "status": "Online",
        "servicos": {
            "listar": "/notas",
            "buscar": "/notas/{id}",
            "adicionar": "/notas (POST)",
            "nota_completa": "/notas/completa/{id}"
        }
    }


@app.get("/notas", response_model=dict, tags=["notas"]) 
def listar_notas():
    """Retorna todas as notas (simulado)."""
    return {"total": len(notas_db), "notas": notas_db}


@app.get("/notas/{nota_id}", response_model=Nota, tags=["notas"]) 
def buscar_nota(nota_id: int):
    nota = next((n for n in notas_db if n["id"] == nota_id), None)
    if nota:
        return nota
    raise HTTPException(status_code=404, detail="Nota não encontrada")


@app.post("/notas", tags=["notas"])  # adicionar nota
def adicionar_nota(nota: NotaCreate):
    global contador_id

    # Verifica recursos externos (caso queira permitir criação offline, comente essas linhas)
    validar_recurso(ALUNOS_URL, nota.aluno_id, "Aluno")
    validar_recurso(TURMAS_URL, nota.turma_id, "Turma")
    validar_recurso(DISCIPLINAS_URL, nota.disciplina_id, "Disciplina")

    contador_id += 1
    nova_nota = {
        "id": contador_id,
        "aluno_id": nota.aluno_id,
        "disciplina_id": nota.disciplina_id,
        "turma_id": nota.turma_id,
        "valor": nota.valor,
    }

    notas_db.append(nova_nota)
    return {"mensagem": "Nota adicionada com sucesso!", "nota": nova_nota}


@app.get("/notas/completa/{nota_id}", tags=["notas"]) 
def nota_completa(nota_id: int):
    nota = next((n for n in notas_db if n["id"] == nota_id), None)

    if not nota:
        raise HTTPException(status_code=404, detail="Nota não encontrada")

    # Tenta buscar dados externos; se falhar, devolve mensagem de erro parcial
    try:
        aluno_resp = requests.get(f"{ALUNOS_URL}/{nota['aluno_id']}", timeout=3)
        if aluno_resp.status_code == 200:
            aluno = aluno_resp.json()
        else:
            aluno = {"erro": f"Serviço de alunos retornou {aluno_resp.status_code}"}
    except requests.RequestException:
        aluno = {"erro": "Serviço de alunos indisponível"}

    try:
        turma_resp = requests.get(f"{TURMAS_URL}/{nota['turma_id']}", timeout=3)
        if turma_resp.status_code == 200:
            turma = turma_resp.json()
        else:
            turma = {"erro": f"Serviço de turmas retornou {turma_resp.status_code}"}
    except requests.RequestException:
        turma = {"erro": "Serviço de turmas indisponível"}

    try:
        disciplina_resp = requests.get(f"{DISCIPLINAS_URL}/{nota['disciplina_id']}", timeout=3)
        if disciplina_resp.status_code == 200:
            disciplina = disciplina_resp.json()
        else:
            disciplina = {"erro": f"Serviço de disciplinas retornou {disciplina_resp.status_code}"}
    except requests.RequestException:
        disciplina = {"erro": "Serviço de disciplinas indisponível"}

    return {
        "nota": nota,
        "aluno": aluno,
        "turma": turma,
        "disciplina": disciplina,
    }


# Executa com: python microservico_notas.py (para desenvolvimento)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("microservico_notas:app", host="0.0.0.0", port=8002, reload=True)
