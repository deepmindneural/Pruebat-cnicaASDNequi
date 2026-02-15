import pytest
from pydantic import ValidationError

from app.esquemas.esquema_mensaje import MensajeEntrada


class TestMensajeEntrada:
    def test_mensaje_valido(self, mensaje_valido):
        mensaje = MensajeEntrada(**mensaje_valido)
        assert mensaje.message_id == "msg-123456"
        assert mensaje.sender == "system"

    def test_falta_message_id(self, mensaje_valido):
        del mensaje_valido["message_id"]
        with pytest.raises(ValidationError):
            MensajeEntrada(**mensaje_valido)

    def test_falta_session_id(self, mensaje_valido):
        del mensaje_valido["session_id"]
        with pytest.raises(ValidationError):
            MensajeEntrada(**mensaje_valido)

    def test_falta_content(self, mensaje_valido):
        del mensaje_valido["content"]
        with pytest.raises(ValidationError):
            MensajeEntrada(**mensaje_valido)

    def test_falta_timestamp(self, mensaje_valido):
        del mensaje_valido["timestamp"]
        with pytest.raises(ValidationError):
            MensajeEntrada(**mensaje_valido)

    def test_falta_sender(self, mensaje_valido):
        del mensaje_valido["sender"]
        with pytest.raises(ValidationError):
            MensajeEntrada(**mensaje_valido)

    def test_sender_invalido(self, mensaje_valido):
        mensaje_valido["sender"] = "bot"
        with pytest.raises(ValidationError):
            MensajeEntrada(**mensaje_valido)

    def test_timestamp_invalido(self, mensaje_valido):
        mensaje_valido["timestamp"] = "no-es-fecha"
        with pytest.raises(ValidationError):
            MensajeEntrada(**mensaje_valido)

    def test_content_vacio(self, mensaje_valido):
        mensaje_valido["content"] = ""
        with pytest.raises(ValidationError):
            MensajeEntrada(**mensaje_valido)

    def test_message_id_vacio(self, mensaje_valido):
        mensaje_valido["message_id"] = ""
        with pytest.raises(ValidationError):
            MensajeEntrada(**mensaje_valido)

    def test_sender_user_valido(self, mensaje_valido):
        mensaje_valido["sender"] = "user"
        mensaje = MensajeEntrada(**mensaje_valido)
        assert mensaje.sender == "user"

    def test_timestamp_con_zona_horaria(self, mensaje_valido):
        mensaje_valido["timestamp"] = "2023-06-15T14:30:00+05:00"
        mensaje = MensajeEntrada(**mensaje_valido)
        assert mensaje.timestamp == "2023-06-15T14:30:00+05:00"
