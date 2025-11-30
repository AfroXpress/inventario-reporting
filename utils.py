# utils.py

import sys
import os
import shutil

def get_data_path():
    """
    Devuelve la ruta a la carpeta de datos persistente.
    Si se ejecuta desde un .exe, crea una carpeta 'data' local si no existe,
    copiando los datos iniciales desde el bundle.
    Si se ejecuta desde el código fuente, usa la carpeta 'data' del proyecto.
    """
    # Determinar si estamos en un entorno empaquetado (ejecutable .exe)
    if getattr(sys, 'frozen', False):
        # Ruta donde está el ejecutable
        base_path = os.path.dirname(sys.executable)
        local_data_path = os.path.join(base_path, 'data')

        # Si la carpeta de datos local no existe, crearla copiando desde el bundle
        if not os.path.exists(local_data_path):
            print("Creando carpeta de datos local por primera vez...")
            # Ruta a los datos dentro del bundle temporal
            bundle_data_path = os.path.join(sys._MEIPASS, 'data')
            # Copiar la carpeta completa
            shutil.copytree(bundle_data_path, local_data_path)
            print(f"Carpeta de datos creada en: {local_data_path}")
        
        return local_data_path
    else:
        # Estamos en modo desarrollo, usar la carpeta 'data' del proyecto
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Actualizar las constantes en los otros módulos para que usen esta función
INVENTARIO_FILE = os.path.join(get_data_path(), "inventario.csv")
USUARIOS_DB = os.path.join(get_data_path(), "usuarios.db")