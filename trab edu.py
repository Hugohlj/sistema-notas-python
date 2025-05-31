import sqlite3

def conectar():
    return sqlite3.connect('sistema_nota.db')

def cadastrar_aluno(nome, matricula):
    if not nome.strip():
        print("❌ Nome não pode estar vazio.")
        return
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alunos (nome, matricula) VALUES (?, ?)", (nome, matricula))
        conn.commit()
        print("✅ Aluno cadastrado com sucesso.")
    except sqlite3.IntegrityError:
        print("❌ Matrícula já cadastrada.")
    finally:
        conn.close()

def cadastrar_nota(aluno_id, funcionario_id, disciplina, nota):
    if not (0 <= nota <= 5):
        print("❌ Nota deve estar entre 0 e 5.")
        return
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notas (aluno_id, funcionario_id, disciplina, nota)
            VALUES (?, ?, ?, ?)
        """, (aluno_id, funcionario_id, disciplina, nota))
        conn.commit()
        print("✅ Nota cadastrada com sucesso.")
    except sqlite3.IntegrityError as e:
        print("❌ Erro ao cadastrar nota:", e)
    finally:
        conn.close()
