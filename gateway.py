#!/usr/bin/env python3
import httpx, json

BASE = {
    "alunos": "http://:",
    "salas": "http://:",
    "turmas": "http://:",
    "notas": "http://:",
    "disciplinas": "http://127.0.0.1:8099",
}

def pretty(x):
    try: return json.dumps(x, ensure_ascii=False, indent=2)
    except: return str(x)

def health():
    with httpx.Client() as c:
        for k, url in BASE.items():
            try:
                r = c.get(url + "/health", timeout=2.0)
                print(f"[{k}] {r.status_code} -> {r.json()}")
            except Exception as e:
                print(f"[{k}] ERRO: {e}")

def listar_alunos():
    turma_id = input("turma_id: ").strip()
    with httpx.Client() as c:
        r = c.get(BASE["alunos"] + f"/alunos")
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def listar_disciplinas():
    #turma_id = input("turma_id: ").strip()
    with httpx.Client() as c:
        r = c.get(BASE["disciplinas"] + f"/disciplinas")
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def menu():
    while True:
        print("\n GATEWAY DE SERVIÇOS: ")
        print("1) Health (todos os serviços)")
        print("2) Listar alunos")
        print("3) Listar disciplinas")
        print("0) Sair")
        op = input("Escolha: ").strip()
        try:
            if op == "1": health()
            elif op == "2": listar_alunos()
            elif op == "3": listar_disciplinas()
            elif op == "0": print("Finalizando"); return
            else: print("opção inválida.")
        except Exception as e:
            print("Erro:", e)

if __name__ == "__main__":
    print("Dica: deixe 'python run_all.py' rodando em outro terminal antes de usar o menu.")
    menu()
