import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from cadastro import cadastrar_aluno
from login import login_funcionario
from conexao import conectar


class SistemaNotasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Notas")
        self.root.geometry("600x400")
        self.funcionario_id = None
        self.style = ttk.Style("flatly")

        self.tela_login()

    def tela_login(self):
        if hasattr(self, "frame"):
            self.frame.destroy()

        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.pack(expand=True)

        ttk.Label(self.frame, text="Login do Funcionário", font=("Arial", 16)).pack(pady=10)

        ttk.Label(self.frame, text="CPF:").pack()
        self.entry_cpf = ttk.Entry(self.frame)
        self.entry_cpf.pack()

        ttk.Label(self.frame, text="Senha:").pack()
        self.entry_senha = ttk.Entry(self.frame, show="*")
        self.entry_senha.pack()

        ttk.Button(self.frame, text="Entrar", bootstyle=PRIMARY, command=self.realizar_login).pack(pady=10)

    def realizar_login(self):
        cpf = self.entry_cpf.get()
        senha = self.entry_senha.get()

        import builtins
        original_input = builtins.input
        builtins.input = lambda _: cpf if _ == "CPF: " else senha

        try:
            self.funcionario_id = login_funcionario()
        finally:
            builtins.input = original_input

        if self.funcionario_id:
            self.frame.destroy()
            self.tela_principal()
        else:
            messagebox.showerror("Erro de Login", "CPF ou senha incorretos.")

    def tela_principal(self):
        if hasattr(self, "frame"):
            self.frame.destroy()

        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.pack(expand=True)

        ttk.Label(self.frame, text="Bem-vindo!", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self.frame, text="Cadastrar Aluno", bootstyle=PRIMARY, command=self.tela_cadastro_aluno).pack(pady=5)
        ttk.Button(self.frame, text="Consultar Alunos", bootstyle=INFO, command=self.tela_consulta_aluno).pack(pady=5)

    def tela_cadastro_aluno(self):
        if hasattr(self, "frame"):
            self.frame.destroy()

        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.pack(expand=True)

        ttk.Label(self.frame, text="Cadastro de Aluno", font=("Arial", 14)).pack(pady=10)

        ttk.Label(self.frame, text="Nome:").pack()
        self.entry_nome = ttk.Entry(self.frame)
        self.entry_nome.pack()

        ttk.Label(self.frame, text="CPF:").pack()
        self.entry_cpf = ttk.Entry(self.frame)
        self.entry_cpf.pack()

        ttk.Label(self.frame, text="Endereço:").pack()
        self.entry_endereco = ttk.Entry(self.frame)
        self.entry_endereco.pack()

        ttk.Button(self.frame, text="Cadastrar", bootstyle=SUCCESS, command=self.acao_cadastrar_aluno).pack(pady=10)
        ttk.Button(self.frame, text="Voltar", bootstyle=SECONDARY, command=self.tela_principal).pack()

    def tela_consulta_aluno(self):
        if hasattr(self, "frame"):
            self.frame.destroy()

        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.pack(fill="both", expand=True)

        ttk.Label(self.frame, text="Consultar Alunos", font=("Arial", 14)).pack(pady=10)

        ttk.Label(self.frame, text="Nome do aluno:").pack()
        self.entry_busca = ttk.Entry(self.frame)
        self.entry_busca.pack()

        ttk.Button(self.frame, text="Buscar", bootstyle=INFO, command=self.buscar_alunos).pack(pady=10)

        colunas = ("matricula", "nome", "matematica", "portugues", "historia",
    "geografia", "ciencias", "ingles", "artes", "educacao_fisica")

        self.tree = ttk.Treeview(self.frame, columns=colunas, show="headings")

        for col in colunas:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")

        self.tree.pack(pady=10, fill="both", expand=True)

        ttk.Label(self.frame, text="Disciplina:").pack()
        self.combo_disciplina = ttk.Combobox(self.frame, values=["Matemática", "Português", "História", "Geografia","Ciências", "Inglês", "Artes", "Educação Física"])

        ttk.Label(self.frame, text="Nota (0 a 10):").pack()
        self.entry_nota = ttk.Entry(self.frame)
        self.entry_nota.pack()

        ttk.Button(self.frame, text="Atribuir Nota", bootstyle=SUCCESS, command=self.atribuir_nota_interface).pack(pady=10)
        ttk.Button(self.frame, text="Voltar", bootstyle=SECONDARY, command=self.tela_principal).pack(pady=5)

        # Atualiza a tabela automaticamente
        self.buscar_alunos()

    def buscar_alunos(self):
        nome = self.entry_busca.get().strip()

        try:
            from backend import consultar_alunos
            resultados = consultar_alunos(nome)

            self.tree.delete(*self.tree.get_children())

            for aluno in resultados:
                self.tree.insert("", "end", iid=aluno["id"], values=(
                    aluno["matricula"],
                    aluno["nome"],
                    aluno["matematica"] or "-",
                    aluno["portugues"] or "-",
                    aluno["historia"] or "-",
                    aluno["geografia"] or "-",
                    aluno["ciencias"] or "-",
                    aluno["ingles"] or "-",
                    aluno["artes"] or "-",
                    aluno["educacao_fisica"] or "-"
                ))

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar alunos: {e}")

    def atribuir_nota_interface(self):
        try:
            aluno_item = self.tree.focus()
            if not aluno_item:
                messagebox.showwarning("Aviso", "Selecione um aluno na tabela.")
                return

            aluno_id = int(aluno_item)
            disciplina = self.combo_disciplina.get()
            nota = float(self.entry_nota.get())

            from backend import atribuir_nota
            atribuir_nota(aluno_id, disciplina, nota, self.funcionario_id)

            messagebox.showinfo("Sucesso", "Nota atribuída com sucesso!")
            self.buscar_alunos()

        except ValueError:
            messagebox.showerror("Erro", "Nota inválida. Digite um número.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atribuir nota: {e}")

    def acao_cadastrar_aluno(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        endereco = self.entry_endereco.get()

        try:
            cadastrar_aluno(nome, cpf, endereco)
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
            self.entry_nome.delete(0, "end")
            self.entry_cpf.delete(0, "end")
            self.entry_endereco.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")


if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = SistemaNotasGUI(root)
    root.mainloop()
