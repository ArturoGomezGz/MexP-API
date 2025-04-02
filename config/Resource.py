from config.Conexion import Conexion
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import logging

class Resource:
    def __init__(self, jsonBaseDeDatos: dict):
        self.conexion = Conexion(jsonBaseDeDatos)
    
    def obtener_usuario(self, email):
        try:
            resultado = self.conexion.sQueryGET("EXEC mexicanosPrimero.dbo.getUsuario ?", params=(email))
            if not resultado:
                raise HTTPException(status_code=404, detail=f"El usuario con email {email} no existe")
            return resultado[0]
        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error al eliminar cotización: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al eliminar cotización")
