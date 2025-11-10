from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="turmas")

TURMAS: Dict[str, dict] = {}  # turma_id -> {"professor":str, "alunos":[...], "aulas":[...]}

class NovaTurma(BaseModel):
    turma_id: str
    professor: str

class Matricula(BaseModel):
    turma_id: str
    aluno_id: str

class AulaIn(BaseModel):
    turma_id: str
    sala: str
    inicio: str
    fim: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/turmas")
def criar_turma(t: NovaTurma):
    if t.turma_id in TURMAS:
        raise HTTPException(409, "turma_ja_existe")
    TURMAS[t.turma_id] = {"professor": t.professor, "alunos": [], "aulas": []}
    return {"ok": True}

@app.post("/matriculas")
def matricular(m: Matricula):
    tur = TURMAS.get(m.turma_id)
    if not tur:
        raise HTTPException(404, "turma_nao_encontrada")
    if m.aluno_id not in tur["alunos"]:
        tur["alunos"].append(m.aluno_id)
    return {"ok": True, "alunos": tur["alunos"]}

@app.get("/turmas/{turma_id}/alunos")
def listar_alunos(turma_id: str):
    tur = TURMAS.get(turma_id)
    if not tur:
        raise HTTPException(404, "turma_nao_encontrada")
    return {"alunos": tur["alunos"]}

@app.post("/aulas")
def registrar_aula(a: AulaIn):
    tur = TURMAS.get(a.turma_id)
    if not tur:
        raise HTTPException(404, "turma_nao_encontrada")
    tur["aulas"].append({"sala": a.sala, "inicio": a.inicio, "fim": a.fim})
    return {"ok": True, "total_aulas": len(tur["aulas"])}
