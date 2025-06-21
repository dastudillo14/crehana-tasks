# API de Gestión de Tareas

## Descripción del Proyecto

Esta es una moderna API de Gestión de Tareas construida con FastAPI, siguiendo los principios de la Arquitectura Limpia. Proporciona una estructura robusta, escalable y mantenible para gestionar listas de tareas y sus tareas asociadas.

El proyecto está diseñado con una clara separación de responsabilidades en tres capas principales:
-   **Dominio**: Contiene la lógica de negocio principal y las entidades.
-   **Aplicación**: Orquesta la lógica de dominio a través de casos de uso.
-   **Infraestructura**: Maneja aspectos externos como la interacción con la base de datos y los endpoints de la API.

Esta arquitectura hace que la aplicación sea fácil de probar, mantener y extender. El proyecto está completamente contenedorizado con Docker e incluye una suite completa de pruebas unitarias y de integración con `pytest`.

---

## Características

-   **Arquitectura Limpia y Modular**: Organizada por funcionalidad para facilitar la navegación y el escalado.
-   **FastAPI**: Framework asíncrono de alto rendimiento.
-   **Pydantic**: Sólida validación de datos y gestión de la configuración.
-   **SQLAlchemy**: Operaciones de base de datos asíncronas con SQLite.
-   **Soporte para Docker**: Totalmente contenedorizado con Docker y Docker Compose para un despliegue sencillo.
-   **Pruebas Completas**: Alta cobertura de código con `pytest`, incluyendo pruebas unitarias y de integración.
-   **Inyección de Dependencias**: Gestiona las dependencias de forma limpia, haciendo la aplicación flexible y fácil de probar.

---

## Cómo Empezar

### Prerrequisitos

-   Python 3.11+
-   Docker y Docker Compose

---

### 1. Configuración del Entorno Local

Para el desarrollo local sin Docker, sigue estos pasos para configurar un entorno virtual.

**a. Clona el repositorio:**
```bash
git clone <url-de-tu-repositorio>
cd crehana-test
```

**b. Crea y activa un entorno virtual:**
```bash
# Crea el entorno virtual
python -m venv .venv

# Actívalo (macOS/Linux)
source .venv/bin/activate

# Actívalo (Windows)
# .\.venv\Scripts\activate
```

**c. Instala las dependencias:**
```bash
pip install -r requirements.txt
```

**d. Crea tu archivo de entorno local:**
Copia el archivo de entorno de ejemplo para crear tu propia configuración local.
```bash
cp .env.example .env
```
La configuración por defecto en `.env` está preparada para el desarrollo local y creará un archivo `task_management.db` en un directorio `data/`.

**e. Ejecuta la aplicación localmente:**
```bash
uvicorn app:app --reload
```
La API estará disponible en `http://localhost:8000`.

---

### 2. Ejecutar la Aplicación con Docker

Esta es la forma recomendada de ejecutar el proyecto para una experiencia de desarrollo consistente.

**a. Construye y ejecuta los contenedores:**
Desde la raíz del proyecto, ejecuta el siguiente comando:
```bash
docker-compose up --build
```
Este comando construirá la imagen de Docker, iniciará el servicio de la API y creará un volumen persistente para la base de datos SQLite en el directorio `data/`.

La API estará disponible en `http://localhost:8000`. Puedes acceder a la documentación autogenerada en:
-   **Swagger UI**: `http://localhost:8000/docs`
-   **ReDoc**: `http://localhost:8000/redoc`

**b. Para detener la aplicación:**
Simplemente presiona `Ctrl+C` en la terminal donde se está ejecutando `docker-compose`, o ejecuta el siguiente comando desde otra terminal:
```bash
docker-compose down
```

---

### 3. Ejecutar las Pruebas

El proyecto incluye una suite completa de pruebas unitarias y de integración usando `pytest`.

**a. Activa tu entorno virtual** (si no está activo):
```bash
source .venv/bin/activate
```

**b. Ejecuta la suite de pruebas:**
Ejecuta el siguiente comando desde la raíz del proyecto:
```bash
pytest
```
Esto descubrirá y ejecutará automáticamente todas las pruebas en el directorio `tests/`. También generará un **informe de cobertura de código** en la terminal, como se configuró en `pytest.ini`.

