# API de Procesamiento de Mensajes de Chat

API para recibir, procesar y almacenar mensajes de chat.

## Tecnologias

- Python 3.10
- FastAPI
- SQLite
- Pytest

## Como correr el proyecto

```bash
git clone https://github.com/deepmindneural/Pruebat-cnicaASDNequi.git
cd Pruebat-cnicaASDNequi

python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
uvicorn app.principal:aplicacion --reload
```

Abrir `http://localhost:8000/docs` para ver la documentacion interactiva.

## Endpoints

### POST /api/messages

Envia un mensaje para ser procesado y almacenado.

```json
{
  "message_id": "msg-123456",
  "session_id": "session-abcdef",
  "content": "Hola, como puedo ayudarte hoy?",
  "timestamp": "2023-06-15T14:30:00Z",
  "sender": "system"
}
```

### GET /api/messages/{session_id}

Obtiene los mensajes de una sesion.

Se puede filtrar por `sender` y paginar con `limit` y `offset`.

Ejemplo: `GET /api/messages/session-abcdef?limit=10&sender=user`

## Tests

```bash
pytest -v
pytest --cov=app
```

## Docker

```bash
docker build -t api-mensajes .
docker run -p 8000:8000 api-mensajes
```
