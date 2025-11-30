# dashboard.py

import ttkbootstrap as ttk
from tkinter import messagebox

class DashboardFrame(ttk.Frame):
    def __init__(self, parent, controller, usuario_actual):
        super().__init__(parent)
        self.controller = controller
        self.usuario_actual = usuario_actual

        self.crear_widgets()

    def crear_widgets(self):
        # Título principal con mensaje de bienvenida
        nombre_usuario = self.usuario_actual.get('nombre_completo', 'Usuario')
        titulo_label = ttk.Label(self, text=f"👋 ¡Bienvenido, {nombre_usuario}!", font=("Helvetica", 24, "bold"))
        titulo_label.pack(pady=20)

        # Descripción de la aplicación
        descripcion_texto = (
            "Este sistema te permite gestionar el inventario de baterías de manera eficiente.\n\n"
            "Puedes importar listas de productos desde archivos Excel, exportar el inventario actual "
            "y generar reportes específicos de productos con stock bajo.\n\n"
            "Utiliza el menú 'Módulos' para navegar entre las diferentes secciones de la aplicación."
        )
        
        desc_label = ttk.Label(self, text=descripcion_texto, wraplength=700, justify="center", font=("Helvetica", 12))
        desc_label.pack(pady=20, padx=20)

        # Frame para información del usuario
        # CORRECCIÓN: LabelFrame -> Labelframe
        info_frame = ttk.Labelframe(self, text="Información de la Sesión", padding=20)
        info_frame.pack(pady=20, fill="x", padx=50)

        ttk.Label(info_frame, text=f"Usuario: {self.usuario_actual.get('nombre_usuario')}", font=("Helvetica", 11)).pack(anchor="w")
        ttk.Label(info_frame, text=f"Nombre Completo: {self.usuario_actual.get('nombre_completo')}", font=("Helvetica", 11)).pack(anchor="w")