class TestPostMensajes:
    def test_crear_mensaje_201(self, cliente, mensaje_valido):
        resp = cliente.post("/api/messages", json=mensaje_valido)
        assert resp.status_code == 201
        datos = resp.json()
        assert datos["status"] == "success"
        assert datos["data"]["message_id"] == "msg-123456"

    def test_respuesta_tiene_metadatos(self, cliente, mensaje_valido):
        resp = cliente.post("/api/messages", json=mensaje_valido)
        datos = resp.json()
        metadata = datos["data"]["metadata"]
        assert "word_count" in metadata
        assert "character_count" in metadata
        assert "processed_at" in metadata

    def test_sin_campos_requeridos_400(self, cliente):
        resp = cliente.post("/api/messages", json={"message_id": "msg-001"})
        assert resp.status_code == 400
        datos = resp.json()
        assert datos["status"] == "error"
        assert datos["error"]["code"] == "VALIDATION_ERROR"

    def test_sender_invalido_400(self, cliente, mensaje_valido):
        mensaje_valido["sender"] = "bot"
        resp = cliente.post("/api/messages", json=mensaje_valido)
        assert resp.status_code == 400

    def test_timestamp_invalido_400(self, cliente, mensaje_valido):
        mensaje_valido["timestamp"] = "fecha-invalida"
        resp = cliente.post("/api/messages", json=mensaje_valido)
        assert resp.status_code == 400

    def test_mensaje_duplicado_409(self, cliente, mensaje_valido):
        cliente.post("/api/messages", json=mensaje_valido)
        resp = cliente.post("/api/messages", json=mensaje_valido)
        assert resp.status_code == 409
        assert resp.json()["error"]["code"] == "DUPLICATE_MESSAGE"

    def test_contenido_inapropiado_se_filtra(self, cliente, mensaje_valido):
        mensaje_valido["content"] = "Eres un idiota"
        resp = cliente.post("/api/messages", json=mensaje_valido)
        assert resp.status_code == 201
        assert "idiota" not in resp.json()["data"]["content"]

    def test_body_vacio_400(self, cliente):
        resp = cliente.post("/api/messages", content=b"", headers={"Content-Type": "application/json"})
        assert resp.status_code == 400

    def test_body_no_json_400(self, cliente):
        resp = cliente.post("/api/messages", content=b"no es json", headers={"Content-Type": "application/json"})
        assert resp.status_code == 400


class TestGetMensajes:
    def _insertar_mensaje(self, cliente, message_id="msg-001", session_id="session-001", sender="user"):
        return cliente.post("/api/messages", json={
            "message_id": message_id,
            "session_id": session_id,
            "content": "Mensaje de prueba",
            "timestamp": "2023-06-15T14:30:00Z",
            "sender": sender,
        })

    def test_obtener_mensajes_200(self, cliente):
        self._insertar_mensaje(cliente)
        resp = cliente.get("/api/messages/session-001")
        assert resp.status_code == 200
        datos = resp.json()
        assert datos["status"] == "success"
        assert len(datos["data"]) == 1

    def test_sesion_no_existente_404(self, cliente):
        resp = cliente.get("/api/messages/no-existe")
        assert resp.status_code == 404
        assert resp.json()["error"]["code"] == "SESSION_NOT_FOUND"

    def test_paginacion_limit(self, cliente):
        for i in range(5):
            self._insertar_mensaje(cliente, message_id=f"msg-{i}")
        resp = cliente.get("/api/messages/session-001?limit=2")
        assert len(resp.json()["data"]) == 2

    def test_paginacion_offset(self, cliente):
        for i in range(5):
            self._insertar_mensaje(cliente, message_id=f"msg-{i}")
        resp = cliente.get("/api/messages/session-001?limit=10&offset=3")
        assert len(resp.json()["data"]) == 2

    def test_filtro_sender(self, cliente):
        self._insertar_mensaje(cliente, message_id="msg-001", sender="user")
        self._insertar_mensaje(cliente, message_id="msg-002", sender="system")
        resp = cliente.get("/api/messages/session-001?sender=system")
        datos = resp.json()
        assert datos["pagination"]["total"] == 1
        assert datos["data"][0]["sender"] == "system"

    def test_paginacion_metadata(self, cliente):
        for i in range(3):
            self._insertar_mensaje(cliente, message_id=f"msg-{i}")
        resp = cliente.get("/api/messages/session-001?limit=2&offset=0")
        pag = resp.json()["pagination"]
        assert pag["total"] == 3
        assert pag["limit"] == 2
        assert pag["offset"] == 0

    def test_respuesta_tiene_metadata_anidada(self, cliente):
        self._insertar_mensaje(cliente)
        resp = cliente.get("/api/messages/session-001")
        mensaje = resp.json()["data"][0]
        assert "metadata" in mensaje
        assert "word_count" in mensaje["metadata"]

    def test_formato_error_consistente(self, cliente):
        resp = cliente.get("/api/messages/no-existe")
        error = resp.json()
        assert "status" in error
        assert "error" in error
        assert "code" in error["error"]
        assert "message" in error["error"]
        assert "details" in error["error"]
