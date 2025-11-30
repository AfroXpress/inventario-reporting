# main.py
#Copyright (c) 2025 Roberto Gómez Gonzalez <redescryptogomez@gmail.com>
#https://github.com/AfroXpress

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttkb
from dashboard import DashboardFrame
from inventario import InventarioFrame
from login import LoginFrame
from user_management import UserManagementFrame
from alerts import AlertsFrame
from settings import SettingsDialog
from history import HistoryDialog # <-- NUEVA IMPORTACIÓN
from usuarios import GestionUsuarios
from config import load_settings

class App(ttkb.Window):
    def __init__(self):
        settings = load_settings()
        theme_name = settings.get("theme", "superhero")
        
        super().__init__(themename=theme_name)
        
        self.usuario_actual = None

        self.container = ttkb.Frame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.crear_frames()
        self.mostrar_frame("Login")

    def crear_frames(self):
        self.frames["Login"] = LoginFrame(self.container, self, self.on_login_success)
        self.frames["Login"].grid(row=0, column=0, sticky="nsew")
        
        self.frames["Dashboard"] = None
        self.frames["Inventario"] = None
        self.frames["UserManagement"] = None
        self.frames["Alerts"] = None

    def crear_frames_principales(self):
        self.frames["Dashboard"] = DashboardFrame(self.container, self, self.usuario_actual)
        self.frames["Dashboard"].grid(row=0, column=0, sticky="nsew")

        # CAMBIO: Pasar el usuario actual al crear el frame de Inventario
        self.frames["Inventario"] = InventarioFrame(self.container, self, self.usuario_actual, self.usuario_actual['nombre_usuario'])
        self.frames["Inventario"].grid(row=0, column=0, sticky="nsew")

        self.frames["Alerts"] = AlertsFrame(self.container, self, self.usuario_actual)
        self.frames["Alerts"].grid(row=0, column=0, sticky="nsew")

        gestor = GestionUsuarios()
        if gestor.es_admin(self.usuario_actual['nombre_usuario']):
            # CAMBIO: Pasar el usuario actual al crear el frame de UserManagement
            self.frames["UserManagement"] = UserManagementFrame(self.container, self, self.usuario_actual, self.usuario_actual['nombre_usuario'])
            self.frames["UserManagement"].grid(row=0, column=0, sticky="nsew")

    def mostrar_frame(self, frame_name):
        frame = self.frames.get(frame_name)
        if frame:
            frame.tkraise()
            if frame_name == "Login":
                self.geometry("400x350")
                self.resizable(False, False)
                self.crear_menu()
            else:
                self.geometry("1000x700")
                self.resizable(True, True)
                self.crear_menu_principal()

    def on_login_success(self, datos_usuario):
        self.usuario_actual = datos_usuario
        self.crear_frames_principales()
        self.mostrar_frame("Dashboard")

    def crear_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        menubar.add_command(label="Salir", command=self.quit)

    def crear_menu_principal(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        nav_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Módulos", menu=nav_menu)
        nav_menu.add_command(label="Dashboard", command=lambda: self.mostrar_frame("Dashboard"))
        nav_menu.add_command(label="Inventario", command=lambda: self.mostrar_frame("Inventario"))
        nav_menu.add_command(label="Alertas de Stock", command=lambda: self.mostrar_frame("Alerts"))
        
        gestor = GestionUsuarios()
        if gestor.es_admin(self.usuario_actual['nombre_usuario']):
            nav_menu.add_separator()
            nav_menu.add_command(label="Gestión de Usuarios", command=lambda: self.mostrar_frame("UserManagement"))

        if gestor.es_admin(self.usuario_actual['nombre_usuario']):
            tools_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Herramientas", menu=tools_menu)
            tools_menu.add_command(label="Configuración", command=self.abrir_configuracion)
            # NUEVO: Añadir opción de historial
            tools_menu.add_command(label="Ver Historial de Cambios", command=self.abrir_historial)

        nav_menu.add_separator()
        nav_menu.add_command(label=f"Cerrar Sesión ({self.usuario_actual['nombre_usuario']})", command=self.logout)
        nav_menu.add_command(label="Salir", command=self.quit)

    def abrir_configuracion(self):
        SettingsDialog(self, on_save_callback=self._refresh_current_frame)

    # NUEVO: Método para abrir el diálogo de historial
    def abrir_historial(self):
        HistoryDialog(self)

    def _refresh_current_frame(self):
        current_frame_name = None
        for name, frame in self.frames.items():
            if frame and frame.winfo_ismapped():
                try:
                    if frame == self.winfo_children()[0]:
                        current_frame_name = name
                        break
                except tk.TclError:
                    pass
        
        if current_frame_name == "Inventario":
            self.frames["Inventario"].cargar_datos_en_treeview()
            self.frames["Inventario"].actualizar_resumen_texto()
        elif current_frame_name == "Alerts":
            self.frames["Alerts"].cargar_alertas_en_treeview()

    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que quieres cerrar la sesión?"):
            self.usuario_actual = None
            if self.frames.get("Dashboard"):
                self.frames["Dashboard"].destroy()
            if self.frames.get("Inventario"):
                self.frames["Inventario"].destroy()
            if self.frames.get("Alerts"):
                self.frames["Alerts"].destroy()
            if self.frames.get("UserManagement"):
                self.frames["UserManagement"].destroy()
            self.frames["Dashboard"] = None
            self.frames["Inventario"] = None
            self.frames["Alerts"] = None
            self.frames["UserManagement"] = None
            self.mostrar_frame("Login")

if __name__ == "__main__":
    app = App()
    app.mainloop()