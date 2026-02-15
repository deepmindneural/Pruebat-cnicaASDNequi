import re

from app.configuracion import obtener_configuracion


class FiltroContenido:
    """Filtro simple de palabras inapropiadas."""

    def __init__(self, palabras_prohibidas: list[str] | None = None):
        config = obtener_configuracion()
        self._palabras_prohibidas = palabras_prohibidas or config.PALABRAS_PROHIBIDAS

    def contiene_contenido_inapropiado(self, texto: str) -> tuple[bool, list[str]]:
        """Verifica si el texto tiene palabras prohibidas. Retorna (bool, palabras_encontradas)."""
        texto_lower = texto.lower()
        encontradas = []
        for palabra in self._palabras_prohibidas:
            patron = rf"\b{re.escape(palabra.lower())}\b"
            if re.search(patron, texto_lower):
                encontradas.append(palabra)
        return len(encontradas) > 0, encontradas

    def filtrar_contenido(self, texto: str) -> str:
        """Reemplaza palabras prohibidas con asteriscos."""
        resultado = texto
        for palabra in self._palabras_prohibidas:
            patron = re.compile(rf"\b{re.escape(palabra)}\b", re.IGNORECASE)
            resultado = patron.sub("*" * len(palabra), resultado)
        return resultado
