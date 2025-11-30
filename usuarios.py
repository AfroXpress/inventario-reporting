# usuarios.py

import sqlite3
import bcrypt
import os
from utils import USUARIOS_DB
from log import log_change # <-- NUEVA IMPORTACIÓN

# Constantes
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin" # Contraseña por defecto

class GestionUsuarios:
    """Maneja todas las operaciones de la base de datos de usuarios."""

    def __init__(self, usuario_actual=None): # <-- NUEVO PARÁMETRO
        self._conectar_y_crear_tabla()
        self._crear_admin_si_no_existe()
        self.usuario_actual = usuario_actual # <-- GUARDAR USUARIO

    def _conectar_y_crear_tabla(self):
        """Se conecta a la BD y crea la tabla de usuarios si no existe."""
        os.makedirs(os.path.dirname(USUARIOS_DB), exist_ok=True)
        conn = sqlite3.connect(USUARIOS_DB)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT UNIQUE NOT NULL,
                nombre_completo TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def _crear_admin_si_no_existe(self):
        """Crea el usuario admin por defecto si no hay ningún usuario en la BD."""
        if not self.obtener_todos_los_usuarios():
            self.crear_usuario(ADMIN_USER, "Administrador del Sistema", ADMIN_PASSWORD)
            print(f"Usuario admin por defecto creado. Usuario: '{ADMIN_USER}', Contraseña: '{ADMIN_PASSWORD}'")

    def es_admin(self, nombre_usuario: str) -> bool:
        """Verifica si el nombre de usuario proporcionado es el admin."""
        return nombre_usuario == ADMIN_USER

    def crear_usuario(self, nombre_usuario: str, nombre_completo: str, password: str) -> bool:
        """Crea un nuevo usuario en la base de datos."""
        if not nombre_usuario or not password:
            return False
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            conn = sqlite3.connect(USUARIOS_DB)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre_usuario, nombre_completo, password_hash) VALUES (?, ?, ?)",
                           (nombre_usuario, nombre_completo, password_hash))
            conn.commit()
            conn.close()
            
            # NUEVO: Registrar en el historial
            log_change(
                usuario=self.usuario_actual or "Sistema",
                accion="Usuario Creado",
                detalles=f"Usuario: {nombre_usuario}, Nombre Completo: {nombre_completo}"
            )
            return True
        except sqlite3.IntegrityError:
            return False

    def verificar_usuario(self, nombre_usuario: str, password: str) -> dict | None:
        """Verifica las credenciales de un usuario. Devuelve los datos del usuario o None."""
        conn = sqlite3.connect(USUARIOS_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre_usuario, nombre_completo, password_hash FROM usuarios WHERE nombre_usuario = ?", (nombre_usuario,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario[3]):
            return {
                "id": usuario[0],
                "nombre_usuario": usuario[1],
                "nombre_completo": usuario[2]
            }
        return None

    def obtener_todos_los_usuarios(self) -> list[dict]:
        """Devuelve una lista de todos los usuarios (sin la contraseña)."""
        conn = sqlite3.connect(USUARIOS_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre_usuario, nombre_completo FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()
        
        return [{"id": u[0], "nombre_usuario": u[1], "nombre_completo": u[2]} for u in usuarios]

    def eliminar_usuario(self, nombre_usuario: str) -> bool:
        """Elimina un usuario de la base de datos por su nombre de usuario."""
        if not nombre_usuario or self.es_admin(nombre_usuario):
            return False
        
        try:
            conn = sqlite3.connect(USUARIOS_DB)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE nombre_usuario = ?", (nombre_usuario,))
            conn.commit()
            conn.close()
            
            # NUEVO: Registrar en el historial
            log_change(
                usuario=self.usuario_actual or "Sistema",
                accion="Usuario Eliminado",
                detalles=f"Usuario: {nombre_usuario}"
            )
            return True
        except sqlite3.Error:
            return False

    def cambiar_password(self, nombre_usuario: str, nueva_password: str) -> bool:
        """Cambia la contraseña de un usuario específico."""
        if not nombre_usuario or not nueva_password:
            return False

        password_hash = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            conn = sqlite3.connect(USUARIOS_DB)
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET password_hash = ? WHERE nombre_usuario = ?",
                           (password_hash, nombre_usuario))
            conn.commit()
            conn.close()
            
            # NUEVO: Registrar en el historial
            log_change(
                usuario=self.usuario_actual or "Sistema",
                accion="Contraseña Cambiada",
                detalles=f"Usuario: {nombre_usuario}"
            )
            return True
        except sqlite3.Error:
            return False