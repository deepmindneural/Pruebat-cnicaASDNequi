from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.excepciones.excepciones_api import ErrorAPI


async def manejar_error_api(request: Request, exc: ErrorAPI) -> JSONResponse:
    return JSONResponse(
        status_code=exc.codigo_http,
        content={
            "status": "error",
            "error": {
                "code": exc.codigo,
                "message": exc.mensaje,
                "details": exc.detalles,
            },
        },
    )


async def manejar_error_validacion(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Convierte errores de validacion de Pydantic al formato estandar."""
    errores = exc.errors()
    if errores:
        primer_error = errores[0]
        campo = " -> ".join(str(loc) for loc in primer_error.get("loc", []) if loc != "body")
        detalle = primer_error.get("msg", "Error de validacion")
    else:
        campo = "desconocido"
        detalle = "Error de validacion"

    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Error de validacion en los datos enviados",
                "details": f"Campo '{campo}': {detalle}",
            },
        },
    )


async def manejar_error_interno(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Error interno del servidor",
                "details": "Ocurrio un error inesperado. Intente nuevamente.",
            },
        },
    )


def registrar_manejadores_errores(aplicacion: FastAPI):
    aplicacion.add_exception_handler(ErrorAPI, manejar_error_api)
    aplicacion.add_exception_handler(RequestValidationError, manejar_error_validacion)
    aplicacion.add_exception_handler(Exception, manejar_error_interno)
