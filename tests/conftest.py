import sqlite3
import pytest
from fastapi.testclient import TestClient

from app.principal import crear_aplicacion
from app.repositorios.base_datos import ESQUEMA_SQL
from app.repositorios.repositorio_mensajes import RepositorioMensajes
from app.servicios.servicio_mensajes import ServicioMensajes
from app.servicios.procesador_mensajes import ProcesadorMensajes
from app.servicios.filtro_contenido import FiltroContenido
from app.dependencias import obtener_servicio_mensajes


@pytest.fixture
def conexion_bd():
    """Base de datos SQLite en memoria para tests."""
    conexion = sqlite3.connect(":memory:", check_same_thread=False)
    conexion.row_factory = sqlite3.Row
    conexion.executescript(ESQUEMA_SQL)
    yield conexion
    conexion.close()


@pytest.fixture
def repositorio(conexion_bd):
    return RepositorioMensajes(conexion_bd)


@pytest.fixture
def filtro():
    return FiltroContenido(palabras_prohibidas=["idiota", "mierda", "estupido"])


@pytest.fixture
def procesador(filtro):
    return ProcesadorMensajes(filtro=filtro)


@pytest.fixture
def servicio(repositorio, procesador):
    return ServicioMensajes(repositorio=repositorio, procesador=procesador)


@pytest.fixture
def cliente(conexion_bd):
    """Cliente HTTP con dependencias sobreescritas para usar BD en memoria."""
    app = crear_aplicacion()

    def _servicio_test():
        repo = RepositorioMensajes(conexion_bd)
        filtro = FiltroContenido(palabras_prohibidas=["idiota", "mierda", "estupido"])
        proc = ProcesadorMensajes(filtro=filtro)
        return ServicioMensajes(repositorio=repo, procesador=proc)

    app.dependency_overrides[obtener_servicio_mensajes] = _servicio_test
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def mensaje_valido():
    """Datos de ejemplo de un mensaje valido."""
    return {
        "message_id": "msg-123456",
        "session_id": "session-abcdef",
        "content": "Hola, como puedo ayudarte hoy?",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "system",
    }
