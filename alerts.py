# alerts.py

import ttkbootstrap as ttk
from tkinter import messagebox, filedialog
from models import Inventario
from config import get_setting # <-- Asegúrate de que esta importación exista
import pandas as pd

class AlertsFrame(ttk.Frame):
    def __init__(self, parent, controller, usuario_actual):
        super().__init__(parent)
        self.controller = controller
        self.usuario_actual = usuario_actual
        self.inventario = Inventario()
        self.stock_low_limit = get_setting("stock_low_limit") # Valor inicial

        self.crear_widgets()
        self.cargar_alertas_en_treeview()

    def crear_widgets(self):
        titulo_label = ttk.Label(self, text="⚠️ Alertas de Stock", font=("Helvetica", 20, "bold"))
        titulo_label.pack(pady=20)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(button_frame, text="Exportar Alertas", command=self.exportar_alertas, bootstyle="SUCCESS").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Actualizar Lista", command=self.cargar_alertas_en_treeview, bootstyle="INFO").pack(side="right", padx=5)

        search_frame = ttk.Labelframe(self, text="🔍 Buscar Alerta", padding=10)
        search_frame.pack(fill="x", padx=10, pady=(5, 10))
        self.search_entry = ttk.Entry(search_frame, bootstyle="PRIMARY")
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", self._perform_search)

        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, bootstyle="PRIMARY", show="headings")
        self.tree.pack(fill="both", expand=True)
        tree_scroll.config(command=self.tree.yview)

        self.tree['columns'] = ('codigo', 'descripcion', 'cantidad', 'estado')
        self.tree.column("codigo", anchor="center", width=150)
        self.tree.column("descripcion", anchor="w", width=500)
        self.tree.column("cantidad", anchor="center", width=100)
        self.tree.column("estado", anchor="w", width=150)
        self.tree.heading("codigo", text="Código", anchor='center')
        self.tree.heading("descripcion", text="Descripción", anchor='w')
        self.tree.heading("cantidad", text="Cantidad Actual", anchor='center')
        self.tree.heading("estado", text="Estado", anchor='w')

    def _populate_treeview(self, productos_list):
        for i in self.tree.get_children():
            self.tree.delete(i)
        if not productos_list:
            self.tree.insert("", "end", values=("", "No hay productos con stock bajo en este momento.", "", ""))
            return
        for index, producto in enumerate(productos_list):
            if producto.cantidad < 20:
                estado = "Crítico"
                tag = 'danger'
            elif producto.cantidad < self.stock_low_limit: # Usar el valor dinámico
                estado = "Bajo"
                tag = 'warning'
            else:
                estado = "Normal"
                tag = 'success'
            self.tree.insert(parent='', index='end', iid=index, text='',
                             values=(producto.codigo, producto.descripcion, producto.cantidad, estado),
                             tags=(tag,))
        self.tree.tag_configure('danger', foreground='red')
        self.tree.tag_configure('warning', foreground='orange')
        self.tree.tag_configure('success', foreground='green')

    def _perform_search(self, event=None):
        search_term = self.search_entry.get().lower().strip()
        # CAMBIO CLAVE: Volver a leer el límite de stock ANTES de buscar
        self.stock_low_limit = get_setting("stock_low_limit")
        
        productos_bajo_stock = self.inventario.obtener_productos_stock_bajo(limite=self.stock_low_limit)

        if not search_term:
            self._populate_treeview(productos_bajo_stock)
        else:
            productos_filtrados = [
                p for p in productos_bajo_stock
                if search_term in p.codigo.lower() or search_term in p.descripcion.lower()
            ]
            self._populate_treeview(productos_filtrados)

    def cargar_alertas_en_treeview(self):
        # CAMBIO CLAVE: Volver a leer el límite de stock ANTES de cargar
        self.stock_low_limit = get_setting("stock_low_limit")
        
        productos_bajo_stock = self.inventario.obtener_productos_stock_bajo(limite=self.stock_low_limit)
        self._populate_treeview(productos_bajo_stock)
        self.search_entry.delete(0, 'end')

    def exportar_alertas(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")),
            title="Guardar reporte de alertas como..."
        )
        if not filepath:
            return
        try:
            # Usar el límite más reciente para exportar
            self.stock_low_limit = get_setting("stock_low_limit")
            productos_bajo_stock = self.inventario.obtener_productos_stock_bajo(limite=self.stock_low_limit)
            
            if not productos_bajo_stock:
                messagebox.showinfo("Sin Datos", "No hay productos con stock bajo para exportar.")
                return
            df_reporte = pd.DataFrame([p.__dict__ for p in productos_bajo_stock])
            df_reporte.to_excel(filepath, index=False)
            messagebox.showinfo("Reporte Generado", f"El reporte de alertas se ha guardado en:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error al Generar Reporte", f"No se pudo generar el reporte.\nError: {e}")