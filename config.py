# config.py

import json
import os
from utils import get_data_path

# Nombre del archivo de configuración
CONFIG_FILE = os.path.join(get_data_path(), "config.json")

# Valores de configuración por defecto
DEFAULT_SETTINGS = {
    "stock_low_limit": 50,
    "theme": "superhero"
}

def load_settings():
    """Carga la configuración desde el archivo JSON.
    Si el archivo no existe, crea uno con los valores por defecto.
    """
    if not os.path.exists(CONFIG_FILE):
        # Si no existe, crearlo con los valores por defecto
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        # Asegurarse de que todas las claves por defecto existan
        # (útil si añadimos nuevas opciones en el futuro)
        for key, value in DEFAULT_SETTINGS.items():
            if key not in settings:
                settings[key] = value
        
        return settings
    except (json.JSONDecodeError, IOError):
        # Si el archivo está corrupto o hay error, volver a los valores por defecto
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

def save_settings(settings_to_save):
    """Guarda el diccionario de configuración en el archivo JSON."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings_to_save, f, indent=4)
        return True
    except IOError:
        return False

def get_setting(key):
    """Obtiene un valor específico de la configuración."""
    settings = load_settings()
    return settings.get(key)

def update_setting(key, value):
    """Actualiza un valor específico y lo guarda."""
    settings = load_settings()
    settings[key] = value
    return save_settings(settings)