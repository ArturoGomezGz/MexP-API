from datetime import datetime, timedelta
from jose import JWTError, jwt
from config.Conexion import Conexion
# from passlib.context import CryptContext #  bcrypt no usado
from argon2 import PasswordHasher # Alternativa a bcrypt
from config.models.Token import Token, TokenData
from fastapi import HTTPException

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
            USUARIO = self.conexion.sQueryGET("EXEC mexicanosPrimero.dbo.getUserCredentials ?", (email,))
            if USUARIO and self.verifyPwd(password, USUARIO[0]["contrasena"]):
                return True
            else:
                return False
        except Exception as e:
            return None

    def changePassword(self, email: str, newPassword: str):
        try:
            self.conexion.sQuery("EXEC mexicanosPrimero.dbo.changePassword ?, ?", (email, self.hashPwd(newPassword)))
        except Exception as e:
            return False
        return True

    def createUser(self, email: str, name: str, password: str, rol: str):
        try:
            # Verificar que el usuario no exista
            if self.conexion.sQueryGET("SELECT * FROM usuarios WHERE correo = ? ", (email,)):
                raise HTTPException(status_code=400, detail="Usuario ya existe")
            
            # Crear el usuario
            self.conexion.sQuery("EXEC mexicanosPrimero.dbo.insertUsuario ?,?,?,?", (email, name, self.hashPwd(password), rol))
        except Exception:
            raise HTTPException(status_code=500, detail="Error interno")
        return {"message": f"Usuario {email} creado exitosamente"}

    """ def deleteUser(self, user: str):
        try:
            self.conexion.sQueryGET("SELECT * FROM MrApi.dbo.Usuarios WHERE username = ?", (user,))
            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            self.conexion.sQuery("DELETE FROM MrApi.dbo.Usuarios WHERE username = ?", (user,))
            return {"message": f"Usuario {user} eliminado exitosamente"}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error interno") """

    def createToken(self, email: str, contrasena: str) -> Token:
        try:
            if self.login(email, contrasena):
                usuario = self.conexion.sQueryGET("EXEC mexicanosPrimero.dbo.getUsuario ?", (email))[0]
                rol = usuario["tipoUsuario"]
                correo = usuario["email"]
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
            token_data = TokenData(correo=correo, rol=rol)
        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
        return token_data
    
    def getRole(self, token: str):
        try:
            return self.verifyToken(token).rol
        except HTTPException as e:
            raise e
        
    def roleRequired(self, token: str, requiredRoles: list[str]):
        try:
            userRole = self.getRole(token)
            if userRole not in requiredRoles:
                raise HTTPException(status_code=403, detail="Unauthorized")
        except HTTPException as e:
            raise e

    def getUsusrio(self, mail):
        try:
            usuario = self.conexion.sQueryGET("SELECT obtener_usuario(?)", (mail,))
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return usuario[0]
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error interno")