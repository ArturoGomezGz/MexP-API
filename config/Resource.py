from config.Conexion import Conexion
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import logging

class Resource:
    def __init__(self, jsonBaseDeDatos: dict):
        self.conexion = Conexion(jsonBaseDeDatos)

    def getUsuario(self, mail):
        try:
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (mail))
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return usuario[0]
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error interno")


    def getRoles(self):
        try:
            roles = self.conexion.sQueryGET("SELECT * FROM tipo_usuarios")
            if not roles:
                raise HTTPException(status_code=404, detail="No se encontraron roles")
            return roles
        except HTTPException as e:
            raise e
        
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")
    
    def getTiposNecesidades(self):
        try:
            tipos = self.conexion.sQueryGET("SELECT * FROM obtener_todos_tipos_necesidades()")
            if not tipos:
                raise HTTPException(status_code=404, detail="No se encontraron tipos de necesidad")
            return tipos
        except HTTPException as e:
            raise e
        
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")


    def crearNecesidad(self, correo, nombre, descripcion, tipos):
        try:
            # Verifica si el usuario existe
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (correo))
            if not usuario:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            
            # Verifica si el usuario tiene el rol de escuela
            rol = self.conexion.sQueryGET("SELECT obtener_tipo_usuario_por_correo(?)", (correo))[0]['obtener_tipo_usuario_por_correo']
            if not rol or rol != '2':
                raise HTTPException(status_code=403, detail="El usuario no tiene permisos para crear necesidades")

            # Crea la necesidad
            necesidad = self.conexion.sQueryGET("SELECT public.crear_necesidad(?,?,?)", (correo, nombre, descripcion))
            if not necesidad:
                raise HTTPException(status_code=404, detail="No se pudo crear la necesidad")
            
            id_necesidad = necesidad[0]['crear_necesidad']

            # Relaciona la necesidad con los tipos
            for tipo in tipos:
                relacion = self.relacionarNecesidadTipo(id_necesidad, tipo)
                if not relacion:
                    raise HTTPException(status_code=404, detail="No se pudo relacionar la necesidad con el tipo")
                
            return {"Necesidad creada y relacionada con exito" }
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def relacionarNecesidadTipo(self, id_necesidad, id_tipo):
        try:
            # Verifica si la necesidad existe
            necesidad = self.conexion.sQueryGET("SELECT * FROM obtener_necesidad(?)", (id_necesidad))
            if not necesidad:
                raise HTTPException(status_code=404, detail="Necesidad no encontrada")
            
            # Verifica si el tipo existe
            tipo = self.conexion.sQueryGET("SELECT * FROM obtener_tipo_necesidad(?)", (id_tipo))
            if not tipo:
                raise HTTPException(status_code=404, detail="Tipo no encontrado")

            # Relaciona la necesidad con el tipo
            relacion = self.conexion.sQueryGET("SELECT public.relacionar_necesidad_tipo(?,?)", (id_necesidad, id_tipo))
            if not relacion:
                raise HTTPException(status_code=404, detail="No se pudo relacionar la necesidad con el tipo")
            
            return True
    
        except (HTTPException, Exception) as e:
            raise e
        
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")
        
    def relacionarAliadoTipos(self, correo_aliado, tipos):
        try:
            # Verifica si el aliado existe
            aliado = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (correo_aliado,))
            if not aliado:
                raise HTTPException(status_code=404, detail="Aliado no encontrado")
            
            for tipo_id in tipos:
                # Verifica si el tipo existe
                tipo_data = self.conexion.sQueryGET("SELECT * FROM obtener_tipo_necesidad(?)", (tipo_id,))
                if not tipo_data:
                    raise HTTPException(status_code=404, detail="Tipo no encontrado")
                
                # Relaciona el aliado con el tipo
                relacion = self.conexion.sQueryGET("SELECT * FROM relacionar_aliado_tipo(?,?)", (correo_aliado, tipo_id))
                if not relacion:
                    raise HTTPException(status_code=404, detail="No se pudo relacionar el aliado con el tipo")
                
            return {"Aliado relacionado con los tipos de necesidad con exito"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")


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
