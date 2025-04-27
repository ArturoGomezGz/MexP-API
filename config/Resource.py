from config.Conexion import Conexion
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import logging
import math

class Resource:
    def __init__(self, jsonBaseDeDatos: dict):
        self.conexion = Conexion(jsonBaseDeDatos)


    # Ecuacion para calcular la distancia entre dos puntos
    def distancia_euclidiana(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def getListaUsuarios(self):
        try:
            usuarios = self.conexion.sQueryGET("SELECT * FROM obtener_usuarios()")
            if not usuarios:
                raise HTTPException(status_code=404, detail="No se encontraron usuarios")
            return usuarios
        except HTTPException as e:
            raise e

        except Exception as e:
            raise HTTPException(status_code=500, detail="Error interno")

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
        
    def getUsuarioPorID(self, id):
        try:
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario_por_id(?)", (id))
            if not usuario:
                raise HTTPException(status_code=404, detail="No se encontraron usuarios")
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

    def relacionarEscuelaAliado(self, correo, necesidad):
        try:
            if necesidad != 0:
                # Verifica si la necesidad existe
                necesidad_data = self.conexion.sQueryGET("SELECT * FROM obtener_necesidad(?)", (necesidad,))
                if not necesidad_data:
                    raise HTTPException(status_code=404, detail="Necesidad no encontrada")
            
            # Relaciona la necesidad con el aliado
            relaciones = self.conexion.sQueryGET("SELECT * FROM obtener_r_escuela_aliado(?,?);", (correo, necesidad))
            print(correo, necesidad)
            if not relaciones:
                raise HTTPException(status_code=404, detail="No existen relaciones entre la escuela y algun aliado")

            return relaciones 
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def relacionarAliadoEscuela(self, correo):
        try:
            # Relaciona el aliado con la escuela
            relaciones = self.conexion.sQueryGET("SELECT * FROM obtener_r_aliado_escuela(?);", (correo))
            if not relaciones:
                raise HTTPException(status_code=404, detail="No existen relaciones entre el aliado y alguna escuela")
            
            return relaciones 
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def enlazarNecesidadAliado(self, correoEscuela, id_necesidad, correoAliado):
        try:
            # Verifica si el usuario existe
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (correoEscuela,))
            if not usuario:
                raise HTTPException(status_code=404, detail="El usuario no existe")

            # Verifica si la necesidad existe   
            necesidad = self.conexion.sQueryGET("SELECT * FROM obtener_necesidad(?)", (id_necesidad,))
            if not necesidad:
                raise HTTPException(status_code=404, detail="Necesidad no encontrada")

            # Verifica si el aliado existe
            aliado = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (correoAliado,))
            if not aliado:
                raise HTTPException(status_code=404, detail="Aliado no encontrado")   

            # Verifica que el vinculo entre la necesidad es posible 
            relacion = self.conexion.sQueryGET("SELECT * FROM obtener_r_aliado_necesidad(?,?)", (correoAliado, id_necesidad))
            if not relacion:
                raise HTTPException(status_code=404, detail="No existe una relacion entre el aliado y la necesidad")

            # Relaciona la necesidad con el aliado
            relacion = self.conexion.sQueryGET("SELECT * FROM vincular_necesidad_aliado(?,?,?)", (correoEscuela, id_necesidad, correoAliado))
            if not relacion:
                raise HTTPException(status_code=404, detail="No se pudo relacionar la necesidad con el aliado")

            # Crear notificacion al aliado
            self.crearNotificacion(correoAliado, f"Se ha vinculado la necesidad {id_necesidad} con el aliado {correoEscuela}")

            # Crear notificacion a la escuela
            self.crearNotificacion(correoEscuela, f"Se ha vinculado la necesidad {id_necesidad} con el aliado {correoAliado}")
            
            return {"Necesidad relacionada con el aliado con exito"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def obtenerNotificaciones(self, email, todos=False):
        try:
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (email,))
            if not usuario:
                raise HTTPException(status_code=404, detail="El usuario no existe")


            notificaciones = self.conexion.sQueryGET("SELECT * FROM obtener_notificaciones(?, ?)", (email,todos))

            if not notificaciones:
                raise HTTPException(status_code=404, detail="No se encontraron notificaciones")

            return notificaciones


        except HTTPException as e:
            raise e

        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def crearNotificacion(self, email, mensaje):
        try:
            # Verifica si el usuario existe
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (email,))
            if not usuario:
                raise HTTPException(status_code=404, detail="El usuario no existe")

            # Crea la notificacion
            notificacion = self.conexion.sQueryGET("SELECT * FROM insertar_notificacion(?, ?)", (email, mensaje))
            if not notificacion:
                raise HTTPException(status_code=404, detail="No se pudo crear la notificación")
            
            return {"Notificación creada con éxito"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def cambiarEstadoNotificacion(self, email, id_notificacion, nuevo_estado):
        try:
            # Verifica si el usuario existe
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (email,))
            if not usuario:
                raise HTTPException(status_code=404, detail="El usuario no existe")

            # Cambia el estado de la notificacion
            notificacion = self.conexion.sQueryGET("SELECT * FROM actualizar_estado_notificacion(?, ?, ?)", (email, id_notificacion, nuevo_estado))
            if not notificacion or notificacion[0]['actualizar_estado_notificacion'] == 'false':
                raise HTTPException(status_code=404, detail="No se pudo cambiar el estado de la notificación")
            
            return {"Estado de la notificación cambiado con éxito"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def vincularAliadoNecesidad(self, email, idNecesidad):
        try:
            # Verifica si el usuario existe
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (email,))
            if not usuario:
                raise HTTPException(status_code=404, detail="El usuario no existe")

            # Cambia el estado de la notificacion
            vinculacion = self.conexion.sQueryGET("SELECT * FROM insertar_r_aliado_necesidad(?, ?)",
                                                   (email, idNecesidad))
            if not vinculacion:
                raise HTTPException(status_code=404, detail="No se pudo vincular la necesidad con el aliado")

            return {"La vinculacion se ha realizado con exito"}

        except HTTPException as e:
            raise e

        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def obtenerNecesidades(self, id_escuela):
        try:

            # Obtiene las necesidades del usuario
            necesidades = self.conexion.sQueryGET("SELECT * FROM obtener_necesidades(?)", (id_escuela,))
            if not necesidades:
                raise HTTPException(status_code=404, detail="No se encontraron necesidades")

            return necesidades

        except HTTPException as e:
            raise e

        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def obtenerDireccion(self, id_usuario):
        try:
            # Obtiene la direccion del usuario
            direccion = self.conexion.sQueryGET("SELECT * FROM obtener_direccion(?)", (id_usuario,))
            if not direccion:
                raise HTTPException(status_code=404, detail="No se encontro la direccion")

            return direccion[0]

        except HTTPException as e:
            raise e

        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")
    
    def setDireccion(self, id_usuario, latitud, longitud):
        try:

            # Crea la direccion
            direccion = self.conexion.sQueryGET("SELECT * FROM set_latitud_longitud(?, ?, ?)", (id_usuario, latitud, longitud))
            if not direccion:
                raise HTTPException(status_code=404, detail="No se pudo crear la direccion")
            
            return {"Coordenadas guardadas con exito"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def setDescripcionUsuario(self, correo, descripcion):
        try:
            # Verifica si el usuario existe
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (correo,))
            if not usuario:
                raise HTTPException(status_code=404, detail="El usuario no existe")

            # Cambia la descripcion del usuario
            descripcion = self.conexion.sQueryGET("SELECT * FROM set_descripcion_usuario(?, ?)", (correo, descripcion))
            if not descripcion:
                raise HTTPException(status_code=404, detail="No se pudo cambiar la descripcion del usuario")
            
            return {"Descripcion cambiada con exito"}
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")

    def obtenerNecesidadesEnlazadasEscuela(self, correo):
        try:
            # Verifica si el usuario existe
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (correo,))
            if not usuario:
                raise HTTPException(status_code=404, detail="El usuario no existe")

            # Obtiene las necesidades enlazadas
            necesidades = self.conexion.sQueryGET("SELECT * FROM obtener_necesidades_enlazadas_escuela(?)", (correo,))
            if not necesidades:
                raise HTTPException(status_code=404, detail="No se encontraron necesidades enlazadas")

            return necesidades

        except HTTPException as e:
            raise e

        except Exception as e:
            logging.error(f"Error al ejecutar la función: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al ejecutar la función")
        
    def obtenerNecesidadesEnlazadasAliado(self, correo):
        try:
            # Verifica si el usuario existe
            usuario = self.conexion.sQueryGET("SELECT * FROM obtener_usuario(?)", (correo,))
            if not usuario:
                raise HTTPException(status_code=404, detail="El usuario no existe")

            # Obtiene las necesidades enlazadas
            necesidades = self.conexion.sQueryGET("SELECT * FROM obtener_necesidades_enlazadas_aliado(?)", (correo,))
            if not necesidades:
                raise HTTPException(status_code=404, detail="No se encontraron necesidades enlazadas")

            return necesidades

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
