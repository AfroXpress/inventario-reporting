# log.py

import os
from datetime import datetime
from utils import get_data_path

# Nombre del archivo de historial
HISTORY_FILE = os.path.join(get_data_path(), "historial_cambios.log")

def log_change(usuario: str, accion: str, detalles: str):
    """
    Registra un cambio en el archivo de historial.
    
    Args:
        usuario (str): El nombre de usuario que realizó la acción.
        accion (str): Una descripción corta de la acción (ej. "Producto Agregado").
        detalles (str): Detalles adicionales sobre el cambio (ej. "Código: XXX, Cantidad: 50").
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = (
        f"[{timestamp}] Usuario: {usuario} | Acción: {accion}\n"
        f"Detalles: {detalles}\n"
        f"--------------------------------------------------\n"
    )
    
    try:
        # Usar 'a' para añadir al final del archivo (append mode)
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except IOError as e:
        # Si no se puede escribir, imprimir el error en la consola
        # para no detener la aplicación.
        print(f"Error al escribir en el historial: {e}")

def clear_history():
    """Borra el contenido del archivo de historial."""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            f.write("") # Escribe una cadena vacía para limpiar el archivo
        return True
    except IOError:
        return False