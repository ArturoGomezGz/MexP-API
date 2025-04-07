from typing import List
from config.models.Token import Token, TokenData
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, Security
from config.models.User import UserCreate
from config.config import securitySesion, dataSourceSesion, authScheme, SHOW_ADMIN_ROUTES

# Desplegar con:
#   uvicorn main:app --reload
#   uvicorn main:app --host localhost --port 8100 --reload
#   uvicorn main:app --host 0.0.0.0 --port 8100 --reload
#   uvicorn main:app --host 0.0.0.0 --port 8100 --reload > logs/uvicorn.log 2>&1

# Documentacion:
#   http://127.0.0.1:8000/docs
#   http://127.0.0.1:8000/redoc

def role_required(allowed_roles: List[str] = ["Administrador","Escuela","Aliado"]):
    def role_checker(token: str = Depends(authScheme)):
        user_data = securitySesion.verifyToken(token)
        if user_data is None or user_data.rol not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return user_data
    return role_checker

app = FastAPI()

@app.get("/", tags=["General"])
def wellcome():
    return {"message": "Bienvanido a la api de Mexicanos Primero"}

@app.post("/token", tags=["Authentication"])
def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return securitySesion.createToken(form_data.username, form_data.password)

@app.post("/escuela/create", tags=["User Management"])
def nuevo_usuario(nombre: str, email: str, direccion: str, password: str):
    return securitySesion.createUser(nombre, email, direccion, 2, password)

@app.post("/aliado/create", tags=["User Management"])
def nuevo_usuario(nombre: str, email: str, direccion: str, password: str):
    return securitySesion.createUser(nombre, email, direccion, 3, password)

@app.post("/admin/create", tags=["User Management"])
def nuevo_usuario(nombre: str, email: str, direccion: str, password: str):
    return securitySesion.createUser(nombre, email, direccion, 1, password)

@app.delete("/user/delete", tags=["User Management"])
def eliminar_usuario(user_data: TokenData = Depends(role_required())):
    return securitySesion.deleteUser(user_data.email)

@app.post("/user/change-password", tags=["User Management"])
def change_password(new_password, user_data: TokenData = Depends(role_required())):
    return securitySesion.changePassword(user_data.email, new_password)

@app.post("/admin/user/create", tags=["Admin"])
def nuevo_usuario(nombre: str, email: str, direccion: str, rol: int, password: str, user_data: TokenData = Depends(role_required(["Administrador"]))):
    return securitySesion.createUser(nombre, email, direccion, rol, password)

@app.delete("/admin/user/delete", tags=["Admin"])
def eliminar_usuario(email: str, user_data: TokenData = Depends(role_required(["Administrador"]))):
    return securitySesion.deleteUser(email)

@app.get("/admin/user/change-rol", tags=["Admin"])
def cambiar_rol(email: str, rol: int, user_data: TokenData = Depends(role_required(["Administrador"]))):
    return securitySesion.changeRol(email, rol)


# Obtener informacion reelvante al desarrollo de la aplicacion

@app.get("/user/{email}")
def obtener_informacion_usuario(email: str, user_data: TokenData = Depends(role_required(["Administrador"]))):
    return dataSourceSesion.getUsuario(email)

@app.get("/user-roles")
def obtener_roles():
    return dataSourceSesion.getRoles()
