# settings.py

import ttkbootstrap as ttk
from tkinter import messagebox
from config import load_settings, update_setting

# Lista de temas disponibles para el Combobox
THEMES = ["superhero", "darkly", "cyborg", "vapor", "litera", "minty", "lumen", "pulse", "sandstone", "united"]

class SettingsDialog(ttk.Toplevel):
    """Dialogo de configuración para ajustes de la aplicación."""
    def __init__(self, parent, on_save_callback=None): # <-- NUEVO PARÁMETRO
        super().__init__(parent)
        self.title("⚙️ Configuración de la Aplicación")
        self.geometry("400x350")
        self.resizable(False, False)
        
        self.on_save_callback = on_save_callback # <-- GUARDAR CALLBACK
        
        # Hace que el diálogo esté sobre la ventana principal y sea modal
        self.transient(parent)
        self.grab_set()

        self.current_settings = load_settings()
        self.crear_widgets()
        self.centrar_ventana()

    def centrar_ventana(self):
        """Centra el diálogo en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def crear_widgets(self):
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        # --- Configuración de Inventario ---
        stock_frame = ttk.Labelframe(main_frame, text="Configuración de Inventario", padding=10)
        stock_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(stock_frame, text="Límite para Stock Bajo:").pack(anchor="w")
        self.stock_limit_spinbox = ttk.Spinbox(stock_frame, from_=1, to=1000, bootstyle="PRIMARY")
        self.stock_limit_spinbox.pack(fill="x", pady=(0, 10))
        
        # Cargar el valor actual en el Spinbox
        self.stock_limit_spinbox.set(self.current_settings.get("stock_low_limit", 50))

        # --- Configuración de Apariencia ---
        appearance_frame = ttk.Labelframe(main_frame, text="Configuración de Apariencia", padding=10)
        appearance_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(appearance_frame, text="Tema Visual:").pack(anchor="w")
        self.theme_combobox = ttk.Combobox(appearance_frame, values=THEMES, bootstyle="PRIMARY", state="readonly")
        self.theme_combobox.pack(fill="x", pady=(0, 10))
        
        # Cargar el valor actual en el Combobox
        self.theme_combobox.set(self.current_settings.get("theme", "superhero"))

        # --- Botones ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(button_frame, text="Guardar Cambios", command=self._save_settings, bootstyle="SUCCESS").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.destroy, bootstyle="SECONDARY").pack(side="right", padx=5)

    def _save_settings(self):
        """Guarda los cambios en el archivo de configuración."""
        try:
            # Obtener valores de los widgets
            new_stock_limit = int(self.stock_limit_spinbox.get())
            new_theme = self.theme_combobox.get()

            # Validar que los valores sean válidos
            if new_stock_limit <= 0:
                messagebox.showerror("Error de Validación", "El límite de stock debe ser un número positivo.", parent=self)
                return

            # Actualizar la configuración usando el módulo config.py
            update_setting("stock_low_limit", new_stock_limit)
            update_setting("theme", new_theme)

            messagebox.showinfo(
                "Configuración Guardada", 
                "Los cambios han sido guardados correctamente.\n\n"
                "Los cambios se aplicarán al instante.",
                parent=self
            )
            
            # NUEVO: Llamar al callback para notificar al padre
            if self.on_save_callback:
                self.on_save_callback()
                
            self.destroy() # Cerrar el diálogo

        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, introduce un número válido para el límite de stock.", parent=self)
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No se pudo guardar la configuración.\nError: {e}", parent=self)