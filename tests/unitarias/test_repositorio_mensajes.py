import pytest

from app.repositorios.repositorio_mensajes import RepositorioMensajes
from app.excepciones.excepciones_api import ErrorMensajeDuplicado


class TestRepositorioMensajes:
    def _datos_mensaje(self, **kwargs) -> dict:
        datos = {
            "message_id": "msg-001",
            "session_id": "session-001",
            "content": "Hola mundo",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": "user",
            "word_count": 2,
            "character_count": 10,
            "processed_at": "2023-06-15T14:30:01Z",
        }
        datos.update(kwargs)
        return datos

    def test_guardar_mensaje(self, repositorio):
        datos = self._datos_mensaje()
        repositorio.guardar_mensaje(datos)
        mensajes, total = repositorio.obtener_mensajes_por_sesion("session-001")
        assert total == 1
        assert mensajes[0]["message_id"] == "msg-001"

    def test_guardar_mensaje_duplicado(self, repositorio):
        datos = self._datos_mensaje()
        repositorio.guardar_mensaje(datos)
        with pytest.raises(ErrorMensajeDuplicado):
            repositorio.guardar_mensaje(datos)

    def test_obtener_por_sesion(self, repositorio):
        repositorio.guardar_mensaje(self._datos_mensaje(message_id="msg-001", session_id="s1"))
        repositorio.guardar_mensaje(self._datos_mensaje(message_id="msg-002", session_id="s1"))
        repositorio.guardar_mensaje(self._datos_mensaje(message_id="msg-003", session_id="s2"))

        mensajes, total = repositorio.obtener_mensajes_por_sesion("s1")
        assert total == 2
        assert len(mensajes) == 2

    def test_sesion_sin_mensajes(self, repositorio):
        mensajes, total = repositorio.obtener_mensajes_por_sesion("no-existe")
        assert total == 0
        assert mensajes == []

    def test_paginacion_limit(self, repositorio):
        for i in range(5):
            repositorio.guardar_mensaje(
                self._datos_mensaje(message_id=f"msg-{i}", session_id="s1", timestamp=f"2023-06-15T14:3{i}:00Z")
            )
        mensajes, total = repositorio.obtener_mensajes_por_sesion("s1", limite=3)
        assert len(mensajes) == 3
        assert total == 5

    def test_paginacion_offset(self, repositorio):
        for i in range(5):
            repositorio.guardar_mensaje(
                self._datos_mensaje(message_id=f"msg-{i}", session_id="s1", timestamp=f"2023-06-15T14:3{i}:00Z")
            )
        mensajes, total = repositorio.obtener_mensajes_por_sesion("s1", limite=3, desplazamiento=3)
        assert len(mensajes) == 2
        assert total == 5

    def test_filtro_por_remitente(self, repositorio):
        repositorio.guardar_mensaje(self._datos_mensaje(message_id="msg-001", sender="user"))
        repositorio.guardar_mensaje(self._datos_mensaje(message_id="msg-002", sender="system"))

        mensajes, total = repositorio.obtener_mensajes_por_sesion("session-001", remitente="user")
        assert total == 1
        assert mensajes[0]["sender"] == "user"

    def test_orden_por_timestamp(self, repositorio):
        repositorio.guardar_mensaje(
            self._datos_mensaje(message_id="msg-002", timestamp="2023-06-15T15:00:00Z")
        )
        repositorio.guardar_mensaje(
            self._datos_mensaje(message_id="msg-001", timestamp="2023-06-15T14:00:00Z")
        )
        mensajes, _ = repositorio.obtener_mensajes_por_sesion("session-001")
        assert mensajes[0]["message_id"] == "msg-001"
        assert mensajes[1]["message_id"] == "msg-002"
