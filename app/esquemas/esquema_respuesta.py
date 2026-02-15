from pydantic import BaseModel
from typing import Any


class DetalleError(BaseModel):
    code: str
    message: str
    details: str


class RespuestaExitosa(BaseModel):
    status: str = "success"
    data: Any


class RespuestaError(BaseModel):
    status: str = "error"
    error: DetalleError


class RespuestaListaMensajes(BaseModel):
    status: str = "success"
    data: list[dict]
    pagination: dict
