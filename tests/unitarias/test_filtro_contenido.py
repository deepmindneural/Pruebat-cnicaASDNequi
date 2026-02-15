from app.servicios.filtro_contenido import FiltroContenido


class TestFiltroContenido:
    def setup_method(self):
        self.filtro = FiltroContenido(palabras_prohibidas=["idiota", "mierda", "estupido"])

    def test_texto_limpio(self):
        es_inapropiado, encontradas = self.filtro.contiene_contenido_inapropiado("Hola, buen dia")
        assert es_inapropiado is False
        assert encontradas == []

    def test_detecta_palabra_prohibida(self):
        es_inapropiado, encontradas = self.filtro.contiene_contenido_inapropiado("Eres un idiota")
        assert es_inapropiado is True
        assert "idiota" in encontradas

    def test_detecta_multiples_palabras(self):
        es_inapropiado, encontradas = self.filtro.contiene_contenido_inapropiado("idiota y mierda")
        assert es_inapropiado is True
        assert len(encontradas) == 2

    def test_no_detecta_subcadenas(self):
        """No debe dar falso positivo con palabras que contengan la prohibida como subcadena."""
        es_inapropiado, _ = self.filtro.contiene_contenido_inapropiado("El analisis fue solido")
        assert es_inapropiado is False

    def test_deteccion_case_insensitive(self):
        es_inapropiado, encontradas = self.filtro.contiene_contenido_inapropiado("Eres IDIOTA")
        assert es_inapropiado is True

    def test_filtrar_reemplaza_con_asteriscos(self):
        resultado = self.filtro.filtrar_contenido("Eres un idiota")
        assert "idiota" not in resultado
        assert "******" in resultado  # len("idiota") = 6

    def test_filtrar_texto_limpio_sin_cambios(self):
        texto = "Hola, todo bien"
        resultado = self.filtro.filtrar_contenido(texto)
        assert resultado == texto