Para ver un informe de cobertura HTML más detallado e interactivo, puedes ejecutar:
```bash
pytest --cov-report html
```
Luego, abre el archivo `htmlcov/index.html` en tu navegador.

## Características

- ✅ Crear, obtener, actualizar y eliminar listas de tareas
- ✅ Crear, obtener, actualizar y eliminar tareas dentro de una lista
- ✅ Cambiar el estado de una tarea
- ✅ Listar tareas con filtros por estado o prioridad
- ✅ Cálculo automático del porcentaje de completitud
- ✅ Base de datos SQLite con SQLAlchemy async
- ✅ Documentación automática con Swagger/ReDoc
- ✅ Validación de datos con Pydantic
- ✅ Manejo de errores HTTP apropiado

## Instalación y Ejecución

### Con Docker

```bash
# Construir la imagen
docker build -t task-management-api .

# Ejecutar el contenedor
docker run -p 8000:8000 task-management-api
```

### Sin Docker

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
```

## Endpoints de la API

### Listas de Tareas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/task-lists/` | Crear una nueva lista de tareas |
| GET | `/task-lists/` | Obtener todas las listas de tareas |
| GET | `/task-lists/{id}` | Obtener una lista específica |
| PUT | `/task-lists/{id}` | Actualizar una lista de tareas |
| DELETE | `/task-lists/{id}` | Eliminar una lista y todas sus tareas |

### Tareas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/tasks/{list_id}/tasks` | Crear una nueva tarea en una lista |
| GET | `/tasks/{list_id}/tasks` | Obtener todas las tareas de una lista |
| GET | `/tasks/{list_id}/tasks/filtered` | Obtener tareas filtradas por estado/prioridad |
| GET | `/tasks/task/{id}` | Obtener una tarea específica |
| PUT | `/tasks/task/{id}` | Actualizar una tarea |
| PATCH | `/tasks/task/{id}/status` | Cambiar el estado de una tarea |
| DELETE | `/tasks/task/{id}` | Eliminar una tarea |

## Modelos de Datos

### TaskList
```json
{
  "id": 1,
  "title": "Mi Lista de Tareas",
  "description": "Descripción opcional",
  "completion_percentage": 75,
  "total_tasks": 4,
  "completed_tasks": 3,
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T15:30:00"
}
```

### Task
```json
{
  "id": 1,
  "title": "Completar proyecto",
  "description": "Finalizar la implementación",
  "status": "in_progress",
  "percentage": 60,
  "priority": "high",
  "task_list_id": 1,
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T15:30:00"
}
```

## Estados y Prioridades

### Estados de Tarea
- `pending`: Pendiente
- `in_progress`: En progreso
- `completed`: Completada
- `cancelled`: Cancelada

### Prioridades
- `low`: Baja
- `medium`: Media
- `high`: Alta
- `urgent`: Urgente

## Ejemplos de Uso

### Crear una lista de tareas
```bash
curl -X POST "http://localhost:8000/task-lists/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Proyecto Web",
    "description": "Tareas para el desarrollo del sitio web"
  }'
```

### Crear una tarea
```bash
curl -X POST "http://localhost:8000/tasks/1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Diseñar interfaz",
    "description": "Crear mockups de la UI",
    "priority": "high",
    "percentage": 0
  }'
```

### Filtrar tareas por estado
```bash
curl "http://localhost:8000/tasks/1/tasks/filtered?status=in_progress"
```

### Cambiar estado de una tarea
```bash
curl -X PATCH "http://localhost:8000/tasks/task/1/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

## Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Base de Datos

La aplicación utiliza SQLite como base de datos. El archivo de base de datos se crea automáticamente en `./tasks.db` cuando se ejecuta la aplicación por primera vez.

## Estructura del Proyecto

```
src/
├── domain/
│   ├── entities.py      # Entidades de dominio
│   └── repositories.py  # Interfaces de repositorios
├── application/
│   ├── dtos.py         # Objetos de transferencia de datos
│   └── use_cases.py    # Casos de uso
├── infrastructure/
│   ├── database.py     # Configuración de base de datos
│   ├── models.py       # Modelos de SQLAlchemy
│   └── repositories.py # Implementaciones de repositorios
└── api/
    └── routes.py       # Endpoints de FastAPI
```

## Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=src
``` 