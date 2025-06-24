# 📚 Sistema de Biblioteca em Python

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)

Um sistema desktop completo para gerenciamento de bibliotecas, com cadastro de usuários, livros, empréstimos e relatórios.

## 🚀 Funcionalidades

- **Cadastro de Usuários**
  - Validação de CPF e e-mail
  - CRUD completo

- **Gestão de Livros**
  - Controle de cópias disponíveis
  - Busca por título/autor

- **Empréstimos/Devoluções**
  - Prazos automáticos (14 dias)
  - Bloqueio por atrasos

- **Relatórios**
  - Livros disponíveis
  - Usuários com atrasos

## 🛠️ Tecnologias

- **Backend**
  - Python 3.9+
  - SQLite (banco de dados)
  - Logging (registro de atividades)

- **Frontend**
  - Tkinter (interface gráfica)
  - tkcalendar (seleção de datas)

## 🗃️ Estrutura do Projeto

biblioteca/
├── main.py # Ponto de entrada
├── database.py # Operações com banco de dados
├── models.py # Regras de negócio
├── interface.py # Telas gráficas
└── biblioteca.db # Banco de dados (gerado automaticamente)

## 📦 Pré-requisitos

- Python 3.9+
- Dependências:
  ```bash
  pip install tkcalendar

🖥️ Como Executar

1. Clone o repositório:
git clone https://github.com/seu-usuario/biblioteca-python.git

2. Execute o sistema:
python main.py

👩‍💻 Autoria
Desenvolvido por Maria Antonia Soares Felix.
Ciência da Computação 2025
