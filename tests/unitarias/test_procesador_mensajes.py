import pytest
from datetime import datetime

from app.esquemas.esquema_mensaje import MensajeEntrada
from app.servicios.procesador_mensajes import ProcesadorMensajes
from app.servicios.filtro_contenido import FiltroContenido
from app.excepciones.excepciones_api import ErrorFormatoInvalido


class TestProcesadorMensajes:
    def setup_method(self):
        filtro = FiltroContenido(palabras_prohibidas=["idiota", "mierda"])
        self.procesador = ProcesadorMensajes(filtro=filtro)

    def _crear_mensaje(self, **kwargs) -> MensajeEntrada:
        datos = {
            "message_id": "msg-001",
            "session_id": "session-001",
            "content": "Hola mundo",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": "user",
        }
        datos.update(kwargs)
        return MensajeEntrada(**datos)

    def test_procesar_mensaje_valido(self):
        mensaje = self._crear_mensaje()
        resultado = self.procesador.procesar(mensaje)
        assert resultado.message_id == "msg-001"
        assert resultado.content == "Hola mundo"
        assert resultado.metadata is not None

    def test_metadatos_conteo_palabras(self):
        mensaje = self._crear_mensaje(content="una dos tres cuatro")
        resultado = self.procesador.procesar(mensaje)
        assert resultado.metadata.word_count == 4

    def test_metadatos_conteo_caracteres(self):
        mensaje = self._crear_mensaje(content="Hola")
        resultado = self.procesador.procesar(mensaje)
        assert resultado.metadata.character_count == 4

    def test_processed_at_formato_iso(self):
        mensaje = self._crear_mensaje()
        resultado = self.procesador.procesar(mensaje)
        # Verificar que se puede parsear como ISO
        datetime.fromisoformat(resultado.metadata.processed_at)

    def test_contenido_solo_espacios_rechazado(self):
        mensaje = self._crear_mensaje(content="   ")
        with pytest.raises(ErrorFormatoInvalido):
            self.procesador.procesar(mensaje)

    def test_contenido_inapropiado_se_filtra(self):
        mensaje = self._crear_mensaje(content="Eres un idiota total")
        resultado = self.procesador.procesar(mensaje)
        assert "idiota" not in resultado.content
        assert "******" in resultado.content

    def test_campos_originales_se_preservan(self):
        mensaje = self._crear_mensaje()
        resultado = self.procesador.procesar(mensaje)
        assert resultado.session_id == "session-001"
        assert resultado.timestamp == "2023-06-15T14:30:00Z"
        assert resultado.sender == "user"
