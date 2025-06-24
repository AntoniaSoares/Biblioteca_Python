import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from contextlib import contextmanager
from models import Usuario, Livro, Emprestimo

class Database:
    def __init__(self, db_name='biblioteca.db'):
        self.db_name = db_name
        self._criar_tabelas()
    
    @contextmanager
    def _get_cursor(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _criar_tabelas(self):
        with self._get_cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT,
                cpf TEXT UNIQUE NOT NULL
            )''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                ano INTEGER,
                copias_disponiveis INTEGER DEFAULT 1,
                UNIQUE(titulo, autor)
            )''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS emprestimos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                livro_id INTEGER NOT NULL,
                data_emprestimo TEXT NOT NULL,
                data_devolucao_prevista TEXT NOT NULL,
                data_devolucao_real TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY (livro_id) REFERENCES livros(id),
                UNIQUE(usuario_id, livro_id, data_devolucao_real)
            )''')
    
    # CRUD Usuários
    def criar_usuario(self, usuario: Usuario) -> int:
        if not usuario.validar_cpf():
            raise ValueError("CPF inválido")
        if not usuario.validar_email():
            raise ValueError("E-mail inválido")
        
        with self._get_cursor() as cursor:
            cursor.execute('''
            INSERT INTO usuarios (nome, email, cpf)
            VALUES (?, ?, ?)
            ''', (usuario.nome, usuario.email, usuario.cpf))
            return cursor.lastrowid
    
    def obter_usuario(self, usuario_id: int) -> Optional[Usuario]:
        with self._get_cursor() as cursor:
            cursor.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
            row = cursor.fetchone()
            return Usuario(**row) if row else None
    
    def atualizar_usuario(self, usuario: Usuario) -> bool:
        if not usuario.validar_cpf():
            raise ValueError("CPF inválido")
        if not usuario.validar_email():
            raise ValueError("E-mail inválido")
        
        with self._get_cursor() as cursor:
            cursor.execute('''
            UPDATE usuarios 
            SET nome = ?, email = ?, cpf = ?
            WHERE id = ?
            ''', (usuario.nome, usuario.email, usuario.cpf, usuario.id))
            return cursor.rowcount > 0
    
    def remover_usuario(self, usuario_id: int) -> bool:
        with self._get_cursor() as cursor:
            cursor.execute('DELETE FROM usuarios WHERE id = ?', (usuario_id,))
            return cursor.rowcount > 0
    
    def listar_usuarios(self) -> List[Usuario]:
        with self._get_cursor() as cursor:
            cursor.execute('SELECT * FROM usuarios ORDER BY nome')
            return [Usuario(**row) for row in cursor.fetchall()]
    
    # CRUD Livros
    def criar_livro(self, livro: Livro) -> int:
        with self._get_cursor() as cursor:
            cursor.execute('''
            INSERT INTO livros (titulo, autor, ano, copias_disponiveis)
            VALUES (?, ?, ?, ?)
            ''', (livro.titulo, livro.autor, livro.ano, livro.copias_disponiveis))
            return cursor.lastrowid
    
    def obter_livro(self, livro_id: int) -> Optional[Livro]:
        with self._get_cursor() as cursor:
            cursor.execute('SELECT * FROM livros WHERE id = ?', (livro_id,))
            row = cursor.fetchone()
            return Livro(**row) if row else None
    
    def atualizar_livro(self, livro: Livro) -> bool:
        with self._get_cursor() as cursor:
            cursor.execute('''
            UPDATE livros 
            SET titulo = ?, autor = ?, ano = ?, copias_disponiveis = ?
            WHERE id = ?
            ''', (livro.titulo, livro.autor, livro.ano, livro.copias_disponiveis, livro.id))
            return cursor.rowcount > 0
    
    def remover_livro(self, livro_id: int) -> bool:
        with self._get_cursor() as cursor:
            cursor.execute('DELETE FROM livros WHERE id = ?', (livro_id,))
            return cursor.rowcount > 0
    
    def listar_livros(self, disponiveis=False) -> List[Livro]:
        with self._get_cursor() as cursor:
            query = 'SELECT * FROM livros'
            if disponiveis:
                query += ' WHERE copias_disponiveis > 0'
            query += ' ORDER BY titulo'
            cursor.execute(query)
            return [Livro(**row) for row in cursor.fetchall()]
    
    # CRUD Empréstimos
    def criar_emprestimo(self, emprestimo: Emprestimo) -> int:
        if not self.validar_emprestimo(emprestimo.usuario_id, emprestimo.livro_id):
            raise ValueError("Empréstimo não permitido")
        
        with self._get_cursor() as cursor:
            # Atualiza cópias disponíveis
            cursor.execute('''
            UPDATE livros 
            SET copias_disponiveis = copias_disponiveis - 1 
            WHERE id = ?
            ''', (emprestimo.livro_id,))
            
            # Cria empréstimo
            cursor.execute('''
            INSERT INTO emprestimos (
                usuario_id, livro_id, data_emprestimo, data_devolucao_prevista
            ) VALUES (?, ?, ?, ?)
            ''', (
                emprestimo.usuario_id,
                emprestimo.livro_id,
                emprestimo.data_emprestimo.strftime('%Y-%m-%d'),
                emprestimo.data_devolucao_prevista.strftime('%Y-%m-%d')
            ))
            return cursor.lastrowid
    
    def validar_emprestimo(self, usuario_id: int, livro_id: int) -> bool:
        """Verifica se o empréstimo é permitido de acordo com as regras de negócio."""
        with self._get_cursor() as cursor:
            # Verifica se o usuário tem empréstimos em atraso
            cursor.execute('''
            SELECT COUNT(*) FROM emprestimos
            WHERE usuario_id = ? 
            AND data_devolucao_real IS NULL
            AND data_devolucao_prevista < date('now')
            ''', (usuario_id,))
            if cursor.fetchone()[0] > 0:
                return False
            
            # Verifica se o usuário já tem 3 empréstimos ativos
            cursor.execute('''
            SELECT COUNT(*) FROM emprestimos
            WHERE usuario_id = ? AND data_devolucao_real IS NULL
            ''', (usuario_id,))
            if cursor.fetchone()[0] >= 3:
                return False
            
            # Verifica se o usuário já tem um exemplar deste livro
            cursor.execute('''
            SELECT COUNT(*) FROM emprestimos
            WHERE usuario_id = ? AND livro_id = ? AND data_devolucao_real IS NULL
            ''', (usuario_id, livro_id))
            if cursor.fetchone()[0] > 0:
                return False
            
            # Verifica se há cópias disponíveis
            cursor.execute('''
            SELECT copias_disponiveis FROM livros WHERE id = ?
            ''', (livro_id,))
            copias = cursor.fetchone()[0]
            return copias > 0
    
    def finalizar_emprestimo(self, emprestimo_id: int) -> bool:
        with self._get_cursor() as cursor:
            # Obtém o livro associado ao empréstimo
            cursor.execute('SELECT livro_id FROM emprestimos WHERE id = ?', (emprestimo_id,))
            livro_id = cursor.fetchone()[0]
            
            # Atualiza cópias disponíveis
            cursor.execute('''
            UPDATE livros 
            SET copias_disponiveis = copias_disponiveis + 1 
            WHERE id = ?
            ''', (livro_id,))
            
            # Registra devolução
            cursor.execute('''
            UPDATE emprestimos 
            SET data_devolucao_real = date('now')
            WHERE id = ?
            ''', (emprestimo_id,))
            return cursor.rowcount > 0
    
    def obter_emprestimo(self, emprestimo_id: int) -> Optional[Emprestimo]:
        with self._get_cursor() as cursor:
            cursor.execute('SELECT * FROM emprestimos WHERE id = ?', (emprestimo_id,))
            row = cursor.fetchone()
            if row:
                return Emprestimo(
                    id=row['id'],
                    usuario_id=row['usuario_id'],
                    livro_id=row['livro_id'],
                    data_emprestimo=datetime.strptime(row['data_emprestimo'], '%Y-%m-%d'),
                    data_devolucao_prevista=datetime.strptime(row['data_devolucao_prevista'], '%Y-%m-%d'),
                    data_devolucao_real=datetime.strptime(row['data_devolucao_real'], '%Y-%m-%d') if row['data_devolucao_real'] else None
                )
            return None
    
    def listar_emprestimos_ativos(self, usuario_id: Optional[int] = None) -> List[Emprestimo]:
        with self._get_cursor() as cursor:
            query = '''
            SELECT e.* FROM emprestimos e
            WHERE e.data_devolucao_real IS NULL
            '''
            params = ()
            
            if usuario_id:
                query += ' AND e.id_usuario = ?'
                params = (usuario_id,)
            
            query += ' ORDER BY e.data_devolucao_prevista'
            cursor.execute(query, params)
            
            return [
                Emprestimo(
                    id=row['id'],
                    usuario_id=row['usuario_id'],
                    livro_id=row['livro_id'],
                    data_emprestimo=datetime.strptime(row['data_emprestimo'], '%Y-%m-%d'),
                    data_devolucao_prevista=datetime.strptime(row['data_devolucao_prevista'], '%Y-%m-%d')
                ) for row in cursor.fetchall()
            ]
    

    