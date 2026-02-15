from datetime import datetime, timezone

from app.esquemas.esquema_mensaje import MensajeEntrada, MensajeProcesado, MetadatosMensaje
from app.servicios.filtro_contenido import FiltroContenido
from app.excepciones.excepciones_api import ErrorFormatoInvalido


class ProcesadorMensajes:
    """Pipeline de procesamiento: validar -> filtrar -> metadatos."""

    def __init__(self, filtro: FiltroContenido | None = None):
        self._filtro = filtro or FiltroContenido()

    def procesar(self, mensaje: MensajeEntrada) -> MensajeProcesado:
        self._validar_formato(mensaje)
        contenido_limpio = self._filtrar_contenido(mensaje.content)
        metadatos = self._generar_metadatos(contenido_limpio)

        return MensajeProcesado(
            message_id=mensaje.message_id,
            session_id=mensaje.session_id,
            content=contenido_limpio,
            timestamp=mensaje.timestamp,
            sender=mensaje.sender,
            metadata=metadatos,
        )

    def _validar_formato(self, mensaje: MensajeEntrada) -> None:
        if not mensaje.content.strip():
            raise ErrorFormatoInvalido(
                "El contenido del mensaje no puede estar vacio o ser solo espacios"
            )

    def _filtrar_contenido(self, contenido: str) -> str:
        """Si hay palabras inapropiadas, las reemplaza con asteriscos."""
        es_inapropiado, _ = self._filtro.contiene_contenido_inapropiado(contenido)
        if es_inapropiado:
            return self._filtro.filtrar_contenido(contenido)
        return contenido

    def _generar_metadatos(self, contenido: str) -> MetadatosMensaje:
        return MetadatosMensaje(
            word_count=len(contenido.split()),
            character_count=len(contenido),
            processed_at=datetime.now(timezone.utc).isoformat(),
        )
