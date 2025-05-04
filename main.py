from cadastro import cadastrar_aluno  # Importa a função de cadastro de aluno
from login import login_funcionario   # Importa a função de login do funcionário

def menu():  # Função principal com o menu do sistema
    print("=== Login do Funcionário ===")
    funcionario_id = login_funcionario()  # Realiza login e retorna o ID do funcionário

    if not funcionario_id:  # Se o login falhar, o acesso é negado
        print("Acesso negado.")
        return

    while True:  # Loop principal do sistema após login
        print("\n=== Sistema de Cadastro de Notas ===")
        print("1. Cadastrar aluno")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")  # Menu com opções

        if opcao == "1":
            nome = input("Nome do aluno: ")  # Solicita o nome do aluno
            disciplina = input("Disciplina: ")  # Solicita a disciplina

            try:
                nota = float(input("Nota (0 a 10): "))  # Solicita a nota
                cadastrar_aluno(nome, nota, disciplina, funcionario_id)  # Chama a função de cadastro
            except ValueError:
                print("Erro: Nota inválida. Digite um número.")  # Erro caso o usuário digite algo que não seja número

        elif opcao == "0":
            print("Saindo...")  # Encerra o programa
            break

        else:
            print("Opção inválida.")  # Caso o usuário digite uma opção que não existe

# Ponto de entrada do sistema (executa o menu)
if __name__ == "__main__":
    menu()
