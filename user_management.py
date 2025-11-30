# user_management.py

import ttkbootstrap as ttk
from tkinter import messagebox
from usuarios import GestionUsuarios

class UserManagementFrame(ttk.Frame):
    """Frame para la gestión de usuarios (solo para el administrador)."""
    def __init__(self, parent, controller, usuario_actual, nombre_usuario):
        super().__init__(parent)
        self.controller = controller
        self.usuario_actual = usuario_actual
        self.gestion_usuarios = GestionUsuarios()

        self.crear_widgets()
        self.cargar_usuarios_en_treeview()

    def crear_widgets(self):
        # Título
        titulo_label = ttk.Label(self, text="⚙️ Gestión de Usuarios", font=("Helvetica", 20, "bold"))
        titulo_label.pack(pady=20)

        # Frame para los botones
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(button_frame, text="Crear Nuevo Usuario", command=self._abrir_dialogo_crear_usuario, bootstyle="SUCCESS").pack(side="left", padx=5)
        # NUEVO: Botón para cambiar contraseña
        ttk.Button(button_frame, text="Cambiar Contraseña", command=self._abrir_dialogo_cambiar_password, bootstyle="INFO").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar Seleccionado", command=self._eliminar_usuario_seleccionado, bootstyle="DANGER").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Actualizar Lista", command=self.cargar_usuarios_en_treeview, bootstyle="SECONDARY").pack(side="right", padx=5)

        # Frame para la tabla (Treeview)
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Scrollbar para la tabla
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")

        # Crear el Treeview
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, bootstyle="PRIMARY", show="headings")
        self.tree.pack(fill="both", expand=True)
        tree_scroll.config(command=self.tree.yview)

        # Definir las columnas
        self.tree['columns'] = ('id', 'nombre_usuario', 'nombre_completo')
        
        # Formatear las columnas
        self.tree.column("id", anchor="center", width=50)
        self.tree.column("nombre_usuario", anchor="center", width=200)
        self.tree.column("nombre_completo", anchor="w", width=400)

        # Crear los encabezados
        self.tree.heading("id", text="ID", anchor='center')
        self.tree.heading("nombre_usuario", text="Nombre de Usuario", anchor='center')
        self.tree.heading("nombre_completo", text="Nombre Completo", anchor='w')

    def cargar_usuarios_en_treeview(self):
        """Limpia la tabla y la vuelve a llenar con los usuarios de la BD."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        try:
            usuarios = self.gestion_usuarios.obtener_todos_los_usuarios()
            for index, usuario in enumerate(usuarios):
                self.tree.insert(parent='', index='end', iid=index, text='',
                                 values=(usuario['id'], usuario['nombre_usuario'], usuario['nombre_completo']))
        except Exception as e:
            messagebox.showerror("Error al Cargar Usuarios", f"No se pudieron cargar los usuarios.\nError: {e}")

    def _abrir_dialogo_crear_usuario(self):
        """Abre el diálogo para crear un nuevo usuario."""
        CrearUsuarioDialog(self, self.gestion_usuarios, self.cargar_usuarios_en_treeview)

    # NUEVO: Método para abrir el diálogo de cambio de contraseña
    def _abrir_dialogo_cambiar_password(self):
        """Abre el diálogo para cambiar la contraseña de un usuario seleccionado."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Selección Requerida", "Por favor, selecciona un usuario de la lista para cambiar su contraseña.")
            return
        
        item_values = self.tree.item(selected_item, 'values')
        nombre_usuario = item_values[1]
        
        ChangePasswordDialog(self, self.gestion_usuarios, nombre_usuario)

    def _eliminar_usuario_seleccionado(self):
        """Elimina el usuario seleccionado en la tabla."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Selección Requerida", "Por favor, selecciona un usuario de la lista para eliminar.")
            return
        
        item_values = self.tree.item(selected_item, 'values')
        nombre_usuario = item_values[1]
        nombre_completo = item_values[2]

        if self.gestion_usuarios.es_admin(nombre_usuario):
            messagebox.showerror("Acción Denegada", "No se puede eliminar al usuario 'admin'.")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Estás seguro de que quieres eliminar al siguiente usuario?\n\n"
            f"Usuario: {nombre_usuario}\n"
            f"Nombre: {nombre_completo}"
        )

        if confirmacion:
            if self.gestion_usuarios.eliminar_usuario(nombre_usuario):
                messagebox.showinfo("Eliminado", "El usuario fue eliminado correctamente.")
                self.cargar_usuarios_en_treeview()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.")


class CrearUsuarioDialog(ttk.Toplevel):
    """Dialogo para crear un nuevo usuario."""
    def __init__(self, parent, gestion_usuarios, refresh_callback):
        super().__init__(parent)
        self.title("Crear Nuevo Usuario")
        self.geometry("350x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.gestion_usuarios = gestion_usuarios
        self.refresh_callback = refresh_callback

        self.crear_widgets()
        self.centrar_ventana()

    def centrar_ventana(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def crear_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Nombre Completo:").pack(anchor="w", pady=(10, 5))
        self.nombre_completo_entry = ttk.Entry(main_frame, bootstyle="PRIMARY")
        self.nombre_completo_entry.pack(fill="x", pady=(0, 10))

        ttk.Label(main_frame, text="Nombre de Usuario:").pack(anchor="w")
        self.usuario_entry = ttk.Entry(main_frame, bootstyle="PRIMARY")
        self.usuario_entry.pack(fill="x", pady=(0, 10))

        ttk.Label(main_frame, text="Contraseña:").pack(anchor="w")
        self.password_entry = ttk.Entry(main_frame, show="*", bootstyle="PRIMARY")
        self.password_entry.pack(fill="x", pady=(0, 10))

        ttk.Label(main_frame, text="Confirmar Contraseña:").pack(anchor="w")
        self.confirmar_password_entry = ttk.Entry(main_frame, show="*", bootstyle="PRIMARY")
        self.confirmar_password_entry.pack(fill="x", pady=(0, 20))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")
        
        ttk.Button(button_frame, text="Crear", command=self._crear, bootstyle="SUCCESS").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.destroy).pack(side="right", padx=5)

    def _crear(self):
        nombre_completo = self.nombre_completo_entry.get().strip()
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get()
        confirmar_password = self.confirmar_password_entry.get()

        if not all([nombre_completo, usuario, password, confirmar_password]):
            messagebox.showwarning("Campos Vacíos", "Todos los campos son obligatorios.", parent=self)
            return
        
        if password != confirmar_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden.", parent=self)
            return

        if self.gestion_usuarios.crear_usuario(usuario, nombre_completo, password):
            messagebox.showinfo("Éxito", f"Usuario '{usuario}' creado correctamente.", parent=self)
            self.refresh_callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "El nombre de usuario ya está en uso.", parent=self)


# NUEVO: Diálogo para cambiar la contraseña
class ChangePasswordDialog(ttk.Toplevel):
    """Dialogo para cambiar la contraseña de un usuario."""
    def __init__(self, parent, gestion_usuarios, nombre_usuario):
        super().__init__(parent)
        self.title(f"Cambiar Contraseña de: {nombre_usuario}")
        self.geometry("400x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.gestion_usuarios = gestion_usuarios
        self.nombre_usuario = nombre_usuario

        self.crear_widgets()
        self.centrar_ventana()

    def centrar_ventana(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def crear_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Nueva Contraseña:").pack(anchor="w", pady=(10, 5))
        self.nueva_password_entry = ttk.Entry(main_frame, show="*", bootstyle="PRIMARY")
        self.nueva_password_entry.pack(fill="x", pady=(0, 10))

        ttk.Label(main_frame, text="Confirmar Nueva Contraseña:").pack(anchor="w")
        self.confirmar_password_entry = ttk.Entry(main_frame, show="*", bootstyle="PRIMARY")
        self.confirmar_password_entry.pack(fill="x", pady=(0, 20))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")
        
        ttk.Button(button_frame, text="Guardar Cambio", command=self._cambiar, bootstyle="SUCCESS").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.destroy).pack(side="right", padx=5)

    def _cambiar(self):
        nueva_password = self.nueva_password_entry.get()
        confirmar_password = self.confirmar_password_entry.get()

        if not all([nueva_password, confirmar_password]):
            messagebox.showwarning("Campos Vacíos", "La nueva contraseña y su confirmación son obligatorias.", parent=self)
            return
        
        if nueva_password != confirmar_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden.", parent=self)
            return
        
        if len(nueva_password) < 4:
            messagebox.showwarning("Contraseña Débil", "La contraseña debe tener al menos 4 caracteres.", parent=self)
            return

        if self.gestion_usuarios.cambiar_password(self.nombre_usuario, nueva_password):
            messagebox.showinfo("Éxito", f"La contraseña para '{self.nombre_usuario}' ha sido cambiada correctamente.", parent=self)
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo cambiar la contraseña. Inténtelo de nuevo.", parent=self)