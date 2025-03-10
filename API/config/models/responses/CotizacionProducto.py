from pydantic import BaseModel

class CotizacionProducto(BaseModel):
    idCotizacion: int
    idProducto: int
    cantidad: int
    unitario: float
    existencia: int