#!/usr/bin/env python3
import httpx, json

BASE = {
    "alunos": "http://127.0.0.1:8001",
    "turma_aluno": "http://127.0.0.1:8003",
    "turmas": "http://127.0.0.1:8004",
    "notas": "http://127.0.0.1:8002",
    "disciplinas": "http://127.0.0.1:8000",
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

def listar_disciplinas():
    with httpx.Client() as c:
        r = c.get(BASE["disciplinas"] + f"/disciplinas")
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def get_disciplina():
    disciplina_id = input("disciplina_id: ").strip()
    with httpx.Client() as c:
        r = c.get(BASE["disciplinas"] + f"/disciplinas/"+disciplina_id)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def adicionar_disciplina():
    disciplina = input("disciplina: ").strip()
    professor = input("professor: ").strip()
    ementa = input("ementa: ").strip()
    carga_horaria = input("carga horaria: ").strip()
    disciplina = {
        "disciplina": disciplina,
        "professor": professor,
        "ementa": ementa,
        "carga_horaria": carga_horaria,
    }
    with httpx.Client() as c:
        r = c.post(BASE["disciplinas"] + f"/disciplinas", json=disciplina)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def listar_alunos():
    with httpx.Client() as c:
        r = c.get(BASE["alunos"] + f"/alunos")
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def get_aluno():
    aluno_id = input("aluno_id: ").strip()
    with httpx.Client() as c:
        r = c.get(BASE["alunos"] + f"/alunos/"+aluno_id)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def adicionar_aluno():
    nome = input("nome: ").strip()
    matricula = input("matricula: ").strip()
    email = input("email: ").strip()

    aluno = {
        "nome": nome,
        "matricula": matricula,
        "email": email,
    }

    with httpx.Client() as c:
        r = c.post(BASE["alunos"] + f"/alunos", json=aluno)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def delete_aluno():
    aluno_id = input("aluno_id: ").strip()
    with httpx.Client() as c:
        r = c.delete(BASE["alunos"] + f"/alunos/"+aluno_id)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def listar_notas():
    with httpx.Client() as c:
        r = c.get(BASE["notas"] + f"/usuarios")
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def get_nota():
    nota_id = input("nota_id: ").strip()
    with httpx.Client() as c:
        r = c.get(BASE["notas"] + f"/notas/"+nota_id)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def adicionar_nota():
    aluno_id = input("aluno_id: ").strip()
    disciplina_id = input("disciplina_id: ").strip()
    turma_id = input("turma_id: ").strip()
    valor = input("valor: ").strip()

    nota = {
        "aluno_id": aluno_id,
        "disciplina_id": disciplina_id,
        "turma_id": turma_id,
        "valor": valor
    }
    
    with httpx.Client() as c:
        r = c.post(BASE["notas"] + f"/notas", json=nota)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def get_nota_completa():
    nota_id = input("nota_id: ").strip()
    with httpx.Client() as c:
        r = c.get(BASE["notas"] + f"/notas/completa/"+nota_id)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def listar_turmas():
    with httpx.Client() as c:
        r = c.get(BASE["turmas"] + f"/turmas")
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def get_turma():
    turma_id = input("turma_id: ").strip()
    with httpx.Client() as c:
        r = c.get(BASE["turmas"] + f"/turmas/"+turma_id)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def get_turmas_por_sala():
    sala = input("sala: ").strip()
    with httpx.Client() as c:
        r = c.get(BASE["turmas"] + f"/turmas/sala/"+sala)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def get_turmas_por_disciplina():
    disciplina = input("disciplina: ").strip()
    with httpx.Client() as c:
        r = c.get(BASE["turmas"] + f"/turmas/discip/"+disciplina)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def listar_matriculas():
    with httpx.Client() as c:
        r = c.get(BASE["turma_aluno"] + f"/matriculas")
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def listar_matriculas_por_turmas():
    turma_id = input("turma_id: ").strip()
    with httpx.Client() as c:
        r = c.get(BASE["turma_aluno"] + f"/matriculas/turma/"+turma_id)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def adicionar_matricula():
    turma_id = input("turma_id: ").strip()
    id_aluno = input("id_aluno: ").strip()

    matricula = {
        "turma_id": turma_id,
        "id_aluno": id_aluno,
    }

    with httpx.Client() as c:
        r = c.post(BASE["turma_aluno"] + f"/matriculas", json=matricula)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def delete_matricula():
    turma_id = input("turma_id: ").strip()
    id_aluno = input("id_aluno: ").strip()

    matricula = {
        "turma_id": turma_id,
        "id_aluno": id_aluno,
    }

    with httpx.Client() as c:
        r = c.delete(BASE["turma_aluno"] + f"/matriculas", json=matricula)
        print(r.status_code, pretty(r.json() if r.headers.get('content-type','').startswith('application/json') else r.text))

def menu():
    while True:
        print("\n GATEWAY DE SERVIÇOS:")
        print("1)  Health (todos os serviços)")
        print("2)  Listar disciplinas")
        print("3)  Buscar disciplina por ID")
        print("4)  Adicionar disciplina")
        print("5)  Listar alunos")
        print("6)  Buscar aluno por ID")
        print("7)  Adicionar aluno")
        print("8)  Remover aluno")
        print("9)  Listar notas")
        print("10) Buscar nota por ID")
        print("11) Adicionar nota")
        print("12) Nota completa por ID")
        print("13) Listar turmas")
        print("14) Buscar turma por ID")
        print("15) Turmas por sala")
        print("16) Turmas por disciplina")
        print("17) Listar matrículas")
        print("18) Matrículas por turma")
        print("19) Adicionar matrícula")
        print("20) Remover matrícula")
        print("0)  Sair")
        op = input("Escolha: ").strip()
        try:
            if op == "1": health()
            elif op == "2": listar_disciplinas()
            elif op == "3": get_disciplina()
            elif op == "4": adicionar_disciplina()
            elif op == "5": listar_alunos()
            elif op == "6": get_aluno()
            elif op == "7": adicionar_aluno()
            elif op == "8": delete_aluno()
            elif op == "9": listar_notas()
            elif op == "10": get_nota()
            elif op == "11": adicionar_nota()
            elif op == "12": get_nota_completa()
            elif op == "13": listar_turmas()
            elif op == "14": get_turma()
            elif op == "15": get_turmas_por_sala()
            elif op == "16": get_turmas_por_disciplina()
            elif op == "17": listar_matriculas()
            elif op == "18": listar_matriculas_por_turmas()
            elif op == "19": adicionar_matricula()
            elif op == "20": delete_matricula()
            elif op == "0": print("Finalizando"); return
            else: print("opção inválida.")
        except Exception as e:
            print("Erro:", e)

if __name__ == "__main__":
    print("Dica: deixe 'python run_all.py' rodando em outro terminal antes de usar o menu.")
    menu()
