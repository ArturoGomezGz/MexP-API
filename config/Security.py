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
            if self.conexion.sQueryGET("EXEC ", (email,)):
                raise HTTPException(status_code=400, detail="Usuario ya existe")
            
            # VEriificar que el correo no exista
            if self.conexion.sQueryGET("EXEC mexicanosPrimero.dbo.getUsuario ?", (email,)):
                raise HTTPException(status_code=400, detail="Correo ya registrado")
            
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

    """ def changeRole(self, user: str, newRole: str):
        try:
            # Validación de roles permitidos
            roles = self.getRoles()
            valid_roles = [r["nombre_rol"] for r in roles]

            # Obtener el id del nuevo rol
            id_rol = self.conexion.sQueryGET("SELECT id_rol FROM MrApi.dbo.Roles WHERE nombre_rol = ?", (newRole,))[0]["id_rol"]

            if newRole not in valid_roles:
                raise HTTPException(status_code=400, detail="Rol no válido")

            # Consultar si el usuario existe
            usuario = self.conexion.sQueryGET("SELECT * FROM MrApi.dbo.Usuarios WHERE username = ?", (user,))
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            # Actualizar el rol del usuario
            result = self.conexion.sQuery("UPDATE MrApi.dbo.Usuarios SET rol = ? WHERE username = ?", (id_rol, user))
            
            # Verificar que el cambio fue exitoso (al menos una fila debe ser afectada)
            if result == 0:
                raise HTTPException(status_code=400, detail="No se pudo actualizar el rol")

            return {"message": f"Rol de {user} cambiado a {newRole} exitosamente"}

        except HTTPException as e:
            # Re-lanzamos excepciones HTTP con el mensaje adecuado
            raise e
        except Exception:
            # En caso de un error inesperado, lanzamos una excepción genérica
            raise HTTPException(status_code=500, detail="Error interno") 

        try:
            return self.conexion.sQueryGET("SELECT nombre_rol FROM MrApi.dbo.Roles WHERE id_rol = ?", (id_rol,))[0]["nombre_rol"]
        except Exception:
            raise HTTPException(status_code=500, detail="Error interno")"""
