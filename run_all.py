import threading, time
import uvicorn

from services.disciplina import app as disciplina_app

def run(app, port):
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    threads = [
        threading.Thread(target=run, args=(disciplina_app, 8099), daemon=True),
    ]
    for t in threads: t.start()
    print("Services up: academico:8010, salas:8001, turmas:8002, notas:8003")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")