import pytest

from app.esquemas.esquema_mensaje import MensajeEntrada
from app.excepciones.excepciones_api import ErrorSesionNoEncontrada, ErrorMensajeDuplicado


class TestServicioMensajes:
    def _crear_entrada(self, **kwargs) -> MensajeEntrada:
        datos = {
            "message_id": "msg-001",
            "session_id": "session-001",
            "content": "Hola mundo",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": "user",
        }
        datos.update(kwargs)
        return MensajeEntrada(**datos)

    def test_crear_mensaje_exitoso(self, servicio):
        entrada = self._crear_entrada()
        resultado = servicio.crear_mensaje(entrada)
        assert resultado.message_id == "msg-001"
        assert resultado.metadata is not None

    def test_crear_mensaje_tiene_metadatos(self, servicio):
        entrada = self._crear_entrada(content="una dos tres")
        resultado = servicio.crear_mensaje(entrada)
        assert resultado.metadata.word_count == 3
        assert resultado.metadata.character_count == 12

    def test_crear_mensaje_duplicado(self, servicio):
        entrada = self._crear_entrada()
        servicio.crear_mensaje(entrada)
        with pytest.raises(ErrorMensajeDuplicado):
            servicio.crear_mensaje(entrada)

    def test_obtener_mensajes_exitoso(self, servicio):
        servicio.crear_mensaje(self._crear_entrada())
        mensajes, total = servicio.obtener_mensajes_sesion("session-001")
        assert total == 1
        assert "metadata" in mensajes[0]
        assert mensajes[0]["metadata"]["word_count"] == 2

    def test_obtener_sesion_no_existente(self, servicio):
        with pytest.raises(ErrorSesionNoEncontrada):
            servicio.obtener_mensajes_sesion("no-existe")

    def test_obtener_con_paginacion(self, servicio):
        for i in range(5):
            servicio.crear_mensaje(
                self._crear_entrada(message_id=f"msg-{i}", timestamp=f"2023-06-15T14:3{i}:00Z")
            )
        mensajes, total = servicio.obtener_mensajes_sesion("session-001", limite=2)
        assert len(mensajes) == 2
        assert total == 5

    def test_obtener_con_filtro_remitente(self, servicio):
        servicio.crear_mensaje(self._crear_entrada(message_id="msg-001", sender="user"))
        servicio.crear_mensaje(self._crear_entrada(message_id="msg-002", sender="system"))
        mensajes, total = servicio.obtener_mensajes_sesion("session-001", remitente="system")
        assert total == 1
        assert mensajes[0]["sender"] == "system"
