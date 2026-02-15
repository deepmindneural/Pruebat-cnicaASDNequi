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

## Endpoints

### POST /api/messages

Recibe un mensaje, lo valida, lo procesa y lo almacena en la base de datos. Si el mensaje tiene contenido inapropiado, se sanitiza automaticamente reemplazando las palabras con asteriscos.

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

Devuelve todos los mensajes de una sesion. Soporta paginacion con `limit` y `offset`, y se puede filtrar por `sender`.

Ejemplo: `GET /api/messages/session-abcdef?limit=10&offset=0&sender=user`

### Manejo de errores

Todos los errores devuelven un formato consistente:
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

Los codigos HTTP que maneja la API: 400 (datos invalidos), 404 (sesion no encontrada), 409 (mensaje duplicado) y 500 (error interno).

## Tests

Se incluyen pruebas unitarias para cada capa y pruebas de integracion para los endpoints.

```bash
pytest -v
pytest --cov=app
```

## Docker

```bash
docker build -t api-mensajes .
docker run -p 8000:8000 api-mensajes
```
