import re
from datetime import datetime, timedelta
from typing import Optional

class Usuario:
    def __init__(
        self, 
        id: Optional[int] = None, 
        nome: Optional[str] = None, 
        email: Optional[str] = None, 
        cpf: Optional[str] = None
    ):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf
    
    def validar_cpf(self) -> bool:
        """Valida o CPF usando algoritmo de verificação."""
        if not self.cpf:
            return False
            
        cpf = re.sub(r'[^0-9]', '', self.cpf)
        
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
            
        # Cálculo dos dígitos verificadores
        for i in range(9, 11):
            soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
            digito = (soma * 10) % 11
            if digito == 10:
                digito = 0
            if str(digito) != cpf[i]:
                return False
        return True
    
    def validar_email(self) -> bool:
        """Valida o formato do e-mail."""
        if not self.email:
            return True  # Email é opcional
            
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, self.email) is not None
    
    def __str__(self) -> str:
        return f"Usuário {self.id}: {self.nome}"

class Livro:
    def __init__(
        self, 
        id: Optional[int] = None, 
        titulo: Optional[str] = None, 
        autor: Optional[str] = None, 
        ano: Optional[int] = None, 
        copias_disponiveis: Optional[int] = None
    ):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.copias_disponiveis = copias_disponiveis or 0
    
    def disponivel(self) -> bool:
        return self.copias_disponiveis > 0
    
    def __str__(self) -> str:
        return f"{self.titulo} ({self.autor}, {self.ano})"

class Emprestimo:
    PRAZO_DEVOLUCAO = 14  # dias
    
    def __init__(
        self, 
        id: Optional[int] = None, 
        usuario_id: Optional[int] = None, 
        livro_id: Optional[int] = None, 
        data_emprestimo: Optional[datetime] = None, 
        data_devolucao_prevista: Optional[datetime] = None, 
        data_devolucao_real: Optional[datetime] = None
    ):
        self.id = id
        self.usuario_id = usuario_id  
        self.livro_id = livro_id    
        self.data_emprestimo = data_emprestimo or datetime.now()
        self.data_devolucao_prevista = data_devolucao_prevista or (
            self.data_emprestimo + timedelta(days=self.PRAZO_DEVOLUCAO)
        )
        self.data_devolucao_real = data_devolucao_real
    
    def esta_atrasado(self) -> bool:
        if self.data_devolucao_real:
            return self.data_devolucao_real > self.data_devolucao_prevista
        return datetime.now() > self.data_devolucao_prevista
    
    def __str__(self) -> str:
        status = "Devolvido" if self.data_devolucao_real else (
            "Atrasado" if self.esta_atrasado() else "Em prazo"
        )
        return f"Empréstimo {self.id} - {status}"