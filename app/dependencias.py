from app.repositorios.base_datos import obtener_conexion
from app.repositorios.repositorio_mensajes import RepositorioMensajes
from app.servicios.servicio_mensajes import ServicioMensajes


def obtener_servicio_mensajes() -> ServicioMensajes:
    """Proveedor de dependencias para el servicio de mensajes."""
    conexion = obtener_conexion()
    repositorio = RepositorioMensajes(conexion)
    return ServicioMensajes(repositorio=repositorio)
