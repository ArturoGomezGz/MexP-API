""" from config.config import securitySesion, dataSourceSesion, authScheme, SHOW_ADMIN_ROUTES
from config.models.User import UserInDB
from config.models.Token import Token, TokenData
from config.models.ListaCodigoProductos import ListaCodigoProductos



from typing import List
from config.models.responsesProducto import Producto, ProductoExtendido, ProductoPrecioExist, Inventario, ProductoCotizacion
 """

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException

# Desplegar con:
#   uvicorn main:app --reload
#   uvicorn main:app --host localhost --port 8100 --reload
#   uvicorn main:app --host 0.0.0.0 --port 8100 --reload
#   uvicorn main:app --host 0.0.0.0 --port 8100 --reload > logs/uvicorn.log 2>&1

# Documentacion:
#   http://127.0.0.1:8000/docs
#   http://127.0.0.1:8000/redoc

""" def role_required(allowed_roles: List[str] = [rol["nombre_rol"] for rol in securitySesion.getRoles()]):
    def role_checker(token: str = Depends(authScheme)):
        user_data = securitySesion.verifyToken(token)
        if user_data is None or securitySesion.getRoleName(user_data.user_role) not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return user_data
    return role_checker """

app = FastAPI()

@app.get("/", tags=["General"])
# Endpoint de bienvenida
def wellcome():
    return {"message": "Puto el que lo lea"}

