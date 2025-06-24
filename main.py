import tkinter as tk
from interface import BibliotecaApp
import logging
import sys
from datetime import datetime

def configure_logging():
    """Configura o sistema de logging."""
    logging.basicConfig(
        filename='biblioteca.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )

def handle_exception(exc_type, exc_value, exc_traceback):
    """Handler para exceções não capturadas."""
    logging.error("Uncaught exception", 
                 exc_info=(exc_type, exc_value, exc_traceback))
    
    from tkinter import messagebox
    messagebox.showerror(
        "Erro inesperado",
        f"Ocorreu um erro não esperado:\n\n{str(exc_value)}\n\n"
        "Detalhes foram registrados no arquivo de log."
    )

def main():
    # Configurações iniciais
    configure_logging()
    sys.excepthook = handle_exception
    
    logging.info("Iniciando aplicação Biblioteca")
    
    # Criar e configurar janela principal
    root = tk.Tk()
    app = BibliotecaApp(root)
    
    # Configurar para fechar corretamente
    def on_closing():
        if tk.messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
            logging.info("Aplicação encerrada pelo usuário")
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()