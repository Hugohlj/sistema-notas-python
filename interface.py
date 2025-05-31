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

        # Monkey patch de input
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
        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.pack(expand=True)

        ttk.Label(self.frame, text="Bem-vindo!", font=("Arial", 16)).pack(pady=10)

        ttk.Button(self.frame, text="Cadastrar Aluno", bootstyle=PRIMARY, command=self.tela_cadastro_aluno).pack(pady=5)
        ttk.Button(self.frame, text="Consultar Alunos", bootstyle=INFO, command=self.tela_consulta_aluno).pack(pady=5)

    def tela_cadastro_aluno(self):
        self.frame.destroy()  # Fecha a tela anterior

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Cadastro de Aluno", font=("Arial", 14)).pack(pady=10)

        ttk.Label(frame, text="Nome:").pack()
        self.entry_nome = ttk.Entry(frame)
        self.entry_nome.pack()

        ttk.Label(frame, text="CPF:").pack()
        self.entry_cpf = ttk.Entry(frame)
        self.entry_cpf.pack()

        ttk.Label(frame, text="Endereço:").pack()
        self.entry_endereco = ttk.Entry(frame)
        self.entry_endereco.pack()

        ttk.Button(frame, text="Cadastrar", bootstyle=SUCCESS, command=self.acao_cadastrar_aluno).pack(pady=10)
        ttk.Button(frame, text="Voltar", bootstyle=SECONDARY, command=self.tela_principal).pack()

    def tela_consulta_aluno(self):
        self.frame.destroy()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Consultar Alunos", font=("Arial", 14)).pack(pady=10)

        ttk.Label(frame, text="Nome do aluno:").pack()
        self.entry_busca = ttk.Entry(frame)
        self.entry_busca.pack()

        ttk.Button(frame, text="Buscar", bootstyle=INFO, command=self.buscar_alunos).pack(pady=10)

        # Tabela com Treeview
        self.tree = ttk.Treeview(frame, columns=("matricula", "disciplina", "nota"), show="headings")
        self.tree.heading("matricula", text="Matrícula")
        self.tree.heading("disciplina", text="Disciplina")
        self.tree.heading("nota", text="Nota")
        self.tree.pack(pady=10, fill="both", expand=True)

        # Área para atribuir nota
        ttk.Label(frame, text="Disciplina:").pack()
        self.combo_disciplina = ttk.Combobox(frame, values=["Matemática", "Português", "História", "Ciências"])
        self.combo_disciplina.pack()

        ttk.Label(frame, text="Nota (0 a 10):").pack()
        self.entry_nota = ttk.Entry(frame)
        self.entry_nota.pack()

        ttk.Button(frame, text="Atribuir Nota", bootstyle=SUCCESS, command=self.atribuir_nota_interface).pack(pady=10)
        ttk.Button(frame, text="Voltar", bootstyle=SECONDARY, command=self.tela_principal).pack(pady=5)

    def buscar_alunos(self):
        nome = self.entry_busca.get().strip()

        if not nome:
            messagebox.showwarning("Aviso", "Digite o nome do aluno.")
            return

        try:
            from backend import consultar_alunos  # Pessoa 4 criará essa função
            resultados = consultar_alunos(nome)

            self.tree.delete(*self.tree.get_children())

            for item in resultados:
                self.tree.insert("", "end", iid=item["id"], values=(item["matricula"], item["disciplina"], item["nota"]))

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

            from backend import atribuir_nota  # Pessoa 4 criará isso
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

        from cadastro import cadastrar_aluno  # Importa só aqui dentro

        try:
            cadastrar_aluno(nome, cpf, endereco)
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
            self.entry_nome.delete(0, "end")
            self.entry_cpf.delete(0, "end")
            self.entry_endereco.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")


    def cadastro_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=20)
        notebook.add(frame, text="Cadastrar Nota")

        ttk.Label(frame, text="Nome do aluno:").pack()
        self.entry_nome = ttk.Entry(frame)
        self.entry_nome.pack()

        ttk.Label(frame, text="Disciplina:").pack()
        self.entry_disciplina = ttk.Entry(frame)
        self.entry_disciplina.pack()

        ttk.Label(frame, text="Nota (0 a 10):").pack()
        self.entry_nota = ttk.Entry(frame)
        self.entry_nota.pack()

        ttk.Button(frame, text="Cadastrar", bootstyle=SUCCESS, command=self.cadastrar).pack(pady=10)

    def consulta_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=20)
        notebook.add(frame, text="Consultar Notas")

        ttk.Label(frame, text="Nome do aluno:").pack()
        self.entry_busca = ttk.Entry(frame)
        self.entry_busca.pack()

        ttk.Button(frame, text="Buscar", bootstyle=INFO, command=self.buscar_notas).pack(pady=10)

        self.text_resultado = ttk.Text(frame, height=10, width=70)
        self.text_resultado.pack()

    def cadastrar(self):
        nome = self.entry_nome.get()
        disciplina = self.entry_disciplina.get()

        try:
            nota = float(self.entry_nota.get())
            cadastrar_aluno(nome, nota, disciplina, self.funcionario_id)
            messagebox.showinfo("Sucesso", f"Nota cadastrada para {nome}.")
        except ValueError:
            messagebox.showerror("Erro", "Nota inválida. Digite um número.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar: {e}")

    def buscar_notas(self):
        nome = self.entry_busca.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Digite o nome do aluno.")
            return

        try:
            conexao = conectar()
            cursor = conexao.cursor()

            query = """
            SELECT a.nome, n.disciplina, n.nota, f.nome
            FROM notas n
            JOIN alunos a ON a.id = n.aluno_id
            JOIN funcionario f ON f.id = n.funcionario_id
            WHERE a.nome LIKE %s
            """
            cursor.execute(query, (f"%{nome}%",))
            resultados = cursor.fetchall()

            self.text_resultado.delete("1.0", "end")
            if resultados:
                for r in resultados:
                    linha = f"Aluno: {r[0]} | Disciplina: {r[1]} | Nota: {r[2]} | Lançada por: {r[3]}\n"
                    self.text_resultado.insert("end", linha)
            else:
                self.text_resultado.insert("end", "Nenhuma nota encontrada.")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao consultar: {e}")
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")  # Temas: flatly, cyborg, morph, etc.
    app = SistemaNotasGUI(root)
    root.mainloop()
