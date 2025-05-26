import sqlite3
from datetime import datetime, timedelta
from models import Usuario, Livro, Emprestimo

class Database:
    def __init__(self, db_name='biblioteca.db'):
        self.conn = sqlite3.connect(db_name)
        self.criar_tabelas()

    def criar_tabelas(self):
        cursor = self.conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            cpf TEXT UNIQUE NOT NULL
        )
        ''')
        
        # Tabela de livros
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano INTEGER,
            copias_disponiveis INTEGER DEFAULT 1
        )
        ''')
        
        # Tabela de empréstimos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            id_livro INTEGER NOT NULL,
            data_emprestimo TEXT NOT NULL,
            data_devolucao_prevista TEXT NOT NULL,
            data_devolucao_real TEXT,
            FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
            FOREIGN KEY (id_livro) REFERENCES livros(id)
        )
        ''')
        
        self.conn.commit()

    # Métodos para usuários
    def adicionar_usuario(self, usuario):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO usuarios (nome, email, cpf)
        VALUES (?, ?, ?)
        ''', (usuario.nome, usuario.email, usuario.cpf))
        self.conn.commit()
        return cursor.lastrowid

    def listar_usuarios(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM usuarios')
        return [Usuario(*row) for row in cursor.fetchall()]

    # Métodos para livros
    def adicionar_livro(self, livro):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO livros (titulo, autor, ano, copias_disponiveis)
        VALUES (?, ?, ?, ?)
        ''', (livro.titulo, livro.autor, livro.ano, livro.copias_disponiveis))
        self.conn.commit()
        return cursor.lastrowid

    def listar_livros(self, disponiveis=False):
        cursor = self.conn.cursor()
        query = 'SELECT * FROM livros'
        if disponiveis:
            query += ' WHERE copias_disponiveis > 0'
        cursor.execute(query)
        return [Livro(*row) for row in cursor.fetchall()]

    # Métodos para empréstimos
    def realizar_emprestimo(self, id_usuario, id_livro):
        cursor = self.conn.cursor()
        
        # Verifica se há cópias disponíveis
        cursor.execute('SELECT copias_disponiveis FROM livros WHERE id = ?', (id_livro,))
        copias = cursor.fetchone()[0]
        
        if copias <= 0:
            return False
        
        # Atualiza cópias disponíveis
        cursor.execute('''
        UPDATE livros 
        SET copias_disponiveis = copias_disponiveis - 1 
        WHERE id = ?
        ''', (id_livro,))
        
        # Registra empréstimo
        data_emprestimo = datetime.now().strftime('%Y-%m-%d')
        data_devolucao = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        
        cursor.execute('''
        INSERT INTO emprestimos (id_usuario, id_livro, data_emprestimo, data_devolucao_prevista)
        VALUES (?, ?, ?, ?)
        ''', (id_usuario, id_livro, data_emprestimo, data_devolucao))
        
        self.conn.commit()
        return True

    def realizar_devolucao(self, id_emprestimo):
        cursor = self.conn.cursor()
        
        # Obtém dados do empréstimo
        cursor.execute('''
        SELECT id_livro FROM emprestimos WHERE id = ?
        ''', (id_emprestimo,))
        id_livro = cursor.fetchone()[0]
        
        # Atualiza cópias disponíveis
        cursor.execute('''
        UPDATE livros 
        SET copias_disponiveis = copias_disponiveis + 1 
        WHERE id = ?
        ''', (id_livro,))
        
        # Registra devolução
        data_devolucao = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
        UPDATE emprestimos 
        SET data_devolucao_real = ? 
        WHERE id = ?
        ''', (data_devolucao, id_emprestimo))
        
        self.conn.commit()
        return True

    # Métodos para consultas
    def livros_emprestados_por_usuario(self, id_usuario):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT l.* FROM livros l
        JOIN emprestimos e ON l.id = e.id_livro
        WHERE e.id_usuario = ? AND e.data_devolucao_real IS NULL
        ''', (id_usuario,))
        return [Livro(*row) for row in cursor.fetchall()]

    def usuarios_com_atraso(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT u.* FROM usuarios u
        JOIN emprestimos e ON u.id = e.id_usuario
        WHERE e.data_devolucao_real IS NULL 
        AND e.data_devolucao_prevista < date('now')
        ''')
        return [Usuario(*row) for row in cursor.fetchall()]

    def emprestimos_por_periodo(self, data_inicio, data_fim):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT e.*, u.nome, l.titulo 
        FROM emprestimos e
        JOIN usuarios u ON e.id_usuario = u.id
        JOIN livros l ON e.id_livro = l.id
        WHERE e.data_emprestimo BETWEEN ? AND ?
        ''', (data_inicio, data_fim))
        return cursor.fetchall()

    def media_livros_por_mes(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT strftime('%Y-%m', data_emprestimo) as mes, 
               COUNT(*) as total
        FROM emprestimos
        GROUP BY mes
        ''')
        resultados = cursor.fetchall()
        if not resultados:
            return 0
        total = sum(row[1] for row in resultados)
        return total / len(resultados)

    def fechar_conexao(self):
        self.conn.close()