# Registro de Decisiones Técnicas (Architectural Decision Record - ADR)

Este documento registra las decisiones técnicas y de arquitectura clave tomadas durante el desarrollo del proyecto, junto con su contexto y justificación.

---

### 1. Arquitectura Modular basada en Clean Architecture

-   **Contexto**: El código inicial agrupaba todas las entidades, repositorios y casos de uso en archivos únicos (por ejemplo, `models.py`, `repositories.py`). Esto dificultaría la escalabilidad y el mantenimiento a medida que el proyecto creciera.
-   **Decisión**: Refactorizar la estructura del proyecto para seguir los principios de **Clean Architecture**, organizando los archivos por *feature* o *dominio* (ej. `task/`, `task_list/`) en lugar de por tipo de capa.
-   **Justificación**:
    -   **Modularidad**: Cada funcionalidad está encapsulada, facilitando su comprensión y modificación sin afectar otras partes del sistema.
    -   **Escalabilidad**: Añadir una nueva entidad (como `User`) es un proceso estandarizado que no requiere modificar archivos existentes, sino añadir nuevos.
    -   **Mantenibilidad**: Es más fácil encontrar el código relevante y depurar problemas.
    -   **Independencia**: La lógica de negocio (`Domain`) permanece independiente del framework (`FastAPI`) y de la base de datos (`SQLAlchemy`).
-   **Consecuencias**: Se reorganizó completamente el directorio `src/`. Se establecieron patrones claros para la ubicación de entidades, repositorios, DTOs y casos de uso.

---

### 2. Contenerización con Docker y Docker Compose

-   **Contexto**: Se necesitaba un entorno de desarrollo consistente y reproducible para evitar problemas del tipo "funciona en mi máquina". Además, se buscaba simplificar el proceso de despliegue.
-   **Decisión**: Utilizar **Docker** para contenerizar la aplicación y **Docker Compose** para orquestar los servicios.
-   **Justificación**:
    -   **Consistencia**: Asegura que todos los desarrolladores y los entornos (desarrollo, producción) ejecuten la aplicación con las mismas dependencias y configuración.
    -   **Simplicidad**: El comando `docker-compose up` es todo lo que se necesita para levantar el entorno completo.
    -   **Aislamiento**: Las dependencias del proyecto no interfieren con las del sistema anfitrión.
-   **Consecuencias**: Se crearon los archivos `Dockerfile` y `docker-compose.yml`. El `Dockerfile` sigue las mejores prácticas, como el uso de un usuario no-root (`appuser`) para mayor seguridad.

---

### 3. Persistencia de Datos con Volúmenes de Docker

-   **Contexto**: Al usar SQLite en un contenedor de Docker, la base de datos se perdía cada vez que el contenedor era eliminado o reconstruido.
-   **Decisión**: Utilizar un **named volume** de Docker (`db_data`) y montarlo en el directorio `/app/data` del contenedor, donde se almacena el archivo de la base de datos.
-   **Justificación**: Los volúmenes son el mecanismo estándar y recomendado por Docker para persistir datos. Desacoplan el ciclo de vida de los datos del ciclo de vida del contenedor.
-   **Consecuencias**: Se actualizó el `docker-compose.yml` para definir el volumen. La configuración de la base de datos en la aplicación apunta a la ruta dentro de este volumen.

---

### 4. Gestión de Configuración con Pydantic-Settings

-   **Contexto**: Las configuraciones, como la URL de la base de datos, no deben estar hardcodeadas en el código. Necesitaban ser gestionadas de una manera flexible y segura.
-   **Decisión**: Implementar la librería **`pydantic-settings`** para cargar la configuración desde variables de entorno y/o un archivo `.env`.
-   **Justificación**:
    -   **Centralización**: Proporciona una única fuente de verdad (`src/config.py`) para toda la configuración.
    -   **Flexibilidad**: Permite cambiar fácilmente entre entornos (desarrollo, producción, pruebas) sin modificar el código.
    -   **Seguridad**: Evita que información sensible se suba al control de versiones.
    -   **Validación**: Pydantic valida automáticamente que las variables de entorno tengan el tipo de dato correcto.
-   **Consecuencias**: Se creó `src/config.py`, `.env` (ignorado por Git) y `.env.example`. El `docker-compose.yml` fue configurado para usar `env_file`.

---

### 5. Calidad de Código con Flake8 y Black

-   **Contexto**: Para mantener un código limpio, legible y consistente, se necesitaba una herramienta para el formateo automático y la detección de errores de estilo.
-   **Decisión**: Adoptar **`black`** como formateador de código y **`flake8`** como *linter*.
-   **Justificación**:
    -   **Consistencia**: `black` asegura un estilo de código uniforme en todo el proyecto, eliminando debates sobre formateo.
    -   **Calidad**: `flake8` detecta errores comunes y violaciones de estilo que pueden llevar a bugs.
    -   **Automatización**: Estas herramientas se integran fácilmente en flujos de CI/CD para garantizar la calidad del código de forma automática.
-   **Consecuencias**: Se añadieron `black` y `flake8` a `requirements.txt`. Se crearon los archivos de configuración `.flake8` y `pyproject.toml` para que las herramientas trabajen en armonía.

---

### 6. Estrategia de Pruebas con Pytest

-   **Contexto**: Se requería una suite de pruebas robusta para garantizar la fiabilidad de la aplicación y prevenir regresiones, con una meta de cobertura de al menos el 75%.
-   **Decisión**: Implementar pruebas unitarias y de integración usando el framework **`pytest`**.
-   **Justificación**:
    -   **Estándar de la Industria**: `pytest` es la herramienta de testing más popular en el ecosistema de Python.
    -   **Pruebas Aisladas**: Se configuró una base de datos SQLite en memoria exclusivamente para las pruebas, asegurando que no interfieran con los datos de desarrollo y que se ejecuten rápidamente.
    -   **Cobertura de Código**: Se integró `pytest-cov` para medir la cobertura de las pruebas y asegurar que se cumpliera el objetivo.
    -   **Pruebas Asíncronas**: Se usó `pytest-asyncio` y `httpx` para probar de manera efectiva los endpoints asíncronos de FastAPI.
-   **Consecuencias**: Se creó el directorio `tests/` con subdirectorios para pruebas unitarias e de integración. Se añadió el archivo de configuración `pytest.ini`. 