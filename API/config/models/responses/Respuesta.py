from pydantic import BaseModel

class Respuesta(BaseModel):
    mensaje: str
    estatus: int