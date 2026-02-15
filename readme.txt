===============================================================
 API DE PROCESAMIENTO DE MENSAJES DE CHAT
===============================================================

DESCRIPCION GENERAL
-------------------
API RESTful para recibir, validar, procesar y almacenar mensajes
de chat. Construida con FastAPI y SQLite.

Funcionalidades principales:
- Recepcion y validacion de mensajes de chat
- Pipeline de procesamiento (validacion, filtrado de contenido,
  generacion de metadatos)
- Almacenamiento persistente en SQLite
- Recuperacion de mensajes con paginacion y filtrado
- Manejo de errores con respuestas estandarizadas


REQUISITOS PREVIOS
------------------
- Python 3.10 o superior
- pip (gestor de paquetes)


INSTALACION Y CONFIGURACION
----------------------------
1. Clonar el repositorio:
   git clone <url-del-repositorio>
   cd Prueba

2. Crear entorno virtual:
   python -m venv .venv

3. Activar entorno virtual:
   - Windows:  .venv\Scripts\activate
   - Linux/Mac: source .venv/bin/activate

4. Instalar dependencias:
   pip install -r requirements.txt

5. Ejecutar el servidor:
   uvicorn app.principal:aplicacion --reload

6. El servidor estara disponible en: http://localhost:8000
   Documentacion interactiva (Swagger): http://localhost:8000/docs


===============================================================
 DOCUMENTACION DE LA API
===============================================================

--------------------------------------------------------------
POST /api/messages
--------------------------------------------------------------
Recibe, valida, procesa y almacena un mensaje de chat.

Content-Type: application/json

Campos del body (todos requeridos):
  - message_id  (string) : Identificador unico del mensaje
  - session_id  (string) : Identificador de la sesion
  - content     (string) : Contenido del mensaje (1-5000 caracteres)
  - timestamp   (string) : Marca de tiempo ISO 8601 (ej: "2023-06-15T14:30:00Z")
  - sender      (string) : "user" o "system"

Ejemplo de request:
  POST http://localhost:8000/api/messages
  {
    "message_id": "msg-123456",
    "session_id": "session-abcdef",
    "content": "Hola, como puedo ayudarte hoy?",
    "timestamp": "2023-06-15T14:30:00Z",
    "sender": "system"
  }

Respuesta exitosa (201 Created):
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
        "character_count": 31,
        "processed_at": "2023-06-15T14:30:01.000000+00:00"
      }
    }
  }

Posibles errores:
  - 400: Formato invalido o campos faltantes
  - 409: Mensaje duplicado (message_id ya existe)
  - 422: Contenido inapropiado (se sanitiza automaticamente)


--------------------------------------------------------------
GET /api/messages/{session_id}
--------------------------------------------------------------
Recupera todos los mensajes de una sesion.

Parametros de ruta:
  - session_id (string) : ID de la sesion a consultar

Parametros de query (opcionales):
  - limit  (int, 1-100, default 50) : Numero maximo de mensajes
  - offset (int, >=0, default 0)    : Desplazamiento para paginacion
  - sender (string, "user"|"system"): Filtrar por remitente

Ejemplo de request:
  GET http://localhost:8000/api/messages/session-abcdef?limit=10&offset=0&sender=user

Respuesta exitosa (200 OK):
  {
    "status": "success",
    "data": [
      {
        "message_id": "msg-123456",
        "session_id": "session-abcdef",
        "content": "Hola mundo",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "user",
        "metadata": {
          "word_count": 2,
          "character_count": 10,
          "processed_at": "2023-06-15T14:30:01.000000+00:00"
        }
      }
    ],
    "pagination": {
      "total": 1,
      "limit": 10,
      "offset": 0
    }
  }

Posibles errores:
  - 404: Sesion no encontrada


