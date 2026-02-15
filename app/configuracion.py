from functools import lru_cache


class Configuracion:
    """Configuracion central de la aplicacion."""

    NOMBRE_APP: str = "API de Procesamiento de Mensajes"
    VERSION: str = "1.0.0"
    RUTA_BASE_DATOS: str = "mensajes.db"
    LIMITE_PAGINACION_DEFECTO: int = 50
    LIMITE_PAGINACION_MAXIMO: int = 100

    # Lista de palabras que se filtran del contenido
    PALABRAS_PROHIBIDAS: list[str] = [
        "idiota", "estupido", "imbecil", "maldito", "carajo",
        "mierda", "puta", "bastardo", "pendejo", "cabron"
    ]


@lru_cache
def obtener_configuracion() -> Configuracion:
    return Configuracion()
