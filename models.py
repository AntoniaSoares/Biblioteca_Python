class Usuario:
    def __init__(self, id=None, nome=None, email=None, cpf=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf

class Livro:
    def __init__(self, id=None, titulo=None, autor=None, ano=None, copias_disponiveis=None):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.copias_disponiveis = copias_disponiveis

class Emprestimo:
    def __init__(self, id=None, id_usuario=None, id_livro=None, data_emprestimo=None, 
                 data_devolucao_prevista=None, data_devolucao_real=None):
        self.id = id
        self.id_usuario = id_usuario
        self.id_livro = id_livro
        self.data_emprestimo = data_emprestimo
        self.data_devolucao_prevista = data_devolucao_prevista
        self.data_devolucao_real = data_devolucao_real