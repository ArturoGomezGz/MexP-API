from pydantic import BaseModel

class Notificacion(BaseModel):
    email: str
    mensaje: str