# 📦 Sistema de Inventario de Baterías

Una aplicación de escritorio robusta y moderna para la gestión de inventario de baterías, desarrollada en Python. Permite a los departamentos de compras y logística controlar el stock, generar alertas y gestionar usuarios de forma segura y eficiente.

![Screenshot Placeholder](assets/screenshot_main.png)

## ✨ Características Clave

- 🔐 **Sistema de Autenticación Seguro**: Roles de usuario (Administrador y Estándar) con contraseñas hasheadas.
- 👤 **Gestión de Usuarios**: El administrador puede crear, eliminar usuarios y cambiar contraseñas desde la aplicación.
- 📊 **Dashboard Personalizado**: Un panel de control con un resumen claro del estado del inventario.
- 📦 **Módulo de Inventario Completo**:
  - Importar listas de productos desde archivos Excel.
  - Exportar el inventario completo o reportes específicos.
  - Buscar productos en tiempo real por código o descripción.
  - Eliminar productos con un solo clic.
- ⚠️ **Alertas de Stock Inteligentes**: Una vista dedicada a los productos con stock bajo, con filtros y exportación.
- ⚙️ **Configuración Flexible**: El administrador puede ajustar el límite de stock bajo y el tema visual de la aplicación.
- 📜 **Historial de Cambios Trazaable**: Un registro completo de todas las acciones importantes (agregados, eliminados, cambios de contraseña), con usuario y fecha.
- 🎨 **Interfaz Moderna**: Diseño profesional y atractivo usando `ttkbootstrap`.

## 🚀 Cómo Empezar

### Para Usuarios Finales (Recomendado)

La forma más sencilla de usar la aplicación es con el archivo ejecutable (`.exe`).

1.  **Descarga** la última versión del archivo `Inventario de Baterias.exe`.
2.  **Descomprime** el archivo `.zip` en una carpeta de tu elección (ej. `C:\Programas\InventarioBaterias`).
3.  **Ejecuta** haciendo doble clic en `Inventario de Baterias.exe`.

¡Listo! La aplicación se iniciará y creará la carpeta `data` necesaria para guardar tu inventario y usuarios.

### Para Desarrolladores

Si quieres ejecutar el código fuente o contribuir al proyecto:

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/inventario-reporting.git
    cd inventario-reporting
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows (PowerShell)
    .\venv\Scripts\Activate.ps1
    # En Windows (CMD)
    .\venv\Scripts\activate.bat
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecuta la aplicación:**
    ```bash
    python main.py
    ```

## 📖 Guía de Uso

### Primeros Pasos

Al ejecutar la aplicación por primera vez, te encontrarás con una pantalla de login.

*   **Usuario por defecto:** `admin`
*   **Contraseña por defecto:** `admin`

Se recomienda encarecidamente cambiar la contraseña del usuario `admin` la primera vez que inicies sesión.

### Navegación por Módulos

Usa el menú **"Módulos"** en la parte superior de la ventana para moverte entre las diferentes secciones de la aplicación.

#### 📊 Dashboard

Pantalla de bienvenida que te da un resumen rápido del estado de tu inventario:
*   Total de productos únicos.
*   Total de unidades en stock.
*   Número de productos con stock bajo.

#### 📦 Inventario

Este es el módulo principal para gestionar tus productos.

-   **Buscar Producto:** Usa la barra de búsqueda para encontrar cualquier producto al instante por su código o descripción.
-   **Importar Excel:** Haz clic en "Importar Excel" para añadir o actualizar productos desde un archivo `.xlsx`. La aplicación actualizará las cantidades de los productos existentes o añadirá los nuevos.
-   **Exportar Todo:** Genera un archivo Excel con todo tu inventario actual.
-   **Eliminar Seleccionado:** Selecciona un producto de la lista y haz clic en este botón para eliminarlo.
-   **Actualizar Vista:** Recarga los datos desde el archivo de datos.

#### ⚠️ Alertas de Stock

Este módulo te muestra una lista filtrada de todos los productos que necesitan atención.

-   **Buscar Alerta:** Busca productos específicos dentro de las alertas.
-   **Exportar Alertas:** Genera un archivo Excel únicamente con los productos que tienen stock bajo.

#### ⚙️ Gestión de Usuarios (Solo para Administradores)

