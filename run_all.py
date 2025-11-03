import threading, time
import uvicorn

from services.salas import app as salas_app
from services.turmas import app as turmas_app
from services.notas import app as notas_app
from services.academico import app as academico_app

def run(app, port):
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="info")
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    threads = [
        threading.Thread(target=run, args=(salas_app, 8001), daemon=True),
        threading.Thread(target=run, args=(turmas_app, 8002), daemon=True),
        threading.Thread(target=run, args=(notas_app, 8003), daemon=True),
        threading.Thread(target=run, args=(academico_app, 8010), daemon=True),  # mudou p/ 8010
    ]
    for t in threads: t.start()
    print("Services up: academico:8010, salas:8001, turmas:8002, notas:8003")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
