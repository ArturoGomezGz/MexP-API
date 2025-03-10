from pydantic import BaseModel
from config.models.responses.Codigo import Codigo
from config.models.responses.Sal import Sal
from typing import List

class Producto(BaseModel):
    id: int
    codigo: str
    nombre: str
    presentacion: str
    tipoUnidad: str
    status: int
    codigos: List[Codigo]

class ProductoExtendido(Producto):
    laboratorio: str
    categoria: str
    precio: float
    iva: bool
    caja: int
    equivalente: str
    especieDescuento: str
    formula: str
    existencia: bool
    restringido: bool
    cantidad: int
    estadoDesc: str
    satClave: str
    sales: List[Sal]  # Suponiendo que almacena referencias de ventas
    usos: List[str]  # Suponiendo que almacena referencias de usos

class ProductoPrecioExist(BaseModel):
    id: int
    existencia: int
    unitario: float 

class Inventario(BaseModel):
    id: int
    cantidad: int

class ProductoCotizacion(BaseModel):
    id: int
    cantidad: int