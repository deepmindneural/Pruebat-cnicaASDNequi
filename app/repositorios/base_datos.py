import sqlite3

from app.configuracion import obtener_configuracion

ESQUEMA_SQL = """
CREATE TABLE IF NOT EXISTS mensajes (
    message_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    sender TEXT NOT NULL CHECK(sender IN ('user', 'system')),
    word_count INTEGER NOT NULL,
    character_count INTEGER NOT NULL,
    processed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_session_id ON mensajes(session_id);
CREATE INDEX IF NOT EXISTS idx_sender ON mensajes(sender);
CREATE INDEX IF NOT EXISTS idx_timestamp ON mensajes(timestamp);
"""


def obtener_conexion(ruta_bd: str | None = None) -> sqlite3.Connection:
    config = obtener_configuracion()
    ruta = ruta_bd or config.RUTA_BASE_DATOS
    conexion = sqlite3.connect(ruta, check_same_thread=False)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA journal_mode=WAL")
    return conexion


def inicializar_base_datos(ruta_bd: str | None = None):
    conexion = obtener_conexion(ruta_bd)
    conexion.executescript(ESQUEMA_SQL)
    conexion.close()
