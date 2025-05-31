from conexao import conectar

def cadastrar_aluno(nome, cpf, endereco):
    if not nome.strip():
        print("Erro: Nome não pode estar vazio.")
        return

    if not cpf.strip():
        print("Erro: CPF não pode estar vazio.")
        return

    if not endereco.strip():
        print("Erro: Endereço não pode estar vazio.")
        return

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # Verifica se o CPF já está cadastrado
        cursor.execute("SELECT id FROM alunos WHERE cpf = %s", (cpf,))
        if cursor.fetchone():
            print("Erro: CPF já cadastrado.")
            return

        # Insere o aluno (sem matrícula ainda)
        cursor.execute(
            "INSERT INTO alunos (nome, cpf, endereco) VALUES (%s, %s, %s)",
            (nome, cpf, endereco)
        )
        aluno_id = cursor.lastrowid  # Captura o ID gerado

        # Gera matrícula no formato MAT0001
        matricula = f"MAT{aluno_id:04d}"

        # Atualiza o campo matrícula
        cursor.execute(
            "UPDATE alunos SET matricula = %s WHERE id = %s",
            (matricula, aluno_id)
        )

        conexao.commit()
        print(f"Aluno '{nome}' cadastrado com matrícula {matricula}.")

    except Exception as erro:
        print("Erro ao cadastrar aluno:", erro)
        conexao.rollback()

    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
