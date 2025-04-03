from datetime import datetime, timedelta
from jose import JWTError, jwt
from config.Conexion import Conexion
# from passlib.context import CryptContext #  bcrypt no usado
from argon2 import PasswordHasher # Alternativa a bcrypt
from config.models.Token import Token, TokenData
from fastapi import HTTPException
import logging

class Security:
    def __init__(self, jsonBaseDeDatos: dict, secretKey: str, algorithm: str, tokenExpirationDays: int):
        self.conexion = Conexion(jsonBaseDeDatos)
        self.secretKey = secretKey
        self.algorithm = algorithm
        self.pwdContext = PasswordHasher() # Alternativa a bcrypt
        self.tokenExpirationDays = tokenExpirationDays

    def verifyPwd(self, plainPassword: str, hashedPassword: str):
        try:
            # Usamos el método verify de Argon2
            return self.pwdContext.verify(hashedPassword, plainPassword)
        except Exception:
            return False

    def hashPwd(self, password: str):
        # Usamos el método hash de Argon2
        return self.pwdContext.hash(password)

    def login(self, email: str, password: str):
        try:
            USUARIO = self.conexion.sQueryGET("SELECT * FROM public.obtener_contrasena(?)", (email))
            if USUARIO and self.verifyPwd(password, USUARIO[0]["obtener_contrasena"]):
                return True
            else:
                return False
        except Exception as e:
            return None

    def changePassword(self, email: str, newPassword: str):
        try:
            # Verificar que el usuario exista
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (email,))
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            # Cambiar la contraseña
            self.conexion.sQuery("SELECT * FROM cambiar_contrasena(?,?)", (email, self.hashPwd(newPassword)))
            return {"message": f"Contraseña de {email} cambiada exitosamente"}

        except HTTPException as e:
            raise e
            
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def createUser(self, nombre: str, email: str, direccion: str, rol: int, password: str):
        try:
            # Verificar que el usuario no exista
            if self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (email)):
                raise HTTPException(status_code=400, detail="Usuario ya existe")
            
            # Crear el usuario
            self.conexion.sQuery("SELECT insertar_usuario(?, ?, ?, ?, ?);", (nombre, email, direccion, rol, self.hashPwd(password)))
            return {"message": f"Usuario {email} creado exitosamente"}
        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def deleteUser(self, email: str):
        try:
            user = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (email))
            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            self.conexion.sQuery("SELECT * FROM eliminar_usuario(?)", (email))
            return {"message": f"Usuario {email} eliminado exitosamente"}

        except HTTPException as e:
            raise e

        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def createToken(self, email: str, contrasena: str) -> Token:
        try:
            if self.login(email, contrasena):
                usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (email))[0]
                rol = usuario["tipo_usuario"]
                correo = usuario["correo"]
                print(correo)
                to_encode = {"email": correo, "rol": rol}
                expire = datetime.utcnow() + timedelta(days=self.tokenExpirationDays)
                to_encode.update({"exp": expire})
                encoded_jwt = jwt.encode(to_encode, self.secretKey, algorithm=self.algorithm)
                return Token(access_token=encoded_jwt, token_type="bearer")
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")
        except HTTPException as e:
            raise e
        except Exception:
            raise HTTPException(status_code=500, detail="Error interno")
    
    def verifyToken(self, token: str):
        try:
            payload = jwt.decode(token, self.secretKey, algorithms=[self.algorithm])
            correo: str = payload.get("email")
            rol: str = payload.get("rol")
            if correo is None or rol is None:
                raise HTTPException(status_code=403, detail="Token missing required fields")
            token_data = TokenData(email=correo, rol=rol)
        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
        return token_data
    
    def getRole(self, token: str):
        try:
            return self.verifyToken(token).rol
        except HTTPException as e:
            raise e

    def getUsusrio(self, mail):
        try:
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (mail))
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return usuario[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error interno")

    def changeRol(self, email: str, rol: int):
        try:
            # Verificar que el usuario exista
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (email))
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            # Cambiar el rol
            self.conexion.sQuery("SELECT * FROM cambiar_rol(?, ?)", (email, rol))
            return {"message": f"Rol de {email} cambiado exitosamente"}

        except HTTPException as e:
            raise e
            
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")