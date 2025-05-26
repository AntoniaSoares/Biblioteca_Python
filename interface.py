import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from database import Database
from models import Usuario, Livro

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Biblioteca")
        self.db = Database()
        
        self.criar_menu()
        self.exibir_tela_login()

    def criar_menu(self):
        menubar = tk.Menu(self.root)
        
        # Menu Cadastros
        cadastro_menu = tk.Menu(menubar, tearoff=0)
        cadastro_menu.add_command(label="Usuários", command=self.exibir_tela_cadastro_usuario)
        cadastro_menu.add_command(label="Livros", command=self.exibir_tela_cadastro_livro)
        menubar.add_cascade(label="Cadastros", menu=cadastro_menu)
        
        # Menu Operações
        operacoes_menu = tk.Menu(menubar, tearoff=0)
        operacoes_menu.add_command(label="Empréstimo", command=self.exibir_tela_emprestimo)
        operacoes_menu.add_command(label="Devolução", command=self.exibir_tela_devolucao)
        menubar.add_cascade(label="Operações", menu=operacoes_menu)
        
        # Menu Relatórios
        relatorios_menu = tk.Menu(menubar, tearoff=0)
        relatorios_menu.add_command(label="Livros Disponíveis", command=self.exibir_livros_disponiveis)
        relatorios_menu.add_command(label="Livros Emprestados por Usuário", command=self.exibir_livros_emprestados_usuario)
        relatorios_menu.add_command(label="Usuários com Atraso", command=self.exibir_usuarios_com_atraso)
        relatorios_menu.add_command(label="Empréstimos por Período", command=self.exibir_emprestimos_periodo)
        relatorios_menu.add_command(label="Média de Livros por Mês", command=self.exibir_media_livros_mes)
        menubar.add_cascade(label="Relatórios", menu=relatorios_menu)
        
        self.root.config(menu=menubar)

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            if widget not in self.root.winfo_children()[:1]:  # Mantém o menu
                widget.destroy()

    def exibir_tela_login(self):
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Bem-vindo ao Sistema de Biblioteca").grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(frame, text="Usuário:").grid(row=1, column=0, sticky=tk.W)
        self.entry_usuario = ttk.Entry(frame)
        self.entry_usuario.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Senha:").grid(row=2, column=0, sticky=tk.W)
        self.entry_senha = ttk.Entry(frame, show="*")
        self.entry_senha.grid(row=2, column=1, pady=5)
        
        ttk.Button(frame, text="Entrar", command=self.login).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Para simplificar, não há autenticação real
        self.entry_usuario.insert(0, "admin")
        self.entry_senha.insert(0, "admin")

    def login(self):
        # Autenticação simplificada (sem verificação real)
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        if usuario and senha:
            self.limpar_tela()
            ttk.Label(self.root, text=f"Bem-vindo, {usuario}!", padding="10").pack()
        else:
            messagebox.showerror("Erro", "Preencha usuário e senha")

    def exibir_tela_cadastro_usuario(self):
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Cadastro de Usuário", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Campos do formulário
        ttk.Label(frame, text="Nome:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_nome = ttk.Entry(frame, width=40)
        self.entry_nome.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="E-mail:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_email = ttk.Entry(frame, width=40)
        self.entry_email.grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="CPF:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_cpf = ttk.Entry(frame, width=40)
        self.entry_cpf.grid(row=3, column=1, pady=5)
        
        # Botões
        ttk.Button(frame, text="Salvar", command=self.salvar_usuario).grid(row=4, column=0, pady=10, sticky=tk.E)
        ttk.Button(frame, text="Cancelar", command=self.exibir_tela_login).grid(row=4, column=1, pady=10, sticky=tk.W)
        
        # Lista de usuários cadastrados
        ttk.Label(frame, text="Usuários Cadastrados:", font=('Arial', 10, 'bold')).grid(row=5, column=0, columnspan=2, pady=10)
        
        columns = ('ID', 'Nome', 'E-mail', 'CPF')
        self.tree_usuarios = ttk.Treeview(frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree_usuarios.heading(col, text=col)
            self.tree_usuarios.column(col, width=100)
        
        self.tree_usuarios.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Preencher a lista
        self.atualizar_lista_usuarios()

    def salvar_usuario(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        cpf = self.entry_cpf.get()
        
        if not nome or not cpf:
            messagebox.showerror("Erro", "Nome e CPF são obrigatórios!")
            return
        
        usuario = Usuario(nome=nome, email=email, cpf=cpf)
        
        try:
            self.db.adicionar_usuario(usuario)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.atualizar_lista_usuarios()
            self.entry_nome.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_cpf.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF já cadastrado!")

    def atualizar_lista_usuarios(self):
        # Limpar a treeview
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        # Adicionar os usuários
        usuarios = self.db.listar_usuarios()
        for usuario in usuarios:
            self.tree_usuarios.insert('', tk.END, values=(
                usuario.id, usuario.nome, usuario.email, usuario.cpf
            ))

    def exibir_tela_cadastro_livro(self):
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Cadastro de Livro", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Campos do formulário
        ttk.Label(frame, text="Título:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_titulo = ttk.Entry(frame, width=40)
        self.entry_titulo.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Autor:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_autor = ttk.Entry(frame, width=40)
        self.entry_autor.grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Ano de Publicação:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_ano = ttk.Entry(frame, width=40)
        self.entry_ano.grid(row=3, column=1, pady=5)
        
        ttk.Label(frame, text="Cópias Disponíveis:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.entry_copias = ttk.Entry(frame, width=40)
        self.entry_copias.grid(row=4, column=1, pady=5)
        
        # Botões
        ttk.Button(frame, text="Salvar", command=self.salvar_livro).grid(row=5, column=0, pady=10, sticky=tk.E)
        ttk.Button(frame, text="Cancelar", command=self.exibir_tela_login).grid(row=5, column=1, pady=10, sticky=tk.W)
        
        # Lista de livros cadastrados
        ttk.Label(frame, text="Livros Cadastrados:", font=('Arial', 10, 'bold')).grid(row=6, column=0, columnspan=2, pady=10)
        
        columns = ('ID', 'Título', 'Autor', 'Ano', 'Cópias')
        self.tree_livros = ttk.Treeview(frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree_livros.heading(col, text=col)
            self.tree_livros.column(col, width=100)
        
        self.tree_livros.grid(row=7, column=0, columnspan=2, pady=5)
        
        # Preencher a lista
        self.atualizar_lista_livros()

    def salvar_livro(self):
        titulo = self.entry_titulo.get()
        autor = self.entry_autor.get()
        ano = self.entry_ano.get()
        copias = self.entry_copias.get()
        
        if not titulo or not autor:
            messagebox.showerror("Erro", "Título e autor são obrigatórios!")
            return
        
        try:
            ano = int(ano) if ano else None
            copias = int(copias) if copias else 1
        except ValueError:
            messagebox.showerror("Erro", "Ano e cópias devem ser números!")
            return
        
        livro = Livro(titulo=titulo, autor=autor, ano=ano, copias_disponiveis=copias)
        
        self.db.adicionar_livro(livro)
        messagebox.showinfo("Sucesso", "Livro cadastrado com sucesso!")
        self.atualizar_lista_livros()
        self.entry_titulo.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.entry_ano.delete(0, tk.END)
        self.entry_copias.delete(0, tk.END)

    def atualizar_lista_livros(self):
        # Limpar a treeview
        for item in self.tree_livros.get_children():
            self.tree_livros.delete(item)
        
        # Adicionar os livros
        livros = self.db.listar_livros()
        for livro in livros:
            self.tree_livros.insert('', tk.END, values=(
                livro.id, livro.titulo, livro.autor, livro.ano, livro.copias_disponiveis
            ))

    def exibir_tela_emprestimo(self):
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Realizar Empréstimo", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Seleção de usuário
        ttk.Label(frame, text="Usuário:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.combo_usuario = ttk.Combobox(frame, state="readonly")
        self.combo_usuario.grid(row=1, column=1, pady=5, sticky=tk.EW)
        
        # Preencher combo de usuários
        usuarios = self.db.listar_usuarios()
        self.combo_usuario['values'] = [(f"{u.id} - {u.nome}") for u in usuarios]
        
        # Seleção de livro
        ttk.Label(frame, text="Livro:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.combo_livro = ttk.Combobox(frame, state="readonly")
        self.combo_livro.grid(row=2, column=1, pady=5, sticky=tk.EW)
        
        # Preencher combo de livros disponíveis
        livros = self.db.listar_livros(disponiveis=True)
        self.combo_livro['values'] = [(f"{l.id} - {l.titulo}") for l in livros]
        
        # Botões
        ttk.Button(frame, text="Realizar Empréstimo", command=self.realizar_emprestimo).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Voltar", command=self.exibir_tela_login).grid(row=4, column=0, columnspan=2, pady=5)

    def realizar_emprestimo(self):
        usuario = self.combo_usuario.get()
        livro = self.combo_livro.get()
        
        if not usuario or not livro:
            messagebox.showerror("Erro", "Selecione usuário e livro!")
            return
        
        id_usuario = int(usuario.split(' - ')[0])
        id_livro = int(livro.split(' - ')[0])
        
        if self.db.realizar_emprestimo(id_usuario, id_livro):
            messagebox.showinfo("Sucesso", "Empréstimo realizado com sucesso!")
            self.exibir_tela_login()
        else:
            messagebox.showerror("Erro", "Não há cópias disponíveis deste livro!")

    def exibir_tela_devolucao(self):
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Registrar Devolução", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Lista de empréstimos ativos
        ttk.Label(frame, text="Empréstimos Ativos:", font=('Arial', 10, 'bold')).grid(row=1, column=0, columnspan=2, pady=10)
        
        columns = ('ID', 'Usuário', 'Livro', 'Data Empréstimo', 'Devolução Prevista')
        self.tree_emprestimos = ttk.Treeview(frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree_emprestimos.heading(col, text=col)
            self.tree_emprestimos.column(col, width=120)
        
        self.tree_emprestimos.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Preencher a lista
        self.atualizar_lista_emprestimos()
        
        # Botões
        ttk.Button(frame, text="Registrar Devolução", command=self.registrar_devolucao).grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(frame, text="Voltar", command=self.exibir_tela_login).grid(row=4, column=0, columnspan=2, pady=5)

    def atualizar_lista_emprestimos(self):
        # Limpar a treeview
        for item in self.tree_emprestimos.get_children():
            self.tree_emprestimos.delete(item)
        
        # Obter empréstimos ativos (sem data de devolução real)
        cursor = self.db.conn.cursor()
        cursor.execute('''
        SELECT e.id, u.nome, l.titulo, e.data_emprestimo, e.data_devolucao_prevista
        FROM emprestimos e
        JOIN usuarios u ON e.id_usuario = u.id
        JOIN livros l ON e.id_livro = l.id
        WHERE e.data_devolucao_real IS NULL
        ''')
        
        for row in cursor.fetchall():
            self.tree_emprestimos.insert('', tk.END, values=row)

    def registrar_devolucao(self):
        selecionado = self.tree_emprestimos.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um empréstimo para devolução!")
            return
        
        item = self.tree_emprestimos.item(selecionado[0])
        id_emprestimo = item['values'][0]
        
        if self.db.realizar_devolucao(id_emprestimo):
            messagebox.showinfo("Sucesso", "Devolução registrada com sucesso!")
            self.atualizar_lista_emprestimos()
        else:
            messagebox.showerror("Erro", "Erro ao registrar devolução!")

    # Métodos para relatórios
    def exibir_livros_disponiveis(self):
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Livros Disponíveis", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=10)
        
        columns = ('ID', 'Título', 'Autor', 'Ano', 'Cópias')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        tree.grid(row=1, column=0, pady=5)
        
        # Preencher a lista
        livros = self.db.listar_livros(disponiveis=True)
        for livro in livros:
            tree.insert('', tk.END, values=(
                livro.id, livro.titulo, livro.autor, livro.ano, livro.copias_disponiveis
            ))
        
        ttk.Button(frame, text="Voltar", command=self.exibir_tela_login).grid(row=2, column=0, pady=10)

    def exibir_livros_emprestados_usuario(self):
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Livros Emprestados por Usuário", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Seleção de usuário
        ttk.Label(frame, text="Usuário:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.combo_usuario_relatorio = ttk.Combobox(frame, state="readonly")
        self.combo_usuario_relatorio.grid(row=1, column=1, pady=5, sticky=tk.EW)
        
        # Preencher combo de usuários
        usuarios = self.db.listar_usuarios()
        self.combo_usuario_relatorio['values'] = [(f"{u.id} - {u.nome}") for u in usuarios]
        
        # Botão para gerar relatório
        ttk.Button(frame, text="Consultar", command=self.gerar_relatorio_emprestimos_usuario).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Treeview para resultados
        columns = ('ID', 'Título', 'Autor', 'Ano')
        self.tree_livros_usuario = ttk.Treeview(frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree_livros_usuario.heading(col, text=col)
            self.tree_livros_usuario.column(col, width=150)
        
        self.tree_livros_usuario.grid(row=3, column=0, columnspan=2, pady=5)
        
        ttk.Button(frame, text="Voltar", command=self.exibir_tela_login).grid(row=4, column=0, columnspan=2, pady=10)

    def gerar_relatorio_emprestimos_usuario(self):
        usuario = self.combo_usuario_relatorio.get()
        if not usuario:
            messagebox.showerror("Erro", "Selecione um usuário!")
            return
        
        # Limpar a treeview
        for item in self.tree_livros_usuario.get_children():
            self.tree_livros_usuario.delete(item)
        
        id_usuario = int(usuario.split(' - ')[0])
        livros = self.db.livros_emprestados_por_usuario(id_usuario)
        
        if not livros:
            messagebox.showinfo("Informação", "Este usuário não possui livros emprestados.")
            return
        
        for livro in livros:
            self.tree_livros_usuario.insert('', tk.END, values=(
                livro.id, livro.titulo, livro.autor, livro.ano
            ))

    def exibir_usuarios_com_atraso(self):
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Usuários com Livros em Atraso", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=10)
        
        columns = ('ID', 'Nome', 'E-mail', 'CPF')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.grid(row=1, column=0, pady=5)
        
        # Preencher a lista
        usuarios = self.db.usuarios_com_atraso()
        for usuario in usuarios:
            tree.insert('', tk.END, values=(
                usuario.id, usuario.nome, usuario.email, usuario.cpf
            ))
        
        if not usuarios:
            ttk.Label(frame, text="Nenhum usuário com livro em atraso.", foreground="green").grid(row=2, column=0, pady=5)
        
        ttk.Button(frame, text="Voltar", command=self.exibir_tela_login).grid(row=3, column=0, pady=10)

    def exibir_emprestimos_periodo(self):
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Empréstimos por Período", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Data inicial
        ttk.Label(frame, text="Data Inicial (AAAA-MM-DD):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_data_inicio = ttk.Entry(frame)
        self.entry_data_inicio.grid(row=1, column=1, pady=5)
        
        # Data final
        ttk.Label(frame, text="Data Final (AAAA-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_data_fim = ttk.Entry(frame)
        self.entry_data_fim.grid(row=2, column=1, pady=5)
        
        # Botão para gerar relatório
        ttk.Button(frame, text="Consultar", command=self.gerar_relatorio_emprestimos_periodo).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Treeview para resultados
        columns = ('ID', 'Usuário', 'Livro', 'Empréstimo', 'Prevista', 'Devolução')
        self.tree_emprestimos_periodo = ttk.Treeview(frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.tree_emprestimos_periodo.heading(col, text=col)
            self.tree_emprestimos_periodo.column(col, width=120)
        
        self.tree_emprestimos_periodo.grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Button(frame, text="Voltar", command=self.exibir_tela_login).grid(row=5, column=0, columnspan=2, pady=10)

    def gerar_relatorio_emprestimos_periodo(self):
        data_inicio = self.entry_data_inicio.get()
        data_fim = self.entry_data_fim.get()
        
        if not data_inicio or not data_fim:
            messagebox.showerror("Erro", "Preencha ambas as datas!")
            return
        
        # Limpar a treeview
        for item in self.tree_emprestimos_periodo.get_children():
            self.tree_emprestimos_periodo.delete(item)
        
        emprestimos = self.db.emprestimos_por_periodo(data_inicio, data_fim)
        
        if not emprestimos:
            messagebox.showinfo("Informação", "Nenhum empréstimo encontrado no período.")
            return
        
        for emp in emprestimos:
            self.tree_emprestimos_periodo.insert('', tk.END, values=(
                emp[0], emp[6], emp[7], emp[3], emp[4], emp[5] if emp[5] else "Pendente"
            ))

    def exibir_media_livros_mes(self):
        self.limpar_tela()
        
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Média de Livros Emprestados por Mês", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=10)
        
        media = self.db.media_livros_por_mes()
        
        ttk.Label(frame, text=f"Média: {media:.2f} livros/mês", font=('Arial', 10)).grid(row=1, column=0, pady=10)
        
        ttk.Button(frame, text="Voltar", command=self.exibir_tela_login).grid(row=2, column=0, pady=10)