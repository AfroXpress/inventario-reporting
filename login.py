# login.py

import ttkbootstrap as ttk
from tkinter import messagebox
from usuarios import GestionUsuarios

class LoginFrame(ttk.Frame):
    """Frame de inicio de sesión que puede ser embebido."""
    def __init__(self, parent, controller, on_success_callback):
        super().__init__(parent)
        self.controller = controller
        self.on_success_callback = on_success_callback
        
        self.gestion_usuarios = GestionUsuarios()
        
        self.crear_widgets()

    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Título
        titulo_label = ttk.Label(main_frame, text="Sistema de Inventario", font=("Helvetica", 20, "bold"))
        titulo_label.pack(pady=(0, 20))

        # Campo de Usuario
        usuario_label = ttk.Label(main_frame, text="Nombre de Usuario:")
        usuario_label.pack(anchor="w", pady=(10, 5))
        self.usuario_entry = ttk.Entry(main_frame, bootstyle="PRIMARY")
        self.usuario_entry.pack(fill="x", pady=(0, 10))
        self.usuario_entry.focus_set()

        # Campo de Contraseña
        password_label = ttk.Label(main_frame, text="Contraseña:")
        password_label.pack(anchor="w")
        self.password_entry = ttk.Entry(main_frame, show="*", bootstyle="PRIMARY")
        self.password_entry.pack(fill="x", pady=(0, 20))

        # Botón de Login
        login_button = ttk.Button(main_frame, text="Iniciar Sesión", command=self._login, bootstyle="SUCCESS")
        login_button.pack(fill="x", pady=5)
        
        # Información del admin
        info_label = ttk.Label(main_frame, text="Usuario por defecto: admin / admin", font=("Helvetica", 9), foreground="gray")
        info_label.pack(pady=(10, 0))

    def _login(self):
        """Maneja la lógica de inicio de sesión."""
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingresa usuario y contraseña.")
            return

        datos_usuario = self.gestion_usuarios.verificar_usuario(usuario, password)
        
        if datos_usuario:
            messagebox.showinfo("Bienvenido", f"¡Hola, {datos_usuario['nombre_completo']}!")
            # Llama a la función de callback para notificar a la ventana principal
            self.on_success_callback(datos_usuario)
        else:
            messagebox.showerror("Error de Autenticación", "Usuario o contraseña incorrectos.")
            self.password_entry.delete(0, 'end')