--------------------------------------------------------------
FORMATO DE ERRORES
--------------------------------------------------------------
Todos los errores siguen el mismo formato:
  {
    "status": "error",
    "error": {
      "code": "CODIGO_ERROR",
      "message": "Descripcion del error",
      "details": "Informacion adicional"
    }
  }

Codigos de error:
  - VALIDATION_ERROR      : Datos de entrada invalidos
  - INVALID_FORMAT        : Formato del mensaje incorrecto
  - DUPLICATE_MESSAGE     : El message_id ya existe
  - SESSION_NOT_FOUND     : No hay mensajes para esa sesion
  - INAPPROPRIATE_CONTENT : Contenido con palabras prohibidas
  - INTERNAL_ERROR        : Error interno del servidor


===============================================================
 PROCESAMIENTO DE MENSAJES
===============================================================
Cada mensaje pasa por un pipeline de procesamiento:

1. VALIDACION: Se verifican todos los campos requeridos y formatos
2. FILTRADO: Se detectan y reemplazan palabras inapropiadas con
   asteriscos (ej: "idiota" -> "******")
3. METADATOS: Se calculan word_count, character_count y se agrega
   el timestamp de procesamiento (processed_at)


===============================================================
 EJECUCION DE PRUEBAS
===============================================================

Ejecutar todas las pruebas:
  pytest

Ejecutar con reporte de cobertura:
  pytest --cov=app --cov-report=term-missing

Ejecutar solo pruebas unitarias:
  pytest tests/unitarias/

Ejecutar solo pruebas de integracion:
  pytest tests/integracion/

Cobertura actual: 96% (58 pruebas)


===============================================================
 ESTRUCTURA DEL PROYECTO
===============================================================

Prueba/
|-- app/
|   |-- principal.py              # Creacion de la app FastAPI
|   |-- configuracion.py          # Configuracion centralizada
|   |-- dependencias.py           # Inyeccion de dependencias
|   |-- controladores/
|   |   |-- rutas_mensajes.py     # Endpoints POST y GET
|   |-- servicios/
|   |   |-- servicio_mensajes.py  # Orquestacion de logica de negocio
|   |   |-- procesador_mensajes.py # Pipeline de procesamiento
|   |   |-- filtro_contenido.py   # Filtro de palabras inapropiadas
|   |-- repositorios/
|   |   |-- base_datos.py         # Conexion SQLite y esquema
|   |   |-- repositorio_mensajes.py # Acceso a datos (CRUD)
|   |-- esquemas/
|   |   |-- esquema_mensaje.py    # Modelos Pydantic de mensajes
|   |   |-- esquema_respuesta.py  # Modelos de respuesta API
|   |-- excepciones/
|       |-- excepciones_api.py    # Excepciones personalizadas
|       |-- manejador_errores.py  # Handlers globales de errores
|-- tests/
|   |-- conftest.py               # Fixtures compartidas
|   |-- unitarias/                # Tests unitarios por componente
|   |-- integracion/              # Tests de endpoints completos
|-- requirements.txt
|-- Dockerfile
|-- readme.txt


===============================================================
 DOCKER (OPCIONAL)
===============================================================

Construir imagen:
  docker build -t api-mensajes .

Ejecutar contenedor:
  docker run -p 8000:8000 api-mensajes


===============================================================
 DECISIONES DE ARQUITECTURA
===============================================================

- Se eligio FastAPI por su soporte nativo de validacion con
  Pydantic, documentacion automatica y rendimiento.

- Arquitectura en capas (Controladores -> Servicios -> Repositorios)
  para separar responsabilidades segun principios SOLID.

- Inyeccion de dependencias usando el sistema built-in de FastAPI
  (Depends) para facilitar testing y desacoplamiento.

- SQLite con el modulo estandar sqlite3 para mantener simplicidad.
  La base de datos se crea automaticamente al iniciar el servidor.

- El filtro de contenido sanitiza (reemplaza con asteriscos) en
  lugar de rechazar mensajes, priorizando la experiencia de usuario.
