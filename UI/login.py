import tkinter as tk
from tkinter import messagebox, font
import sys
from pathlib import Path

# Adiciona o diretório pai ao path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from User.SDB_User import check_user_credentials


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Horse - Login")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")
        
        # Centraliza a janela na tela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Define fontes
        title_font = font.Font(family="Helvetica", size=32, weight="bold")
        label_font = font.Font(family="Helvetica", size=12, weight="bold")
        button_font = font.Font(family="Helvetica", size=11, weight="bold")
        
        # Frame principal com padding
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=30)
        
        # Título "data_horse"
        title_label = tk.Label(
            main_frame,
            text="data_horse",
            font=title_font,
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        title_label.pack(pady=(0, 40))
        
        # Label e entrada para Nome de Usuário
        name_label = tk.Label(
            main_frame,
            text="Name",
            font=label_font,
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        name_label.pack(anchor="w", pady=(10, 5))
        
        self.name_entry = tk.Entry(
            main_frame,
            font=("Helvetica", 11),
            width=30,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightcolor="#3498db"
        )
        self.name_entry.pack(fill=tk.X, pady=(0, 20))
        self.name_entry.bind("<Return>", lambda e: self.login())
        
        # Label e entrada para Senha
        password_label = tk.Label(
            main_frame,
            text="Password",
            font=label_font,
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        password_label.pack(anchor="w", pady=(10, 5))
        
        self.password_entry = tk.Entry(
            main_frame,
            font=("Helvetica", 11),
            width=30,
            show="*",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightcolor="#3498db"
        )
        self.password_entry.pack(fill=tk.X, pady=(0, 30))
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Botão Login
        login_button = tk.Button(
            main_frame,
            text="Login",
            font=button_font,
            fg="white",
            bg="#3498db",
            activebackground="#2980b9",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=50,
            pady=10,
            command=self.login
        )
        login_button.pack(fill=tk.X, pady=(20, 0))
        
        # Foca no campo de nome ao iniciar
        self.name_entry.focus()
    
    def login(self):
        """Valida as credenciais e faz login."""
        username = self.name_entry.get().strip()
        password = self.password_entry.get()
        
        # Validação básica
        if not username or not password:
            messagebox.showwarning(
                "Aviso",
                "Por favor, preencha os campos de usuário e senha."
            )
            return
        
        # Verifica credenciais
        user = check_user_credentials(username, password)
        
        if user:
            messagebox.showinfo(
                "Sucesso",
                f"Bem-vindo, {user.username}!\nPapel: {user.role.name}"
            )
            # Aqui você pode adicionar a lógica para ir para a próxima tela
            # self.root.destroy()
        else:
            messagebox.showerror(
                "Erro de Login",
                "Usuário ou senha incorretos."
            )
            self.password_entry.delete(0, tk.END)
            self.name_entry.focus()


def main():
    """Inicia a aplicação de login."""
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
