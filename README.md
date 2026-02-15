# API de Procesamiento de Mensajes de Chat

API RESTful para recibir, validar, procesar y almacenar mensajes de chat. El sistema incluye un pipeline de procesamiento que valida el formato, filtra contenido inapropiado y genera metadatos automaticamente.

## Tecnologias utilizadas

- Python 3.10
- FastAPI
- SQLite
- Pydantic (validacion de datos)
- Pytest

## Instalacion y ejecucion

```bash
git clone https://github.com/deepmindneural/Pruebat-cnicaASDNequi.git
cd Pruebat-cnicaASDNequi

python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
uvicorn app.principal:aplicacion --reload
```

Una vez levantado, la documentacion interactiva queda disponible en `http://localhost:8000/docs`

## Estructura del proyecto

El proyecto esta organizado en capas siguiendo principios de arquitectura limpia:

```
app/
├── principal.py                 # Punto de entrada, crea la app FastAPI
├── configuracion.py             # Configuracion centralizada
├── dependencias.py              # Inyeccion de dependencias
├── controladores/
│   └── rutas_mensajes.py        # Definicion de los endpoints
├── servicios/
│   ├── servicio_mensajes.py     # Logica de negocio principal
│   ├── procesador_mensajes.py   # Pipeline de procesamiento de mensajes
│   └── filtro_contenido.py      # Filtrado de palabras inapropiadas
├── repositorios/
│   ├── base_datos.py            # Conexion y esquema SQLite
│   └── repositorio_mensajes.py  # Consultas a la base de datos
├── esquemas/
│   ├── esquema_mensaje.py       # Modelos Pydantic para mensajes
│   └── esquema_respuesta.py     # Modelos para respuestas de la API
└── excepciones/
    ├── excepciones_api.py       # Excepciones personalizadas
    └── manejador_errores.py     # Manejo global de errores
```

La idea es que cada capa tenga una responsabilidad clara: los controladores solo manejan HTTP, los servicios tienen la logica de negocio, y los repositorios se encargan de la base de datos. Se usa inyeccion de dependencias con el sistema de `Depends` de FastAPI para mantener todo desacoplado.

## Pipeline de procesamiento

Cuando llega un mensaje, pasa por tres etapas:

1. **Validacion** — Se verifica que todos los campos esten presentes y con el formato correcto. El timestamp debe ser ISO 8601, el sender solo puede ser "user" o "system", y el contenido no puede estar vacio.

2. **Filtrado de contenido** — Se revisa el texto buscando palabras inapropiadas. Si se encuentran, se reemplazan con asteriscos en vez de rechazar el mensaje completo. El filtro usa regex con word boundaries para no tener falsos positivos.

3. **Generacion de metadatos** — Se calcula el conteo de palabras (`word_count`), el largo del contenido (`character_count`) y se registra el momento del procesamiento (`processed_at`).

## Endpoints

### POST /api/messages

Recibe un mensaje, lo valida, lo procesa y lo almacena en la base de datos.

Campos requeridos:
- `message_id` (string) — identificador unico del mensaje
- `session_id` (string) — identificador de la sesion
- `content` (string) — contenido del mensaje
- `timestamp` (string) — fecha y hora en formato ISO 8601
- `sender` (string) — "user" o "system"

Ejemplo de request:
```json
{
  "message_id": "msg-123456",
  "session_id": "session-abcdef",
  "content": "Hola, como puedo ayudarte hoy?",
  "timestamp": "2023-06-15T14:30:00Z",
  "sender": "system"
}
```

Respuesta exitosa (201):
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

Devuelve todos los mensajes de una sesion ordenados cronologicamente. Soporta paginacion y filtrado.

Parametros opcionales:
- `limit` (int, 1-100, default 50) — cantidad maxima de mensajes a devolver
- `offset` (int, default 0) — desde que posicion empezar
- `sender` ("user" o "system") — filtrar por remitente

Ejemplo: `GET /api/messages/session-abcdef?limit=10&offset=0&sender=user`

La respuesta incluye los mensajes y un objeto `pagination` con el total de mensajes, el limit y el offset usados.

### Manejo de errores

Todos los errores devuelven un formato consistente para que sea facil de manejar del lado del cliente:

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

Codigos HTTP:
- **400** — datos invalidos o campos faltantes
- **404** — no se encontraron mensajes para esa sesion
- **409** — ya existe un mensaje con ese message_id
- **500** — error interno del servidor

## Tests

Hay pruebas unitarias para cada capa (esquemas, filtro de contenido, procesador, repositorio y servicio) y pruebas de integracion que prueban los endpoints completos.

```bash
# Correr todos los tests
pytest -v

# Correr con reporte de cobertura
pytest --cov=app

# Solo unitarias
pytest tests/unitarias/ -v

# Solo integracion
pytest tests/integracion/ -v
```

## Docker

El proyecto incluye un Dockerfile para desplegar facilmente:

```bash
docker build -t api-mensajes .
docker run -p 8000:8000 api-mensajes
```

## Decisiones tecnicas

- **FastAPI sobre Flask**: elegí FastAPI porque tiene validacion integrada con Pydantic, genera documentacion automatica y el sistema de inyeccion de dependencias viene built-in.
- **SQLite sin ORM**: para mantener la simplicidad use el modulo `sqlite3` de Python directo con consultas parametrizadas. Todo el SQL esta encapsulado en la capa de repositorios.
- **Filtrado vs rechazo**: decidí que el filtro de contenido sanitice los mensajes (reemplaza con asteriscos) en vez de rechazarlos, porque me parecio mas practico para un sistema de chat real.
- **Endpoints sincronicos**: como SQLite es sincrono, los endpoints usan `def` en vez de `async def`. FastAPI los ejecuta en un threadpool automaticamente, asi que no hay problema de rendimiento.
