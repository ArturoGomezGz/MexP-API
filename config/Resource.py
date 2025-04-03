from config.Conexion import Conexion
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import logging

class Resource:
    def __init__(self, jsonBaseDeDatos: dict):
        self.conexion = Conexion(jsonBaseDeDatos)

    # Boseto de creacion de funciones 
    """
    def nombre_funcion(self, params):
        # Todo dentro de un try except para menejar errores generales
        try:

            # Ejecutar la función almacenada en la base de datos
            resultado = self.conexion.sQueryGET("EXEC mexicanosPrimero.dbo.nombre_funcion ?", params=(params))
            if not resultado:
                raise HTTPException(status_code=404, detail="No se encontraron resultados")
            return JSONResponse(content=resultado)

            # Despues de un raise el error cae a la excepcion
        except HTTPException as e:
            raise e

            # Si no es un error de la API, se maneja el error
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")
    
    """
    