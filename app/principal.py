from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.configuracion import obtener_configuracion
from app.controladores.rutas_mensajes import enrutador
from app.excepciones.manejador_errores import registrar_manejadores_errores
from app.repositorios.base_datos import inicializar_base_datos


@asynccontextmanager
async def ciclo_vida(app: FastAPI):
    # Al iniciar: crear tablas si no existen
    inicializar_base_datos()
    yield


def crear_aplicacion() -> FastAPI:
    config = obtener_configuracion()

    app = FastAPI(
        title=config.NOMBRE_APP,
        version=config.VERSION,
        description="API RESTful para procesamiento y almacenamiento de mensajes de chat",
        lifespan=ciclo_vida,
    )

    app.include_router(enrutador)
    registrar_manejadores_errores(app)

    return app


aplicacion = crear_aplicacion()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.principal:aplicacion", host="0.0.0.0", port=8000, reload=True)
