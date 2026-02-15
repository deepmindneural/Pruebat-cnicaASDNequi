from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.esquemas.esquema_mensaje import MensajeEntrada
from app.esquemas.esquema_respuesta import RespuestaExitosa, RespuestaError, RespuestaListaMensajes
from app.servicios.servicio_mensajes import ServicioMensajes
from app.dependencias import obtener_servicio_mensajes

enrutador = APIRouter(prefix="/api", tags=["mensajes"])


@enrutador.post(
    "/messages",
    response_model=RespuestaExitosa,
    status_code=201,
    responses={
        400: {"model": RespuestaError},
        409: {"model": RespuestaError},
        422: {"model": RespuestaError},
    },
)
def crear_mensaje(
    mensaje: MensajeEntrada,
    servicio: ServicioMensajes = Depends(obtener_servicio_mensajes),
) -> dict:
    """Recibe, valida, procesa y almacena un mensaje de chat."""
    mensaje_procesado = servicio.crear_mensaje(mensaje)
    return {"status": "success", "data": mensaje_procesado.model_dump()}


@enrutador.get(
    "/messages/{session_id}",
    response_model=RespuestaListaMensajes,
    responses={404: {"model": RespuestaError}},
)
def obtener_mensajes(
    session_id: str,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    sender: Optional[str] = Query(default=None, pattern="^(user|system)$"),
    servicio: ServicioMensajes = Depends(obtener_servicio_mensajes),
) -> dict:
    """Recupera mensajes de una sesion con paginacion y filtrado."""
    mensajes, total = servicio.obtener_mensajes_sesion(
        session_id=session_id,
        limite=limit,
        desplazamiento=offset,
        remitente=sender,
    )
    return {
        "status": "success",
        "data": mensajes,
        "pagination": {"total": total, "limit": limit, "offset": offset},
    }
