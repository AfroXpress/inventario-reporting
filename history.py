# history.py

import ttkbootstrap as ttk
from tkinter import messagebox
from log import HISTORY_FILE, clear_history

class HistoryDialog(ttk.Toplevel):
    """Dialogo para ver el historial de cambios."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("📜 Historial de Cambios")
        self.geometry("800x600")
        self.resizable(True, True)
        
        self.transient(parent)
        self.grab_set()

        self.crear_widgets()
        self.cargar_historial()
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
        # Frame para los botones
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(button_frame, text="Actualizar", command=self.cargar_historial, bootstyle="INFO").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpiar Historial", command=self.limpiar_historial, bootstyle="WARNING").pack(side="right", padx=5)

        # Frame para el texto del historial
        history_frame = ttk.Frame(self)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Scrollbar para el texto
        history_scroll = ttk.Scrollbar(history_frame)
        history_scroll.pack(side="right", fill="y")

        # Widget de texto para mostrar el historial
        self.history_text = ttk.Text(history_frame, wrap="word", font=("Consolas", 10), state="disabled", yscrollcommand=history_scroll.set)
        self.history_text.pack(fill="both", expand=True)
        history_scroll.config(command=self.history_text.yview)

    def cargar_historial(self):
        """Carga el contenido del archivo de historial en el widget de texto."""
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            self.history_text.config(state="normal")
            self.history_text.delete('1.0', "end")
            self.history_text.insert('1.0', contenido)
            self.history_text.config(state="disabled")
            self.history_text.see("end") # Desplazarse al final
        except FileNotFoundError:
            self.history_text.config(state="normal")
            self.history_text.delete('1.0', "end")
            self.history_text.insert('1.0', "No hay historial de cambios disponible.")
            self.history_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error al Cargar Historial", f"No se pudo cargar el historial.\nError: {e}", parent=self)

    def limpiar_historial(self):
        """Limpia el archivo de historial y la vista."""
        confirmacion = messagebox.askyesno(
            "Confirmar Limpieza",
            "¿Estás seguro de que quieres limpiar todo el historial de cambios?\n\nEsta acción no se puede deshacer.",
            parent=self
        )

        if confirmacion:
            if clear_history():
                self.history_text.config(state="normal")
                self.history_text.delete('1.0', "end")
                self.history_text.insert('1.0', "El historial ha sido limpiado.")
                self.history_text.config(state="disabled")
                messagebox.showinfo("Historial Limpiado", "El historial de cambios se ha eliminado correctamente.", parent=self)
            else:
                messagebox.showerror("Error al Limpiar", "No se pudo limpiar el archivo de historial.", parent=self)