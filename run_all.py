import threading, time
import uvicorn

from services.disciplina import app as disciplina_app
from services.aluno import app as aluno_app
from services.notas_server import app as nota_app
from services.turma_aluno import app as turma_aluno_app
from services.turma_service import app as turma_app


def run(app, port):
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    threads = [
        threading.Thread(target=run, args=(disciplina_app, 8000), daemon=True),     #DISCIPLINA
        threading.Thread(target=run, args=(aluno_app, 8001), daemon=True),          #ALUNO
        threading.Thread(target=run, args=(nota_app, 8002), daemon=True),           #NOTA
        threading.Thread(target=run, args=(turma_aluno_app, 8003), daemon=True),    #TURMA_ALUNO
        threading.Thread(target=run, args=(turma_app, 8004), daemon=True),          #TURMA
    ]
    for t in threads: t.start()
    print("Services up: academico:8010, salas:8001, turmas:8002, notas:8003")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")