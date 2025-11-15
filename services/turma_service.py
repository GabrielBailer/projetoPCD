from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

print("🎓 MICROSSERVIÇO DE TURMAS - CONECTADO AO GATEWAY")
print("=" * 60)

app = FastAPI(
    title="Serviço de Turmas",
    description="Microserviço responsável pelo gerenciamento das turmas no sistema acadêmico.",
    version="1.0.0"
)

# ================== CONFIGURAÇÃO DE CORS ==================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================== BANCO DE DADOS SIMULADO ==================
turmas_db = [
    {"id": 1, "discip": "Dispositivos Móveis", "horarioIni": "18h30", "horarioFim": "22h30", "sala": "Lab 6"},
    {"id": 2, "discip": "Programação Orientada a Objetos", "horarioIni": "18h30", "horarioFim": "22h30", "sala": "Lab 3"},
    {"id": 3, "discip": "Programação para Internet", "horarioIni": "18h30", "horarioFim": "22h30", "sala": "Lab 2"},
    {"id": 4, "discip": "Programação Concorrente Distribuída", "horarioIni": "18h30", "horarioFim": "22h30", "sala": "Lab 6"},

]

# ================== ROTAS PRINCIPAIS ==================
@app.get("/")
def home():
    return {
        "servico": "turmas",
        "status": "online",
        "descricao": "Microserviço de turmas ativo",
        "endpoints": {
            "listar_turmas": "/turmas",
            "buscar_turma_por_id": "/turmas/{id}",
            "filtrar_por_sala": "/turmas/sala/{sala}",
            "filtrar_por_disciplina": "/turmas/discip/{discip}",
            "adicionar_turma": "/turmas (POST)",
            "atualizar_turma": "/turmas/{id} (PUT)",
            "remover_turma": "/turmas/{id} (DELETE)"
        }
    }

# ================== REQUISIÇÕES ==================
@app.get("/turmas")
def listar_turmas():
    return {"servico": "turmas", "total": len(turmas_db), "dados": turmas_db}

@app.get("/turmas/{turma_id}")
def buscar_turma(turma_id: int):
    for turma in turmas_db:
        if turma["id"] == turma_id:
            return {"servico": "turmas", "turma": turma}
    raise HTTPException(status_code=404, detail="Turma não encontrada")

@app.get("/turmas/sala/{sala}")
def turmas_por_sala(sala: str):
    filtradas = [t for t in turmas_db if t["sala"].lower() == sala.lower()]
    return {"servico": "turmas", "filtro": f"sala={sala}", "dados": filtradas}

@app.get("/turmas/discip/{discip}")
def turmas_por_disciplina(discip: str):
    filtradas = [t for t in turmas_db if discip.lower() in t["discip"].lower()]
    return {"servico": "turmas", "filtro": f"discip={discip}", "dados": filtradas}

# ================== EXECUÇÃO ==================
if __name__ == "__main__":
    uvicorn.run("microservico_turmas:app", host="0.0.0.0", port=8001, reload=True)
