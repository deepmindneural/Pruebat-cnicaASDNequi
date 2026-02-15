# API de Procesamiento de Mensajes de Chat

API RESTful para procesar y almacenar mensajes de chat, construida con FastAPI y SQLite.

## Tecnologias

- Python 3.10
- FastAPI
- SQLite
- Pydantic
- Pytest

## Instalacion

```bash
# Clonar repositorio
git clone https://github.com/deepmindneural/Pruebat-cnicaASDNequi.git
cd Pruebat-cnicaASDNequi

# Crear entorno virtual
python -m venv .venv

# Activar entorno
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecucion

```bash
uvicorn app.principal:aplicacion --reload
```

El servidor inicia en `http://localhost:8000`

Documentacion Swagger disponible en `http://localhost:8000/docs`

## Endpoints

### POST /api/messages

Recibe y procesa un mensaje de chat.

```json
{
  "message_id": "msg-123456",
  "session_id": "session-abcdef",
  "content": "Hola, como puedo ayudarte hoy?",
  "timestamp": "2023-06-15T14:30:00Z",
  "sender": "system"
}
```

Respuesta (201):
```json
{
  "status": "success",
  "data": {
    "message_id": "msg-123456",
    "session_id": "session-abcdef",
    "content": "Hola, como puedo ayudarte hoy?",
    "timestamp": "2023-06-15T14:30:00Z",
    "sender": "system",
    "metadata": {
      "word_count": 6,
      "character_count": 30,
      "processed_at": "2023-06-15T14:30:01.000000+00:00"
    }
  }
}
```

### GET /api/messages/{session_id}

Obtiene los mensajes de una sesion con paginacion y filtrado.

Parametros query:
- `limit` (int, 1-100, default 50)
- `offset` (int, default 0)
- `sender` ("user" o "system", opcional)

Ejemplo: `GET /api/messages/session-abcdef?limit=10&sender=user`

### Codigos de error

| Codigo | Descripcion |
|--------|-------------|
| 400 | Formato invalido o campos faltantes |
| 404 | Sesion no encontrada |
| 409 | Mensaje duplicado |
| 500 | Error interno |

Formato de error:
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_FORMAT",
    "message": "Formato de mensaje invalido",
    "details": "El campo 'sender' debe ser 'user' o 'system'"
  }
}
```

## Procesamiento

Cada mensaje pasa por un pipeline:

1. **Validacion** - Se verifican campos requeridos y formatos
2. **Filtrado de contenido** - Palabras inapropiadas se reemplazan con asteriscos
3. **Metadatos** - Se calcula word_count, character_count y processed_at

## Tests

```bash
# Ejecutar todos los tests
pytest -v

# Con cobertura
pytest --cov=app --cov-report=term-missing
```

58 tests | 96% cobertura

## Estructura del proyecto

```
app/
├── principal.py              # App FastAPI
├── configuracion.py          # Configuracion general
├── dependencias.py           # Inyeccion de dependencias
├── controladores/
│   └── rutas_mensajes.py     # Endpoints
├── servicios/
│   ├── servicio_mensajes.py  # Logica de negocio
│   ├── procesador_mensajes.py # Pipeline de procesamiento
│   └── filtro_contenido.py   # Filtro de palabras
├── repositorios/
│   ├── base_datos.py         # Conexion SQLite
│   └── repositorio_mensajes.py # Acceso a datos
├── esquemas/
│   ├── esquema_mensaje.py    # Modelos de mensaje
│   └── esquema_respuesta.py  # Modelos de respuesta
└── excepciones/
    ├── excepciones_api.py    # Excepciones custom
    └── manejador_errores.py  # Manejo global de errores
```

## Docker

```bash
docker build -t api-mensajes .
docker run -p 8000:8000 api-mensajes
```
