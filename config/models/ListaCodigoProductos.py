from pydantic import BaseModel
from typing import List

class ListaCodigoProductos(BaseModel):
    productos: List[str]
