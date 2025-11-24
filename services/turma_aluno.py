from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import requests

print("MICROSSERVIÇO DE MATRÍCULAS - Conectado")
print("=" * 60)

app = FastAPI(title="Microserviço de Matrículas")

# URLs dos outros serviços
ALUNOS_URL = "http://127.0.0.1:8001/alunos"
TURMAS_URL = "http://127.0.0.1:8004/turmas"


# ===========================
#   Função de validação
# ===========================
def validar_recurso(url_base: str, recurso_id: int, nome_recurso: str):
    try:
        resposta = requests.get(f"{url_base}/{recurso_id}")
        if resposta.status_code != 200:
            raise HTTPException(status_code=404, detail=f"{nome_recurso} não encontrado.")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail=f"Serviço de {nome_recurso.lower()} indisponível.")

matriculas_db = [
    {"id_turma": 1, "id_aluno": 1, "n_matricula": "202501"},
    {"id_turma": 2, "id_aluno": 2, "n_matricula": "202502"},
    {"id_turma": 3, "id_aluno": 3, "n_matricula": "202503"}
]

def health() -> bool:
    try:
        for a in matriculas_db:
            if not all(k in a for k in ("id_turma", "id_aluno", "n_matricula")):
                return False
        return True
    except Exception:
        return False
    
@app.get("/health")
def health_check():
    return {"ok": health()}

contador_matricula = 202504

class Matricula(BaseModel):
    id_turma: int
    id_aluno: int

@app.get("/")
def home():
    return {
        "servico": "matriculas",
        "status": "Online",
        "descricao": "Relaciona alunos às turmas.",
        "servicos": {
            "listar_matriculas": "/matriculas",
            "listar_por_turma": "/matriculas/turma/{id_turma}",
            "criar_matricula": "/addMatriculas",
            "remover_matricula": "/matriculas/{id_turma}/{id_aluno}"
        }
    }


@app.get("/matriculas")
def listar_matriculas():
    return {"total": len(matriculas_db), "dados": matriculas_db}


@app.get("/matriculas/turma/{id_turma}")
def listar_alunos_por_turma(id_turma: int):
    alunos = [m for m in matriculas_db if m["id_turma"] == id_turma]
    if not alunos:
        raise HTTPException(status_code=404, detail="Nenhum aluno matriculado nesta turma.")
    return {"id_turma": id_turma, "alunos": alunos}


@app.post("/addMatriculas")
def criar_matricula(matricula: Matricula):
    global contador_matricula

    # Validar aluno e turma em outros microserviços
    validar_recurso(ALUNOS_URL, matricula.id_aluno, "Aluno")
    validar_recurso(TURMAS_URL, matricula.id_turma, "Turma")

    # Verificar se já existe
    for m in matriculas_db:
        if m["id_turma"] == matricula.id_turma and m["id_aluno"] == matricula.id_aluno:
            raise HTTPException(status_code=400, detail="Aluno já está matriculado nesta turma.")

    nova_matricula = {
        "id_turma": matricula.id_turma,
        "id_aluno": matricula.id_aluno,
        "n_matricula": str(contador_matricula)
    }

    matriculas_db.append(nova_matricula)
    contador_matricula += 1

    return {"mensagem": "Matrícula criada com sucesso!", "matricula": nova_matricula}


@app.delete("/matriculas/{id_turma}/{id_aluno}")
def remover_matricula(id_turma: int, id_aluno: int):
    for m in matriculas_db:
        if m["id_turma"] == id_turma and m["id_aluno"] == id_aluno:
            matriculas_db.remove(m)
            return {"mensagem": "Matrícula removida com sucesso!"}

    raise HTTPException(status_code=404, detail="Matrícula não encontrada.")


if __name__ == "__main__":
    uvicorn.run("turma_aluno:app", host="127.0.0.1", port=8003, reload=True)