from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
import requests 

print("🎯 MICROSSERVIÇO DE MATRÍCULAS")
print("=" * 60)

app = FastAPI(title="Turma-Aluno")

matriculas_db = []
contador_matricula = 1

class Matricula(BaseModel):
    id_turma: str
    id_aluno: str

def validar_recurso(url_base: str, recurso_id: int, nome_recurso: str):
    try:
        resposta = requests.get(f"{url_base}/{recurso_id}")
        if resposta.status_code != 200:
            raise HTTPException(status_code=404, detail=f"{nome_recurso} não encontrado no serviço correspondente.")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail=f"Serviço de {nome_recurso.lower()} indisponível no momento.")

@app.get("/")
def home():
    return {
        "servico": "matriculas",
        "status": "Online",
        "descricao": "Gerencia a relação entre alunos e turmas.",
        "servicos": {
            "listar_matriculas": "/matriculas",
            "buscar_por_turma": "/matriculas/turma/{id_turma}",
            "criar_matricula": "/matriculas",
            "remover_matricula": "/matriculas{id_matricula}"
        }
    }

@app.get("/matriculas")
def listar_matriculas():
    return {"servico": "matriculas", "total": len(matriculas_db), "dados": matriculas_db}

@app.get("/matriculas/turma/{id_turma}")
def listar_alunos_por_turma(id_turma: int):
    """Buscar aluno numa turma pelo ID"""
    for matricula in matriculas_db:
        if matricula["id_turma"] == id_turma:
            return {"servico": "matriculas", "id_turma": id_turma, "aluno": matricula}
    raise HTTPException(status_code=404, detail="Nenhum aluno matriculado nessa turma.")
    
@app.post("/matriculas")
def criar_matricula(matricula: Matricula):
    """Adicionar numa nova matricula?"""
    global contador_matricula

    nova_matricula = matricula.dict()
    nova_matricula["matricula"] = matricula

    matriculas_db.append(nova_matricula) #matricula_db
    contador_matricula += 1

    return {"mensagem": "Matricula criada com sucesso!", "matricula": nova_matricula}

@app.post("/matriculas")
def criar_matricula(matricula: Matricula):

    for m in matriculas_db:
        if m["id_turma"] == matricula.id_turma and m["id_aluno"] == matricula.id_aluno:
            raise HTTPException(status_code=400, detail="Aluno já matriculado nessa turma.")

    validar_recurso(ALUNOS_URL, matricula.id_aluno, "Aluno")    
    validar_recurso(TURMAS_URL, matricula.id_turma, "Turma")

    matriculas_db.append(matricula.dict())
    return {"mensagem": "Matrícula criada com sucesso!", "matricula": matricula}

@app.delete("/matriculas")
def remover_matricula(matricula: Matricula):
    for m in matriculas_db:
        if m["id_turma"] == matricula.id_turma and m["id_aluno"] == matricula.id_aluno:
            matriculas_db.remove(m)
            return {"mensagem": "Matrícula removida com sucesso!"}
    raise HTTPException(status_code=404, detail="Matrícula não encontrada.")

    if __name__ == "__main__":
        uvicorn.run("turma_aluno:app", host="127.0.0.1", port=8003, reload=True)