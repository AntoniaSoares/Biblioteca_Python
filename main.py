import tkinter as tk
from interface import BibliotecaApp

def main():
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.geometry("800x600")
    root.mainloop()

if __name__ == "__main__":
    main()