class ErrorAPI(Exception):
    """Excepcion base para errores de la API."""

    def __init__(self, codigo: str, mensaje: str, detalles: str, codigo_http: int = 400):
        self.codigo = codigo
        self.mensaje = mensaje
        self.detalles = detalles
        self.codigo_http = codigo_http
        super().__init__(mensaje)


class ErrorFormatoInvalido(ErrorAPI):
    def __init__(self, detalles: str):
        super().__init__(
            codigo="INVALID_FORMAT",
            mensaje="Formato de mensaje invalido",
            detalles=detalles,
            codigo_http=400,
        )


class ErrorContenidoInapropiado(ErrorAPI):
    def __init__(self, detalles: str):
        super().__init__(
            codigo="INAPPROPRIATE_CONTENT",
            mensaje="El mensaje contiene contenido inapropiado",
            detalles=detalles,
            codigo_http=422,
        )


class ErrorSesionNoEncontrada(ErrorAPI):
    def __init__(self, session_id: str):
        super().__init__(
            codigo="SESSION_NOT_FOUND",
            mensaje="Sesion no encontrada",
            detalles=f"No se encontraron mensajes para la sesion: {session_id}",
            codigo_http=404,
        )


class ErrorMensajeDuplicado(ErrorAPI):
    def __init__(self, message_id: str):
        super().__init__(
            codigo="DUPLICATE_MESSAGE",
            mensaje="Mensaje duplicado",
            detalles=f"Ya existe un mensaje con el id: {message_id}",
            codigo_http=409,
        )
