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

@app.get("/")
def wellcome():
    return {"message": "la eylin es gay"}

@app.post("/token")
def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return securitySesion.createToken(form_data.username, form_data.password)

@app.post("/user/create")
def create_user(user: UserCreate):
    return securitySesion.createUser(user.email, user.name, user.password, user.rol)

@app.post("/user/change-password")
def change_password(new_password, user_data: TokenData = Depends(role_required())):
    return securitySesion.changePassword(user_data.email, new_password)

@app.get("/user/{email}")
def get_user_data(email: str, user_data: TokenData = Depends(role_required(["Administrador"]))):
    return dataSourceSesion.obtener_usuario(email)