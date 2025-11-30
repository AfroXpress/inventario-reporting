# models.py

import pandas as pd
import os
from utils import INVENTARIO_FILE
from log import log_change # <-- NUEVA IMPORTACIÓN

# Constantes
COLUMNAS = ['codigo', 'descripcion', 'cantidad']

class Producto:
    """Representa un único producto en el inventario."""
    def __init__(self, codigo: str, descripcion: str, cantidad: int):
        self.codigo = str(codigo)
        self.descripcion = str(descripcion)
        self.cantidad = int(cantidad)

    def __repr__(self):
        return f"Producto(Código: {self.codigo}, Descripción: {self.descripcion}, Cantidad: {self.cantidad})"

class Inventario:
    """Gestiona toda la colección de productos del inventario."""
    def __init__(self, usuario_actual=None): # <-- NUEVO PARÁMETRO
        self._datos = self._cargar_datos()
        self.usuario_actual = usuario_actual # <-- GUARDAR USUARIO

    def _cargar_datos(self) -> pd.DataFrame:
        """Carga los datos desde el archivo CSV o crea un DataFrame vacío si no existe."""
        if os.path.exists(INVENTARIO_FILE):
            try:
                df = pd.read_csv(INVENTARIO_FILE)
                for col in COLUMNAS:
                    if col not in df.columns:
                        df[col] = "" if col == 'descripcion' else 0
                df['codigo'] = df['codigo'].astype(str)
                df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce').fillna(0).astype(int)
                return df[COLUMNAS]
            except (pd.errors.EmptyDataError, FileNotFoundError):
                return pd.DataFrame(columns=COLUMNAS)
        else:
            os.makedirs(os.path.dirname(INVENTARIO_FILE), exist_ok=True)
            return pd.DataFrame(columns=COLUMNAS)

    def guardar_datos(self):
        """Guarda el DataFrame actual en el archivo CSV."""
        self._datos.to_csv(INVENTARIO_FILE, index=False)

    def agregar_o_actualizar_producto(self, codigo: str, descripcion: str, cantidad: int):
        """
        Agrega un nuevo producto o actualiza la cantidad y descripción de uno existente.
        Si el producto ya existe, su cantidad y descripción son REEMPLAZADAS por los nuevos valores.
        """
        codigo = str(codigo).strip()
        descripcion = str(descripcion).strip()
        cantidad = int(cantidad)

        if not codigo:
            print("Advertencia: Se intentó agregar un producto con código vacío. Ignorando.")
            return

        mascara = self._datos['codigo'].astype(str).str.strip() == codigo
        indice = self._datos[mascara].index

        if indice.empty:
            # El producto no existe, lo agregamos
            nuevo_producto = pd.DataFrame([[codigo, descripcion, cantidad]], columns=COLUMNAS)
            self._datos = pd.concat([self._datos, nuevo_producto], ignore_index=True)
            print(f"Producto '{codigo}' agregado.")
            # NUEVO: Registrar en el historial
            log_change(
                usuario=self.usuario_actual or "Sistema",
                accion="Producto Agregado",
                detalles=f"Código: {codigo}, Descripción: {descripcion}, Cantidad: {cantidad}"
            )
        else:
            # El producto existe, REEMPLAZAMOS su cantidad y descripción
            cantidad_anterior = self._datos.loc[indice[0], 'cantidad']
            self._datos.loc[indice[0], 'cantidad'] = cantidad
            self._datos.loc[indice[0], 'descripcion'] = descripcion
            print(f"Producto '{codigo}' actualizado.")
            # NUEVO: Registrar en el historial
            log_change(
                usuario=self.usuario_actual or "Sistema",
                accion="Cantidad Actualizada",
                detalles=f"Código: {codigo}, Cantidad Anterior: {cantidad_anterior}, Cantidad Nueva: {cantidad}"
            )

    def eliminar_producto(self, codigo: str):
        """Elimina un producto del inventario por su código."""
        codigo = str(codigo).strip()
        mascara = self._datos['codigo'].astype(str).str.strip() == codigo
        indice = self._datos[mascara].index
        
        if not indice.empty:
            # NUEVO: Obtener detalles antes de eliminar
            producto_a_eliminar = self._datos.loc[indice[0]]
            detalles = f"Código: {producto_a_eliminar['codigo']}, Descripción: {producto_a_eliminar['descripcion']}, Cantidad: {producto_a_eliminar['cantidad']}"
            
            self._datos.drop(indice, inplace=True)
            print(f"Producto '{codigo}' eliminado.")
            
            # NUEVO: Registrar en el historial
            log_change(
                usuario=self.usuario_actual or "Sistema",
                accion="Producto Eliminado",
                detalles=detalles
            )
            return True
        else:
            print(f"Error: Producto con código '{codigo}' no encontrado.")
            return False

    def obtener_todos_los_productos(self) -> list[Producto]:
        """Devuelve una lista de objetos Producto."""
        productos = []
        for _, row in self._datos.iterrows():
            productos.append(Producto(row['codigo'], row['descripcion'], row['cantidad']))
        return productos

    def obtener_dataframe(self) -> pd.DataFrame:
        """Devuelve el DataFrame completo para mostrarlo en tablas."""
        return self._datos

    def obtener_productos_stock_bajo(self, limite: int = 50) -> list[Producto]:
        """Devuelve una lista de productos con stock por debajo del límite especificado."""
        df_filtrado = self._datos[self._datos['cantidad'] < limite]
        productos = []
        for _, row in df_filtrado.iterrows():
            productos.append(Producto(row['codigo'], row['descripcion'], row['cantidad']))
        return productos