Desde aquí, el usuario `admin` puede:
-   **Crear Nuevo Usuario:** Añadir nuevas cuentas para que otros miembros del equipo puedan usar la aplicación.
-   **Cambiar Contraseña:** Restablecer la contraseña de cualquier usuario (incluido el `admin`).
-   **Eliminar Usuario:** Eliminar cuentas que ya no se necesiten.

#### ⚙️ Herramientas (Solo para Administradores)

-   **Configuración:** Accede a la configuración de la aplicación para personalizar:
    -   **Límite para Stock Bajo:** Define cuántas unidades o menos se consideran "stock bajo" (por defecto, 50).
    -   **Tema Visual:** Cambia la apariencia de la aplicación (ej. a "darkly", "cyborg", etc.).

## 🔧 Personalización Avanzada

### Cambiar el Tema Visual

1.  Ve a **Herramientas > Configuración**.
2.  Selecciona tu tema preferido en el menú desplegable.
3.  Guarda los cambios.
4.  Reinicia la aplicación para que el nuevo tema se aplique completamente.

### Ajustar el Límite de Stock Bajo

1.  Ve a **Herramientas > Configuración**.
2.  Usa las flechas o escribe el nuevo número en el campo "Límite para Stock Bajo".
3.  Guarda los cambios. El límite se aplicará al instante en los módulos de Inventario y Alertas.

## 🤔 Soporte y Preguntas Frecuentes (FAQ)

**P: ¿Puedo recuperar mi contraseña si la olvido?**
R: Actualmente, la recuperación de contraseña debe ser realizada por el administrador del sistema a través del módulo "Gestión de Usuarios".

**P: ¿La aplicación funciona en macOS o Linux?**
R: El código fuente es compatible con macOS y Linux. Sin embargo, el ejecutable `.exe` proporcionado es solo para Windows. Para otras plataformas, sigue la guía de instalación para desarrolladores.

**P: ¿Dónde se guardan mis datos?**
R: Todos tus datos (inventario, usuarios, configuración e historial) se guardan en una carpeta llamada `data`, que se crea en el mismo directorio donde se encuentra el archivo ejecutable. Puedes hacer una copia de seguridad de esta carpeta.

## 🛠️ Pila Tecnológica

-   **Lenguaje:** Python 3.8+
-   **Interfaz Gráfica:** `tkinter` + `ttkbootstrap`
-   **Manejo de Datos:** `pandas` (para inventario), `sqlite3` (para usuarios)
-   **Integración con Excel:** `openpyxl`
-   **Seguridad:** `bcrypt`
-   **Empaquetado:** `PyInstaller`

## 📁 Estructura del Proyecto
inventario-reporting/
├── main.py # Punto de entrada y controlador principal
├── requirements.txt # Dependencias del proyecto
├── README.md # Este archivo
├── models.py # Modelo de datos para el inventario
├── usuarios.py # Modelo de datos y lógica para usuarios
├── config.py # Gestión de la configuración de la app
├── log.py # Gestión del historial de cambios
├── dashboard.py # Vista y lógica del dashboard
├── inventario.py # Vista y lógica del módulo de inventario
├── alerts.py # Vista y lógica del módulo de alertas
├── login.py # Vista y lógica de la pantalla de login
├── user_management.py # Vista y lógica de la gestión de usuarios
├── settings.py # Vista y lógica del diálogo de configuración
├── history.py # Vista y lógica del visor de historial
├── utils.py # Utilidades (rutas de datos, etc.)
├── assets/ # Recursos gráficos (iconos, etc.)
└── data/ # Carpeta de datos (creada al ejecutar)
├── inventario.csv # Base de datos del inventario
├── usuarios.db # Base de datos de usuarios
├── config.json # Archivo de configuración
└── historial_cambios.log # Historial de acciones

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si tienes una idea para mejorar la aplicación o has encontrado un error, por favor:

1.  Abre un **issue** en el repositorio de GitHub.
2.  Haz un **fork** del proyecto.
3.  Crea una nueva rama (`git checkout -b feature/tu-mejora`).
4.  Realiza tus cambios.
5.  Haz un `commit` (`git commit -m 'Añade tu descripción aquí'`).
6.  Empuja tu rama (`git push origin feature/tu-mejora`).
7.  Abre un **Pull Request**.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---
