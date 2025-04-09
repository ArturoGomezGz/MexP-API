from typing import List
from config.models.Token import Token, TokenData
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, Security
from config.models.User import UserCreate
from config.config import securitySesion, dataSourceSesion, authScheme, SHOW_ADMIN_ROUTES
from fastapi.middleware.cors import CORSMiddleware

# Modelos
from config.models.TiposNecesidades import TiposNecesidades
from config.models.Notificacion import Notificacion

# Desplegar con:
#   uvicorn main:app --reload
#   uvicorn main:app --host localhost --port 8100 --reload
#   uvicorn main:app --host 0.0.0.0 --port 8100 --reload
#   uvicorn main:app --host 0.0.0.0 --port 8100 --reload > logs/uvicorn.log 2>&1
#   journalctl -u mexicanosPrimeroAPI.service -f

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

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Puedes especificar métodos permitidos
    allow_headers=["*"],  # Puedes especificar headers permitidos
)


@app.get("/", tags=["General"])
def wellcome():
    return {"message": "Bienvanido a la api de Mexicanos Primero"}

@app.post("/token", tags=["Authentication"])
def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return securitySesion.createToken(form_data.username, form_data.password)

@app.post("/escuela/create", tags=["User Management"])
def nuevo_usuario(nombre: str, email: str, numero: int, direccion: str, password: str):
    return securitySesion.createUser(nombre, email, numero, direccion, 2, password)

@app.post("/aliado/create", tags=["User Management"])
def nuevo_usuario(nombre: str, email: str, numero: int, direccion: str, password: str):
    return securitySesion.createUser(nombre, email, numero, direccion, 3, password)

@app.post("/admin/create", tags=["User Management"])
def nuevo_usuario(nombre: str, email: str, numero: int, direccion: str, password: str):
    return securitySesion.createUser(nombre, email, numero, direccion, 1, password)

@app.delete("/user/delete", tags=["User Management"])
def eliminar_usuario(user_data: TokenData = Depends(role_required())):
    return securitySesion.deleteUser(user_data.email)

@app.post("/user/change-password", tags=["User Management"])
def change_password(new_password, user_data: TokenData = Depends(role_required())):
    return securitySesion.changePassword(user_data.email, new_password)

@app.post("/admin/user/create", tags=["Admin"])
def nuevo_usuario(nombre: str, email: str, numero: int, direccion: str, rol: int, password: str, user_data: TokenData = Depends(role_required(["Administrador"]))):
    return securitySesion.createUser(nombre, email, numero, direccion, rol, password)

@app.delete("/admin/user/delete", tags=["Admin"])
def eliminar_usuario(email: str, user_data: TokenData = Depends(role_required(["Administrador"]))):
    return securitySesion.deleteUser(email)

@app.get("/admin/user/change-rol", tags=["Admin"])
def cambiar_rol(email: str, rol: int, user_data: TokenData = Depends(role_required(["Administrador"]))):
    return securitySesion.changeRol(email, rol)


# Obtener informacion reelvante al desarrollo de la aplicacion

@app.get("/user/{email}")
def obtener_informacion_usuario(email: str, user_data: TokenData = Depends(role_required())):
    return dataSourceSesion.getUsuario(email)

@app.get("/user-roles")
def obtener_roles(user_data: TokenData = Depends(role_required())):
    return dataSourceSesion.getRoles()

@app.get("/tipos-necesidades")
def obtener_tipos_necesidades(user_data: TokenData = Depends(role_required())):
    return dataSourceSesion.getTiposNecesidades()


# Endpoints relacionados a escuelas

@app.post("/escuela/crear-necesidad", tags=["Escuela"])
def crear_necesidad(nombre: str, descripcion: str, tipos: TiposNecesidades, user_data: TokenData = Depends(role_required(["Escuela"]))):
    return dataSourceSesion.crearNecesidad(user_data.email, nombre, descripcion, tipos.tipos_necesidad)

@app.get("/escuela/vincular-aliados", tags=["Escuela"])
def relacionar_aliados(necesidad: int, user_data: TokenData = Depends(role_required(["Escuela"]))):
    return dataSourceSesion.relacionarEscuelaAliado(user_data.email, necesidad)

# Endpoints relacionados a aliados

@app.post("/aliado/relacionar-tipos-necesidades", tags=["Aliado"])
def relacionar_tipos_necesidades(tipos: TiposNecesidades, user_data: TokenData = Depends(role_required(["Aliado"]))):
    return dataSourceSesion.relacionarAliadoTipos(user_data.email, tipos.tipos_necesidad)

@app.get("/aliado/vincular-escuelas", tags=["Aliado"])
def relacionar_escuelas(user_data: TokenData = Depends(role_required(["Aliado"]))):
    return dataSourceSesion.relacionarAliadoEscuela(user_data.email)


# Endpoints relacionados a notificaciones

@app.post("/notificacion/crear", tags=["Notificaciones"])
def crear_notificacion(notificacion: Notificacion, user_data: TokenData = Depends(role_required(["Administrador"]))):
    return dataSourceSesion.crearNotificacion(notificacion.email, notificacion.mensaje)

@app.get("/usuario/notificacioes", tags=["Notificaciones"])
def obtener_notificaciones(todos: bool, user_data: TokenData = Depends(role_required())):
    return dataSourceSesion.obtenerNotificaciones(user_data.email, todos)