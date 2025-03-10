from pydantic import BaseModel
from typing import Optional

class Factura(BaseModel):
    id: int
    folioFiscal: str
    fecha: str
    vencimiento: str
    cancelada: Optional[str]
    estatus: str
    porte: Optional[str]
    documento:  str
    tipoEnvio: str
    transportista: Optional[str]
    direccion: str
    cp: str
    ciudad: str
    estado: str
    guia: Optional[str]
    productos: int
    cajas: int
    bultos: int
    subtotal: float
    descMonto: float
    ivaMonto: float
    total: float