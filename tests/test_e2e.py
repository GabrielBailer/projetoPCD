import time, httpx, subprocess, sys, os, signal

def test_fluxo_academico_v2():
    p = subprocess.Popen([sys.executable, "run_all.py"])
    try:
        time.sleep(2.8)
        c = httpx.Client()

        # health
        assert c.get("http://127.0.0.1:8010/health").status_code == 200
        assert c.get("http://127.0.0.1:8001/health").status_code == 200
        assert c.get("http://127.0.0.1:8002/health").status_code == 200
        assert c.get("http://127.0.0.1:8003/health").status_code == 200

        # cria turma e matricula aluno
        r = c.post("http://127.0.0.1:8002/turmas", json={"turma_id":"ADS101","professor":"simone"})
        assert r.status_code == 200
        r = c.post("http://127.0.0.1:8002/matriculas", json={"turma_id":"ADS101","aluno_id":"A1"})
        assert r.status_code == 200

        # agenda aula via orquestrador (8010)
        r = c.post("http://127.0.0.1:8010/agendar-aula", json={
            "turma_id":"ADS101","sala":"LAB-01","inicio":"2025-11-05T19:00","fim":"2025-11-05T21:00"
        })
        assert r.status_code == 200

        # lança nota via orquestrador (8010)
        r = c.post("http://127.0.0.1:8010/lancar-nota", json={
            "turma_id":"ADS101","aluno_id":"A1","avaliacao":"P1","nota":8.5
        })
        assert r.status_code == 200

        # confere notas
        r = c.get("http://127.0.0.1:8003/nota/ADS101/A1")
        assert r.status_code == 200
        regs = r.json()["registros"]
        assert any(x["avaliacao"]=="P1" and x["nota"]==8.5 for x in regs)

    finally:
        if p.poll() is None:
            if os.name == "nt":
                p.terminate()
            else:
                os.kill(p.pid, signal.SIGINT)
            p.wait(timeout=5)
