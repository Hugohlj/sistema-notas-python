from conexao import conectar  # Importa a função de conexão com o banco de dados

def cadastrar_aluno(nome, nota, disciplina, funcionario_id):  # Função para cadastrar aluno e nota
    if not nome.strip():  # Verifica se o nome está vazio
        print("Erro: Nome não pode estar vazio.")
        return

    if not (0 <= nota <= 10):  # Verifica se a nota está entre 0 e 10
        print("Erro: Nota deve estar entre 0 e 10.")
        return

    if not disciplina.strip():  # Verifica se a disciplina está vazia
        print("Erro: Disciplina não pode estar vazia.")
        return

    try:
        conexao = conectar()  # Conecta ao banco de dados
        cursor = conexao.cursor()

        # Verifica se o aluno já existe no banco pelo nome
        cursor.execute("SELECT id FROM alunos WHERE nome = %s", (nome,))
        aluno = cursor.fetchone()

        if aluno:
            aluno_id = aluno[0]  # Usa o ID do aluno existente
        else:
            # Insere um novo aluno com uma matrícula gerada a partir do nome
            cursor.execute("INSERT INTO alunos (nome, matricula) VALUES (%s, %s)", (nome, "MAT"+nome[:3]))
            aluno_id = cursor.lastrowid  # Captura o ID gerado automaticamente

        # Insere a nota do aluno para a disciplina, associada ao funcionário
        query_nota = """
            INSERT INTO notas (aluno_id, disciplina, nota, funcionario_id)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_nota, (aluno_id, disciplina, nota, funcionario_id))  # Executa o INSERT
        conexao.commit()  # Salva as alterações no banco

        print(f"Aluno '{nome}' registrado com nota {nota} em '{disciplina}'.")  # Confirmação para o usuário

    except Exception as erro:
        print("Erro ao cadastrar aluno:", erro)  # Mostra erro se algo falhar

    finally:
        if conexao.is_connected():  # Fecha a conexão se estiver ativa
            cursor.close()
            conexao.close()
