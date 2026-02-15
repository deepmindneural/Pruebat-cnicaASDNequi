import sqlite3
from typing import Optional

from app.excepciones.excepciones_api import ErrorMensajeDuplicado


class RepositorioMensajes:
    """Capa de acceso a datos para mensajes."""

    def __init__(self, conexion: sqlite3.Connection):
        self._conexion = conexion

    def guardar_mensaje(self, datos: dict) -> None:
        consulta = """
            INSERT INTO mensajes (message_id, session_id, content, timestamp, sender,
                                  word_count, character_count, processed_at)
            VALUES (:message_id, :session_id, :content, :timestamp, :sender,
                    :word_count, :character_count, :processed_at)
        """
        try:
            self._conexion.execute(consulta, datos)
            self._conexion.commit()
        except sqlite3.IntegrityError:
            raise ErrorMensajeDuplicado(datos["message_id"])

    def obtener_mensajes_por_sesion(
        self,
        session_id: str,
        limite: int = 50,
        desplazamiento: int = 0,
        remitente: Optional[str] = None,
    ) -> tuple[list[dict], int]:
        """Recupera mensajes paginados para una sesion. Retorna (mensajes, total)."""
        condiciones = ["session_id = ?"]
        parametros: list = [session_id]

        if remitente:
            condiciones.append("sender = ?")
            parametros.append(remitente)

        clausula_where = " AND ".join(condiciones)

        # Contar total para metadata de paginacion
        consulta_total = f"SELECT COUNT(*) FROM mensajes WHERE {clausula_where}"
        total = self._conexion.execute(consulta_total, parametros).fetchone()[0]

        # Consulta con paginacion
        consulta = f"""
            SELECT * FROM mensajes
            WHERE {clausula_where}
            ORDER BY timestamp ASC
            LIMIT ? OFFSET ?
        """
        parametros.extend([limite, desplazamiento])
        filas = self._conexion.execute(consulta, parametros).fetchall()
        mensajes = [dict(fila) for fila in filas]

        return mensajes, total

    def cerrar(self):
        self._conexion.close()
