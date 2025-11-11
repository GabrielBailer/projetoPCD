import threading, time
import uvicorn

from services.disciplina import app as disciplina_app
from services.turmas import app as turmas_app
from services.professor import app as professor_app
from services.gateway import app as gateway_app
from services.turma_aluno import app as turma_aluno_app
from services.nota import app as nota_app
from services.aluno import app as aluno_app

def run(app, port):
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    threads = [
        threading.Thread(target=run, args=(disciplina_app, 8001), daemon=True),
        threading.Thread(target=run, args=(turmas_app, 8002), daemon=True),
        threading.Thread(target=run, args=(professor_app, 8003), daemon=True),
        threading.Thread(target=run, args=(gateway_app, 8010), daemon=True), 
        threading.Thread(target=run, args=(turma_aluno_app, 8011), daemon=True),
        threading.Thread(target=run, args=(nota_app, 8012), daemon=True), 
        threading.Thread(target=run, args=(aluno_app, 8013), daemon=True), 
]
    for t in threads: t.start()
    print("Services up: gateway:8010, disciplina:8001, turmas:8002, professor:8003, turma_aluno:80011, nota:80012, aluno:80013")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
