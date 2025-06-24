import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from tkcalendar import DateEntry
from database import Database
from models import Usuario, Livro, Emprestimo

class StyleManager:
    def __init__(self):
        self.colors = {
            "primary": "#2C3E50",
            "secondary": "#3498DB",
            "success": "#2ECC71",
            "danger": "#E74C3C",
            "warning": "#F39C12",
            "info": "#1ABC9C",
            "background": "#ECF0F1",
            "text": "#2C3E50"
        }
        self.setup_styles()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurações gerais
        style.configure('.', background=self.colors['background'])
        style.configure('TFrame', background=self.colors['background'])
        style.configure('TLabel', background=self.colors['background'], foreground=self.colors['text'])
        style.configure('TButton', padding=6, relief="flat", font=('Arial', 10))
        style.configure('Treeview', rowheight=25, font=('Arial', 10))
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        
        # Estilos específicos
        style.configure('Primary.TButton', background=self.colors['primary'], foreground='white')
        style.configure('Success.TButton', background=self.colors['success'], foreground='white')
        style.configure('Danger.TButton', background=self.colors['danger'], foreground='white')
        style.configure('Warning.TButton', background=self.colors['warning'], foreground='white')
        
        style.map('TButton',
            background=[('active', self.colors['secondary'])],
            foreground=[('active', 'white')]
        )

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)
        
        # Configurar estilo
        self.style = StyleManager()
        self.db = Database()
        
        # Configurar layout principal
        self.setup_main_layout()
        self.show_home_screen()
    
    def show_book_screen(self):
        """Exibe a tela de gerenciamento de livros."""
        self.clear_main_frame()
        self.update_status("Carregando cadastro de livros...")
        
        # Frame principal
        book_frame = ttk.Frame(self.main_frame)
        book_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame do formulário
        form_frame = ttk.LabelFrame(book_frame, text="Cadastro de Livro", padding=10)
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campos do formulário
        ttk.Label(form_frame, text="Título:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.book_title_entry = ttk.Entry(form_frame, width=40)
        self.book_title_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Autor:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.book_author_entry = ttk.Entry(form_frame, width=40)
        self.book_author_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Ano:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.book_year_entry = ttk.Entry(form_frame, width=40)
        self.book_year_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Cópias disponíveis:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.book_copies_entry = ttk.Entry(form_frame, width=40)
        self.book_copies_entry.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Botões do formulário
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Salvar", 
            style='Success.TButton',
            command=self.save_book
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Limpar", 
            command=self.clear_book_form
        ).pack(side=tk.LEFT, padx=5)
        
        # Lista de livros
        list_frame = ttk.LabelFrame(book_frame, text="Livros Cadastrados", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('id', 'titulo', 'autor', 'ano', 'copias')
        self.book_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        
        # Configurar colunas
        self.book_tree.heading('id', text='ID')
        self.book_tree.column('id', width=50, anchor=tk.CENTER)
        
        self.book_tree.heading('titulo', text='Título')
        self.book_tree.column('titulo', width=200)
        
        self.book_tree.heading('autor', text='Autor')
        self.book_tree.column('autor', width=150)
        
        self.book_tree.heading('ano', text='Ano')
        self.book_tree.column('ano', width=80, anchor=tk.CENTER)
        
        self.book_tree.heading('copias', text='Cópias')
        self.book_tree.column('copias', width=80, anchor=tk.CENTER)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.book_tree.yview)
        self.book_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.book_tree.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        action_frame = ttk.Frame(list_frame)
        action_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(
            action_frame,
            text="Editar",
            style='Primary.TButton',
            command=self.edit_book
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Excluir",
            style='Danger.TButton',
            command=self.delete_book
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Atualizar",
            command=self.load_books
        ).pack(side=tk.RIGHT, padx=5)
        
        # Carregar livros
        self.load_books()
        self.update_status("Cadastro de livros carregado")

    def load_books(self):
        """Carrega a lista de livros na Treeview."""
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        books = self.db.listar_livros()
        for book in books:
            self.book_tree.insert('', tk.END, values=(
                book.id, book.titulo, book.autor, book.ano or '', book.copias_disponiveis
            ))

    def clear_book_form(self):
        """Limpa o formulário de livro."""
        self.book_title_entry.delete(0, tk.END)
        self.book_author_entry.delete(0, tk.END)
        self.book_year_entry.delete(0, tk.END)
        self.book_copies_entry.delete(0, tk.END)
        self.current_book_id = None

    def save_book(self):
        """Salva ou atualiza um livro."""
        titulo = self.book_title_entry.get().strip()
        autor = self.book_author_entry.get().strip()
        ano = self.book_year_entry.get().strip()
        copias = self.book_copies_entry.get().strip() or "1"
        
        if not titulo or not autor:
            messagebox.showwarning("Aviso", "Título e autor são obrigatórios!")
            return
        try:
            ano = int(ano) if ano else None
            copias = int(copias)
            
            livro = Livro(titulo=titulo, autor=autor, ano=ano, copias_disponiveis=copias)
            
            if hasattr(self, 'current_book_id') and self.current_book_id:
                livro.id = self.current_book_id
                success = self.db.atualizar_livro(livro)
                message = "atualizado"
            else:
                self.db.criar_livro(livro)
                message = "cadastrado"
            
            messagebox.showinfo("Sucesso", f"Livro {message} com sucesso!")
            self.clear_book_form()
            self.load_books()
            self.update_status(f"Livro {message} com sucesso")
            
        except ValueError:
            messagebox.showerror("Erro", "Ano e cópias devem ser números inteiros!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar livro: {str(e)}")
            self.update_status(f"Erro ao salvar livro: {str(e)}")

    def edit_book(self):
        """Preenche o formulário com os dados do livro selecionado."""
        selected = self.book_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um livro para editar!")
            return
        
        item = self.book_tree.item(selected[0])
        book_id, titulo, autor, ano, copias = item['values']
        
        self.current_book_id = book_id
        self.book_title_entry.delete(0, tk.END)
        self.book_title_entry.insert(0, titulo)
        
        self.book_author_entry.delete(0, tk.END)
        self.book_author_entry.insert(0, autor)
        
        self.book_year_entry.delete(0, tk.END)
        if ano:
            self.book_year_entry.insert(0, ano)
        
        self.book_copies_entry.delete(0, tk.END)
        self.book_copies_entry.insert(0, copias)
        
        self.update_status(f"Editando livro: {titulo}")

    def delete_book(self):
        """Exclui o livro selecionado."""
        selected = self.book_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um livro para excluir!")
            return
        
        item = self.book_tree.item(selected[0])
        book_id, titulo, _, _, _ = item['values']
        
        if messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o livro '{titulo}'?",
            icon='warning'
        ):
            try:
                if self.db.remover_livro(book_id):
                    messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
                    self.load_books()
                    self.clear_book_form()
                    self.update_status(f"Livro {titulo} excluído")
                else:
                    messagebox.showerror("Erro", "Não foi possível excluir o livro!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao excluir livro: {str(e)}")
                self.update_status(f"Erro ao excluir livro: {str(e)}")

    def setup_main_layout(self):
        """Configura o layout principal da aplicação."""
        # Barra de status
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status("Sistema iniciado")
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Criar menu
        self.create_menu()
    
    def update_status(self, message: str):
        """Atualiza a barra de status."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"{timestamp} - {message}")
    
    def create_menu(self):
        """Cria a barra de menu principal."""
        menubar = tk.Menu(self.root)
        
        # Menu Cadastros
        cadastro_menu = tk.Menu(menubar, tearoff=0)
        cadastro_menu.add_command(label="Usuários", command=self.show_user_screen)
        cadastro_menu.add_command(label="Livros", command=self.show_book_screen)
        menubar.add_cascade(label="Cadastros", menu=cadastro_menu)
        
        # Menu Operações
        operacoes_menu = tk.Menu(menubar, tearoff=0)
        operacoes_menu.add_command(label="Empréstimos", command=self.show_loan_screen)
        operacoes_menu.add_command(label="Devoluções", command=self.show_return_screen)
        menubar.add_cascade(label="Operações", menu=operacoes_menu)
        
        # Menu Relatórios
        relatorios_menu = tk.Menu(menubar, tearoff=0)
        relatorios_menu.add_command(label="Livros Disponíveis", command=self.show_available_books)
        relatorios_menu.add_command(label="Empréstimos Ativos", command=self.show_active_loans)
        relatorios_menu.add_command(label="Usuários com Atraso", command=self.show_overdue_users)
        menubar.add_cascade(label="Relatórios", menu=relatorios_menu)
        
        # Menu Ajuda
        ajuda_menu = tk.Menu(menubar, tearoff=0)
        ajuda_menu.add_command(label="Sobre", command=self.show_about)
        menubar.add_cascade(label="Ajuda", menu=ajuda_menu)
        
        self.root.config(menu=menubar)
    
    def show_loan_screen(self):
        """Exibe a tela de empréstimos de livros."""
        self.clear_main_frame()
        self.update_status("Carregando tela de empréstimos...")
        
        # Frame principal
        loan_frame = ttk.Frame(self.main_frame)
        loan_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(
            loan_frame, 
            text="Realizar Novo Empréstimo",
            font=('Arial', 12, 'bold'),
            foreground=self.style.colors['primary']
        ).pack(pady=(0, 10))
        
        # Frame do formulário
        form_frame = ttk.Frame(loan_frame)
        form_frame.pack(fill=tk.X, pady=5)
        
        # Seleção de usuário
        ttk.Label(form_frame, text="Usuário:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.loan_user_combo = ttk.Combobox(form_frame, state="readonly")
        self.loan_user_combo.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Seleção de livro
        ttk.Label(form_frame, text="Livro disponível:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.loan_book_combo = ttk.Combobox(form_frame, state="readonly")
        self.loan_book_combo.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Carregar combos
        self.load_loan_combos()
        
        # Botão de empréstimo
        ttk.Button(
            loan_frame,
            text="Registrar Empréstimo",
            style='Success.TButton',
            command=self.register_loan
        ).pack(pady=10)
        
        # Lista de empréstimos ativos
        list_frame = ttk.LabelFrame(loan_frame, text="Empréstimos Ativos", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('id', 'usuario', 'livro', 'data', 'devolucao')
        self.loan_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        
        # Configurar colunas
        self.loan_tree.heading('id', text='ID')
        self.loan_tree.column('id', width=50, anchor=tk.CENTER)
        
        self.loan_tree.heading('usuario', text='Usuário')
        self.loan_tree.column('usuario', width=150)
        
        self.loan_tree.heading('livro', text='Livro')
        self.loan_tree.column('livro', width=200)
        
        self.loan_tree.heading('data', text='Data Empréstimo')
        self.loan_tree.column('data', width=100, anchor=tk.CENTER)
        
        self.loan_tree.heading('devolucao', text='Devolução Prevista')
        self.loan_tree.column('devolucao', width=120, anchor=tk.CENTER)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.loan_tree.yview)
        self.loan_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.loan_tree.pack(fill=tk.BOTH, expand=True)
    
        # Carregar empréstimos
        self.load_active_loans()
        self.update_status("Tela de empréstimos carregada")

    def load_loan_combos(self):
        """Carrega os comboboxes de usuário e livros disponíveis."""
        users = self.db.listar_usuarios()
        self.loan_user_combo['values'] = [f"{u.id} - {u.nome}" for u in users]
        
        books = self.db.listar_livros(disponiveis=True)
        self.loan_book_combo['values'] = [f"{b.id} - {b.titulo}" for b in books]

    def load_active_loans(self):
        """Carrega a lista de empréstimos ativos."""
        for item in self.loan_tree.get_children():
            self.loan_tree.delete(item)
        
        loans = self.db.listar_emprestimos_ativos()
        for loan in loans:
            user = self.db.obter_usuario(loan.usuario_id)
            book = self.db.obter_livro(loan.livro_id)
            
            self.loan_tree.insert('', tk.END, values=(
                loan.id,
                user.nome if user else "Desconhecido",
                book.titulo if book else "Desconhecido",
                loan.data_emprestimo.strftime('%d/%m/%Y'),
                loan.data_devolucao_prevista.strftime('%d/%m/%Y')
            ))

    def register_loan(self):
        """Registra um novo empréstimo."""
        user = self.loan_user_combo.get()
        book = self.loan_book_combo.get()
        
        if not user or not book:
            messagebox.showwarning("Aviso", "Selecione usuário e livro!")
            return
        
        try:
            user_id = int(user.split(' - ')[0])
            book_id = int(book.split(' - ')[0])
            
            emprestimo = Emprestimo(usuario_id=user_id, livro_id=book_id)
            self.db.criar_emprestimo(emprestimo)
            
            messagebox.showinfo("Sucesso", "Empréstimo registrado com sucesso!")
            self.load_active_loans()
            self.load_loan_combos()
            self.update_status("Novo empréstimo registrado")
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao processar empréstimo: {str(e)}")
            self.update_status(f"Erro ao registrar empréstimo: {str(e)}")

    def clear_main_frame(self):
        """Limpa o frame principal."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_home_screen(self):
        """Exibe a tela inicial."""
        self.clear_main_frame()
        
        # Frame de boas-vindas
        welcome_frame = ttk.Frame(self.main_frame)
        welcome_frame.pack(expand=True, pady=50)
        
        ttk.Label(
            welcome_frame, 
            text="Sistema de Gerenciamento de Biblioteca",
            font=('Arial', 16, 'bold'),
            foreground=self.style.colors['primary']
        ).pack(pady=20)
        
        ttk.Label(
            welcome_frame,
            text="Selecione uma opção no menu acima para começar",
            font=('Arial', 12)
        ).pack(pady=10)
        
        self.update_status("Tela inicial carregada")
    
    # [Implementações das outras telas seguindo o mesmo padrão moderno...]
    # Implementações completas disponíveis no código final
    
    def show_user_screen(self):
        """Exibe a tela de gerenciamento de usuários."""
        self.clear_main_frame()
        self.update_status("Carregando cadastro de usuários...")
        
        # Frame principal
        user_frame = ttk.Frame(self.main_frame)
        user_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame do formulário
        form_frame = ttk.LabelFrame(user_frame, text="Cadastro de Usuário", padding=10)
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campos do formulário
        ttk.Label(form_frame, text="Nome completo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.user_name_entry = ttk.Entry(form_frame, width=40)
        self.user_name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="E-mail:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.user_email_entry = ttk.Entry(form_frame, width=40)
        self.user_email_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="CPF:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.user_cpf_entry = ttk.Entry(form_frame, width=40)
        self.user_cpf_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Botões do formulário
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Salvar", 
            style='Success.TButton',
            command=self.save_user
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Limpar", 
            command=self.clear_user_form
        ).pack(side=tk.LEFT, padx=5)
        
        # Lista de usuários
        list_frame = ttk.LabelFrame(user_frame, text="Usuários Cadastrados", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('id', 'nome', 'email', 'cpf')
        self.user_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        
        # Configurar colunas
        self.user_tree.heading('id', text='ID')
        self.user_tree.column('id', width=50, anchor=tk.CENTER)
        
        self.user_tree.heading('nome', text='Nome')
        self.user_tree.column('nome', width=200)
        
        self.user_tree.heading('email', text='E-mail')
        self.user_tree.column('email', width=150)
        
        self.user_tree.heading('cpf', text='CPF')
        self.user_tree.column('cpf', width=120, anchor=tk.CENTER)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.user_tree.yview)
        self.user_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.user_tree.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        action_frame = ttk.Frame(list_frame)
        action_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(
            action_frame,
            text="Editar",
            style='Primary.TButton',
            command=self.edit_user
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Excluir",
            style='Danger.TButton',
            command=self.delete_user
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Atualizar",
            command=self.load_users
        ).pack(side=tk.RIGHT, padx=5)
        
        # Carregar usuários
        self.load_users()
        self.update_status("Cadastro de usuários carregado")
    
    def load_users(self):
        """Carrega a lista de usuários na Treeview."""
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        users = self.db.listar_usuarios()
        for user in users:
            self.user_tree.insert('', tk.END, values=(
                user.id, user.nome, user.email or '', user.cpf
            ))
    
    def clear_user_form(self):
        """Limpa o formulário de usuário."""
        self.user_name_entry.delete(0, tk.END)
        self.user_email_entry.delete(0, tk.END)
        self.user_cpf_entry.delete(0, tk.END)
        self.current_user_id = None
    
    def save_user(self):
        """Salva ou atualiza um usuário."""
        nome = self.user_name_entry.get().strip()
        email = self.user_email_entry.get().strip() or None
        cpf = self.user_cpf_entry.get().strip()
        
        if not nome or not cpf:
            messagebox.showwarning("Aviso", "Nome e CPF são obrigatórios!")
            return
        
        user = Usuario(nome=nome, email=email, cpf=cpf)
        
        try:
            if not user.validar_cpf():
                raise ValueError("CPF inválido")
            
            if email and not user.validar_email():
                raise ValueError("E-mail inválido")
            
            if hasattr(self, 'current_user_id') and self.current_user_id:
                user.id = self.current_user_id
                success = self.db.atualizar_usuario(user)
                message = "atualizado"
            else:
                self.db.criar_usuario(user)
                message = "cadastrado"
            
            messagebox.showinfo("Sucesso", f"Usuário {message} com sucesso!")
            self.clear_user_form()
            self.load_users()
            self.update_status(f"Usuário {message} com sucesso")
            
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            self.update_status(f"Erro ao salvar usuário: {str(e)}")
    
    def edit_user(self):
        """Preenche o formulário com os dados do usuário selecionado."""
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar!")
            return
        
        item = self.user_tree.item(selected[0])
        user_id, nome, email, cpf = item['values']
        
        self.current_user_id = user_id
        self.user_name_entry.delete(0, tk.END)
        self.user_name_entry.insert(0, nome)
        
        self.user_email_entry.delete(0, tk.END)
        if email:
            self.user_email_entry.insert(0, email)
        
        self.user_cpf_entry.delete(0, tk.END)
        self.user_cpf_entry.insert(0, cpf)
        
        self.update_status(f"Editando usuário: {nome}")
    
    def delete_user(self):
        """Exclui o usuário selecionado."""
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um usuário para excluir!")
            return
        
        item = self.user_tree.item(selected[0])
        user_id, nome, _, _ = item['values']
        
        if messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o usuário {nome}?",
            icon='warning'
        ):
            try:
                if self.db.remover_usuario(user_id):
                    messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
                    self.load_users()
                    self.clear_user_form()
                    self.update_status(f"Usuário {nome} excluído")
                else:
                    messagebox.showerror("Erro", "Não foi possível excluir o usuário!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao excluir usuário: {str(e)}")
                self.update_status(f"Erro ao excluir usuário: {str(e)}")

    def show_return_screen(self):
        """Exibe a tela de devolução de livros."""
        self.clear_main_frame()
        self.update_status("Carregando tela de devoluções...")
        
        # Frame principal
        return_frame = ttk.Frame(self.main_frame)
        return_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(
            return_frame, 
            text="Registrar Devolução",
            font=('Arial', 12, 'bold'),
            foreground=self.style.colors['primary']
        ).pack(pady=(0, 10))
        
        # Lista de empréstimos ativos
        list_frame = ttk.LabelFrame(return_frame, text="Empréstimos Ativos", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('id', 'usuario', 'livro', 'data', 'devolucao', 'status')
        self.return_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        
        # Configurar colunas
        self.return_tree.heading('id', text='ID')
        self.return_tree.column('id', width=50, anchor=tk.CENTER)
        
        self.return_tree.heading('usuario', text='Usuário')
        self.return_tree.column('usuario', width=150)
        
        self.return_tree.heading('livro', text='Livro')
        self.return_tree.column('livro', width=200)
        
        self.return_tree.heading('data', text='Data Empréstimo')
        self.return_tree.column('data', width=100, anchor=tk.CENTER)
        
        self.return_tree.heading('devolucao', text='Devolução Prevista')
        self.return_tree.column('devolucao', width=120, anchor=tk.CENTER)
        
        self.return_tree.heading('status', text='Status')
        self.return_tree.column('status', width=100, anchor=tk.CENTER)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.return_tree.yview)
        self.return_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.return_tree.pack(fill=tk.BOTH, expand=True)
        
        # Botão de devolução
        ttk.Button(
            list_frame,
            text="Registrar Devolução",
            style='Success.TButton',
            command=self.register_return
        ).pack(pady=10)
        
        # Carregar empréstimos
        self.load_returns()
        self.update_status("Tela de devoluções carregada")

    def load_returns(self):
        """Carrega a lista de empréstimos para devolução."""
        for item in self.return_tree.get_children():
            self.return_tree.delete(item)
        
        loans = self.db.listar_emprestimos_ativos()
        for loan in loans:
            user = self.db.obter_usuario(loan.usuario_id)
            book = self.db.obter_livro(loan.livro_id)
            
            status = "Atrasado" if loan.esta_atrasado() else "No prazo"
            
            self.return_tree.insert('', tk.END, values=(
                loan.id,
                user.nome if user else "Desconhecido",
                book.titulo if book else "Desconhecido",
                loan.data_emprestimo.strftime('%d/%m/%Y'),
                loan.data_devolucao_prevista.strftime('%d/%m/%Y'),
                status
            ))
    def show_available_books(self):
        """Exibe a lista de livros disponíveis para empréstimo."""
        self.clear_main_frame()
        self.update_status("Carregando livros disponíveis...")
        
        # Frame principal
        avail_frame = ttk.Frame(self.main_frame)
        avail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(
            avail_frame,
            text="Livros Disponíveis para Empréstimo",
            font=('Arial', 12, 'bold'),
            foreground=self.style.colors['primary']
        ).pack(pady=(0, 10))
        
        # Lista de livros
        list_frame = ttk.Frame(avail_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('id', 'titulo', 'autor', 'ano', 'copias')
        self.avail_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            selectmode='extended'
        )
        
        # Configurar colunas
        self.avail_tree.heading('id', text='ID')
        self.avail_tree.column('id', width=50, anchor=tk.CENTER)
        
        self.avail_tree.heading('titulo', text='Título')
        self.avail_tree.column('titulo', width=250)
        
        self.avail_tree.heading('autor', text='Autor')
        self.avail_tree.column('autor', width=150)
        
        self.avail_tree.heading('ano', text='Ano')
        self.avail_tree.column('ano', width=80, anchor=tk.CENTER)
        
        self.avail_tree.heading('copias', text='Cópias Disp.')
        self.avail_tree.column('copias', width=100, anchor=tk.CENTER)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.avail_tree.yview)
        self.avail_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.avail_tree.pack(fill=tk.BOTH, expand=True)
        
        # Botão de atualizar
        ttk.Button(
            avail_frame,
            text="Atualizar Lista",
            command=self.load_available_books
        ).pack(pady=10)
        
        # Carregar dados
        self.load_available_books()
        self.update_status("Lista de livros disponíveis carregada")

    def load_available_books(self):
        """Carrega os livros disponíveis na Treeview."""
        for item in self.avail_tree.get_children():
            self.avail_tree.delete(item)
        
        books = self.db.listar_livros(disponiveis=True)
        for book in books:
            self.avail_tree.insert('', tk.END, values=(
                book.id,
                book.titulo,
                book.autor,
                book.ano if book.ano else '',
                book.copias_disponiveis
            ))

    def register_return(self):
        """Registra a devolução de um livro."""
        selected = self.return_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um empréstimo para devolver!")
            return
        
        item = self.return_tree.item(selected[0])
        loan_id = item['values'][0]
        
        try:
            if self.db.finalizar_emprestimo(loan_id):
                messagebox.showinfo("Sucesso", "Devolução registrada com sucesso!")
                self.load_returns()
                self.update_status("Devolução registrada")
            else:
                messagebox.showerror("Erro", "Não foi possível registrar a devolução!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar devolução: {str(e)}")
            self.update_status(f"Erro ao registrar devolução: {str(e)}")
   
    def show_active_loans(self):
        """Exibe a lista de empréstimos ativos."""
        self.clear_main_frame()
        self.update_status("Carregando empréstimos ativos...")
        
        # Frame principal
        loans_frame = ttk.Frame(self.main_frame)
        loans_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(
            loans_frame,
            text="Empréstimos Ativos",
            font=('Arial', 12, 'bold'),
            foreground=self.style.colors['primary']
        ).pack(pady=(0, 10))
        
        # Lista de empréstimos
        list_frame = ttk.Frame(loans_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('id', 'usuario', 'livro', 'data_emp', 'data_dev', 'status')
        self.loans_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            selectmode='extended'
        )
        
        # Configurar colunas
        self.loans_tree.heading('id', text='ID')
        self.loans_tree.column('id', width=50, anchor=tk.CENTER)
        
        self.loans_tree.heading('usuario', text='Usuário')
        self.loans_tree.column('usuario', width=150)
        
        self.loans_tree.heading('livro', text='Livro')
        self.loans_tree.column('livro', width=200)
        
        self.loans_tree.heading('data_emp', text='Data Empréstimo')
        self.loans_tree.column('data_emp', width=100, anchor=tk.CENTER)
        
        self.loans_tree.heading('data_dev', text='Devolução Prevista')
        self.loans_tree.column('data_dev', width=120, anchor=tk.CENTER)
        
        self.loans_tree.heading('status', text='Status')
        self.loans_tree.column('status', width=100, anchor=tk.CENTER)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.loans_tree.yview)
        self.loans_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.loans_tree.pack(fill=tk.BOTH, expand=True)
        
        # Botão de atualizar
        ttk.Button(
            loans_frame,
            text="Atualizar Lista",
            command=self.load_active_loans_report
        ).pack(pady=10)
        
        # Carregar dados
        self.load_active_loans_report()
        self.update_status("Lista de empréstimos ativos carregada")

    def load_active_loans_report(self):
        """Carrega os empréstimos ativos na Treeview."""
        for item in self.loans_tree.get_children():
            self.loans_tree.delete(item)
        
        loans = self.db.listar_emprestimos_ativos()
        for loan in loans:
            user = self.db.obter_usuario(loan.usuario_id)
            book = self.db.obter_livro(loan.livro_id)
            
            status = "Atrasado" if loan.esta_atrasado() else "No prazo"
            
            self.loans_tree.insert('', tk.END, values=(
                loan.id,
                user.nome if user else "Desconhecido",
                book.titulo if book else "Desconhecido",
                loan.data_emprestimo.strftime('%d/%m/%Y'),
                loan.data_devolucao_prevista.strftime('%d/%m/%Y'),
                status
            ))

    def show_overdue_users(self):
        """Exibe a lista de usuários com empréstimos em atraso."""
        self.clear_main_frame()
        self.update_status("Carregando usuários com atraso...")
        
        # Frame principal
        overdue_frame = ttk.Frame(self.main_frame)
        overdue_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(
            overdue_frame,
            text="Usuários com Empréstimos em Atraso",
            font=('Arial', 12, 'bold'),
            foreground=self.style.colors['primary']
        ).pack(pady=(0, 10))
        
        # Lista de usuários
        list_frame = ttk.Frame(overdue_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('id', 'nome', 'email', 'cpf', 'qtd_atrasos')
        self.overdue_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show='headings',
            selectmode='extended'
        )
        
        # Configurar colunas
        self.overdue_tree.heading('id', text='ID')
        self.overdue_tree.column('id', width=50, anchor=tk.CENTER)
        
        self.overdue_tree.heading('nome', text='Nome')
        self.overdue_tree.column('nome', width=150)
        
        self.overdue_tree.heading('email', text='E-mail')
        self.overdue_tree.column('email', width=150)
        
        self.overdue_tree.heading('cpf', text='CPF')
        self.overdue_tree.column('cpf', width=120, anchor=tk.CENTER)
        
        self.overdue_tree.heading('qtd_atrasos', text='Qtd. Atrasos')
        self.overdue_tree.column('qtd_atrasos', width=100, anchor=tk.CENTER)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.overdue_tree.yview)
        self.overdue_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.overdue_tree.pack(fill=tk.BOTH, expand=True)
        
        # Botão de atualizar
        ttk.Button(
            overdue_frame,
            text="Atualizar Lista",
            command=self.load_overdue_users
        ).pack(pady=10)
        
        # Carregar dados
        self.load_overdue_users()
        self.update_status("Lista de usuários com atraso carregada")

    def load_overdue_users(self):
        """Carrega os usuários com empréstimos em atraso."""
        for item in self.overdue_tree.get_children():
            self.overdue_tree.delete(item)
        
        with self.db._get_cursor() as cursor:
            cursor.execute('''
            SELECT u.id, u.nome, u.email, u.cpf, COUNT(e.id) as qtd_atrasos
            FROM usuarios u
            JOIN emprestimos e ON u.id = e.usuario_id
            WHERE e.data_devolucao_real IS NULL 
            AND e.data_devolucao_prevista < date('now')
            GROUP BY u.id
            ORDER BY qtd_atrasos DESC
            ''')
            
            for row in cursor.fetchall():
                self.overdue_tree.insert('', tk.END, values=(
                    row['id'],
                    row['nome'],
                    row['email'] or '',
                    row['cpf'],
                    row['qtd_atrasos']
                ))
    def show_about(self):
        """Exibe a janela 'Sobre' com informações do sistema."""
        self.clear_main_frame()
        self.update_status("Exibindo informações sobre o sistema...")
        
        # Frame principal
        about_frame = ttk.Frame(self.main_frame, padding=20)
        about_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Title
        ttk.Label(
            about_frame,
            text="Sistema de Gerenciamento de Biblioteca",
            font=('Arial', 16, 'bold'),
            foreground=self.style.colors['primary']
        ).pack(pady=(0, 20))
        
        # Informações do sistema
        info_frame = ttk.Frame(about_frame)
        info_frame.pack(fill=tk.X, pady=10)
        
        infos = [
            ("Versão", "1.0.0"),
            ("Maria Antonia Soares Felix", "Sua Biblioteca Digital"),
            ("Data de Lançamento", "2025"),
            ("Tecnologias", "Python, Tkinter, SQLite"),
            ("Licença", "MIT License")
        ]
        
        for i, (label, value) in enumerate(infos):
            ttk.Label(
                info_frame,
                text=f"{label}:",
                font=('Arial', 10, 'bold'),
                foreground=self.style.colors['primary']
            ).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            
            ttk.Label(
                info_frame,
                text=value,
                font=('Arial', 10)
            ).grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Texto descritivo
        desc_text = """
        Este sistema foi desenvolvido para gerenciar os empréstimos
        e devoluções de livros em bibliotecas de pequeno e médio porte.
        
        Funcionalidades incluem:
        - Cadastro de usuários e livros
        - Controle de empréstimos e devoluções
        - Relatórios e estatísticas
        """
        
        ttk.Label(
            about_frame,
            text=desc_text,
            font=('Arial', 10),
            justify=tk.LEFT
        ).pack(pady=20)
        
        # Botão OK
        ttk.Button(
            about_frame,
            text="OK",
            style='Primary.TButton',
            command=self.show_home_screen,
            width=10
        ).pack(pady=10)

                
        self.update_status("Informações sobre o sistema exibidas") 
   
    def show_license(self):
        """Exibe o texto completo da licença."""
        license_text = """
        MIT License

        Copyright (c) 2025 Sua Biblioteca Digital
        
        Permissão é concedida [... texto completo da licença ...]
        """
        messagebox.showinfo("Licença", license_text)

    def show_credits(self):
        """Exibe os créditos de desenvolvimento."""
        credits = """
        Desenvolvido por:
        - Maria Antonia Soares Felix
    
        
        Agradecimentos especiais:
        - À comunidade Python
        - Aos usuários do sistema
        """
        messagebox.showinfo("Créditos", credits)
        
    def main():
        root = tk.Tk()
        app = BibliotecaApp(root)
        root.mainloop()

    if __name__ == "__main__":
        main()