# inventario.py

import ttkbootstrap as ttk
from tkinter import messagebox, filedialog
from models import Inventario
from config import get_setting # <-- Asegúrate de que esta importación exista
import pandas as pd

class InventarioFrame(ttk.Frame):
    def __init__(self, parent, controller, usuario_actual, nombre_usuario):
        super().__init__(parent)
        self.controller = controller
        self.usuario_actual = usuario_actual
        self.inventario = Inventario()
        self.stock_low_limit = get_setting("stock_low_limit") # Valor inicial

        self.crear_widgets()
        self.cargar_datos_en_treeview()
        self.actualizar_resumen_texto()

    def crear_widgets(self):
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(button_frame, text="Importar Excel", command=self.importar_excel, bootstyle="SUCCESS").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Exportar Todo", command=self.exportar_excel, bootstyle="INFO").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar Seleccionado", command=self.eliminar_producto_seleccionado, bootstyle="DANGER").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Actualizar Vista", command=self.cargar_datos_en_treeview, bootstyle="SECONDARY").pack(side="right", padx=5)

        search_frame = ttk.Labelframe(self, text="🔍 Buscar Producto", padding=10)
        search_frame.pack(fill="x", padx=10, pady=(5, 10))
        self.search_entry = ttk.Entry(search_frame, bootstyle="PRIMARY")
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", self._perform_search)

        resumen_frame = ttk.Labelframe(self, text="📄 Resumen del Inventario", padding=10)
        resumen_frame.pack(fill="x", padx=10, pady=(5, 10))
        self.resumen_text = ttk.Text(resumen_frame, height=4, state="disabled", wrap="word", font=("Helvetica", 10))
        self.resumen_text.pack(fill="x")

        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, bootstyle="PRIMARY")
        self.tree.pack(fill="both", expand=True)
        tree_scroll.config(command=self.tree.yview)

        self.tree['columns'] = ('codigo', 'descripcion', 'cantidad')
        self.tree.column("#0", width=0, stretch='NO')
        self.tree.column("codigo", anchor="center", width=150)
        self.tree.column("descripcion", anchor="w", width=500)
        self.tree.column("cantidad", anchor="center", width=100)
        self.tree.heading("#0", text="", anchor='center')
        self.tree.heading("codigo", text="Código", anchor='center')
        self.tree.heading("descripcion", text="Descripción", anchor='w')
        self.tree.heading("cantidad", text="Cantidad", anchor='center')

    def _populate_treeview(self, df):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for index, row in df.iterrows():
            self.tree.insert(parent='', index='end', iid=index, text='',
                             values=(row['codigo'], row['descripcion'], row['cantidad']))

    def _perform_search(self, event=None):
        search_term = self.search_entry.get().lower().strip()
        df = self.inventario.obtener_dataframe()
        if not search_term:
            self._populate_treeview(df)
        else:
            mask = (df['codigo'].str.lower().str.contains(search_term, na=False)) | \
                   (df['descripcion'].str.lower().str.contains(search_term, na=False))
            df_filtrado = df[mask]
            self._populate_treeview(df_filtrado)

    def cargar_datos_en_treeview(self):
        df = self.inventario.obtener_dataframe()
        self._populate_treeview(df)
        self.search_entry.delete(0, 'end')

    def actualizar_resumen_texto(self):
        # CAMBIO CLAVE: Volver a leer el límite de stock ANTES de calcular
        self.stock_low_limit = get_setting("stock_low_limit")
        
        try:
            df = self.inventario.obtener_dataframe()
            total_productos = len(df)
            total_unidades = df['cantidad'].sum()
            # Usar el valor recién leído
            productos_bajo_stock = len(df[df['cantidad'] < self.stock_low_limit])

            resumen = (
                f"Total de productos únicos: {total_productos}\n"
                f"Total de unidades en stock: {total_unidades}\n"
                f"Productos con stock bajo (< {self.stock_low_limit} unidades): {productos_bajo_stock}"
            )

            self.resumen_text.config(state="normal")
            self.resumen_text.delete('1.0', "end")
            self.resumen_text.insert('1.0', resumen)
            self.resumen_text.config(state="disabled")
        except Exception as e:
            print(f"Error al actualizar el resumen: {e}")

    def importar_excel(self):
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo Excel para importar",
            filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*"))
        )
        if not filepath:
            return
        try:
            df_importado = pd.read_excel(filepath)
            if 'codigo' not in df_importado.columns or 'cantidad' not in df_importado.columns:
                messagebox.showerror("Error de Formato", "El archivo Excel debe contener las columnas 'codigo' y 'cantidad'.")
                return
            productos_agregados = 0
            productos_actualizados = 0
            for index, row in df_importado.iterrows():
                if pd.isna(row['codigo']) or str(row['codigo']).strip() == '':
                    continue
                codigo = str(row['codigo']).strip()
                descripcion = str(row.get('descripcion', '')).strip()
                cantidad = int(row.get('cantidad', 0))
                if self.inventario._datos[self.inventario._datos['codigo'] == codigo].empty:
                    productos_agregados += 1
                else:
                    productos_actualizados += 1
                self.inventario.agregar_o_actualizar_producto(codigo, descripcion, cantidad)
            self.inventario.guardar_datos()
            self.cargar_datos_en_treeview()
            self.actualizar_resumen_texto()
            messagebox.showinfo("Importación Completa", 
                                f"Se importaron los datos con éxito.\n\n"
                                f"Productos agregados: {productos_agregados}\n"
                                f"Productos actualizados: {productos_actualizados}")
        except Exception as e:
            messagebox.showerror("Error al Importar", f"Ocurrió un error al leer el archivo Excel.\nError: {e}")

    def exportar_excel(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=(("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")),
            title="Guardar inventario completo como..."
        )
        if not filepath:
            return
        try:
            df = self.inventario.obtener_dataframe()
            df.to_excel(filepath, index=False)
            messagebox.showinfo("Exportación Completa", f"El inventario completo se ha guardado en:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error al Exportar", f"No se pudo guardar el archivo.\nError: {e}")

    def eliminar_producto_seleccionado(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Selección Requerida", "Por favor, selecciona un producto de la lista para eliminar.")
            return
        item_values = self.tree.item(selected_item, 'values')
        codigo_producto = item_values[0]
        descripcion_producto = item_values[1]
        confirmacion = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Estás seguro de que quieres eliminar el siguiente producto?\n\n"
            f"Código: {codigo_producto}\n"
            f"Descripción: {descripcion_producto}"
        )
        if confirmacion:
            if self.inventario.eliminar_producto(codigo_producto):
                self.inventario.guardar_datos()
                self.cargar_datos_en_treeview()
                self.actualizar_resumen_texto()
                messagebox.showinfo("Eliminado", "El producto fue eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto. Puede que ya no exista.")