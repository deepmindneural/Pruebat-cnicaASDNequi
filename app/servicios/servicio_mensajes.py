from typing import Optional

from app.repositorios.repositorio_mensajes import RepositorioMensajes
from app.servicios.procesador_mensajes import ProcesadorMensajes
from app.esquemas.esquema_mensaje import MensajeEntrada, MensajeProcesado
from app.excepciones.excepciones_api import ErrorSesionNoEncontrada


class ServicioMensajes:
    """Servicio principal que orquesta procesamiento y persistencia."""

    def __init__(self, repositorio: RepositorioMensajes, procesador: ProcesadorMensajes | None = None):
        self._repositorio = repositorio
        self._procesador = procesador or ProcesadorMensajes()

    def crear_mensaje(self, mensaje: MensajeEntrada) -> MensajeProcesado:
        mensaje_procesado = self._procesador.procesar(mensaje)

        # Aplanar datos para guardar en BD
        datos = {
            "message_id": mensaje_procesado.message_id,
            "session_id": mensaje_procesado.session_id,
            "content": mensaje_procesado.content,
            "timestamp": mensaje_procesado.timestamp,
            "sender": mensaje_procesado.sender,
            "word_count": mensaje_procesado.metadata.word_count,
            "character_count": mensaje_procesado.metadata.character_count,
            "processed_at": mensaje_procesado.metadata.processed_at,
        }
        self._repositorio.guardar_mensaje(datos)
        return mensaje_procesado

    def obtener_mensajes_sesion(
        self,
        session_id: str,
        limite: int = 50,
        desplazamiento: int = 0,
        remitente: Optional[str] = None,
    ) -> tuple[list[dict], int]:
        mensajes, total = self._repositorio.obtener_mensajes_por_sesion(
            session_id=session_id,
            limite=limite,
            desplazamiento=desplazamiento,
            remitente=remitente,
        )

        if total == 0 and desplazamiento == 0:
            raise ErrorSesionNoEncontrada(session_id)

        # Reestructurar filas planas a formato con metadata anidada
        resultado = []
        for msg in mensajes:
            resultado.append({
                "message_id": msg["message_id"],
                "session_id": msg["session_id"],
                "content": msg["content"],
                "timestamp": msg["timestamp"],
                "sender": msg["sender"],
                "metadata": {
                    "word_count": msg["word_count"],
                    "character_count": msg["character_count"],
                    "processed_at": msg["processed_at"],
                },
            })

        return resultado, total
