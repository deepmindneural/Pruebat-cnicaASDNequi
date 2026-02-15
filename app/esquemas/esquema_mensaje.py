from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal


class MensajeEntrada(BaseModel):
    """Modelo de validacion para mensajes entrantes."""

    message_id: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1, max_length=5000)
    timestamp: str = Field(...)
    sender: Literal["user", "system"] = Field(...)

    @field_validator("timestamp")
    @classmethod
    def validar_timestamp(cls, valor: str) -> str:
        try:
            datetime.fromisoformat(valor.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            raise ValueError("El timestamp debe tener formato ISO 8601 valido")
        return valor


class MetadatosMensaje(BaseModel):
    """Metadatos generados durante el procesamiento."""

    word_count: int
    character_count: int
    processed_at: str


class MensajeProcesado(BaseModel):
    """Mensaje con metadatos despues del procesamiento."""

    message_id: str
    session_id: str
    content: str
    timestamp: str
    sender: str
    metadata: MetadatosMensaje
