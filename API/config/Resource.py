from config.Conexion import Conexion
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from config.models.responses.Producto import Producto, ProductoExtendido, ProductoPrecioExist, Inventario
from config.models.responses.Oferta import Oferta
from config.models.responses.Respuesta import Respuesta
import logging

class Resource:
    def __init__(self, jsonBaseDeDatos: dict):
        self.conexion = Conexion(jsonBaseDeDatos)

    def get_producto_resumido(self, codigoProducto):
        try:
            resultado_producto = self.conexion.sQueryGET("EXEC MrApi.dbo.getProducto ?", params=(codigoProducto,))
            if not resultado_producto:
                raise HTTPException(status_code=404, detail=f"Producto con codigo {codigoProducto} no encontrado en Producto Resumido.")

            res = resultado_producto[0]
            resultado_codigos = self.conexion.sQueryGET("EXEC MrApi.dbo.getCodigosProducto ?", params=(codigoProducto,))
            res["codigos"] = resultado_codigos 
            return Producto.model_validate(res)

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error al obtener producto resumido con código {codigoProducto}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error al obtener producto resumido con código {codigoProducto}")

    def get_producto_extendido(self, codigoProducto):
        try:
            resultado_producto = self.conexion.sQueryGET("EXEC MrApi.dbo.getProductoExtendido ?", params=(codigoProducto,))
            if not resultado_producto:
                raise HTTPException(status_code=404, detail=f"Producto con código {codigoProducto} no encontrado en Producto Extendido.")

            res = resultado_producto[0]
            idProducto = res["id"]
            resultado_codigos = self.conexion.sQueryGET("EXEC MrApi.dbo.getCodigosProducto ?", params=(codigoProducto,))
            resultado_sales = self.conexion.sQueryGET("EXEC MrApi.dbo.getSalesProducto ?", params=(idProducto,))
            resultado_usos = self.conexion.sQueryGET("EXEC MrApi.dbo.getUsosProducto ?", params=(idProducto,))

            res["codigos"] = resultado_codigos 
            res["usos"] = [uso["Uso"] for uso in resultado_usos]
            res["sales"] = resultado_sales

            return ProductoExtendido.model_validate(res)

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error al obtener producto extendido con código {codigoProducto}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error al obtener producto extendido con código {codigoProducto}")

    def get_precio_existencia(self, codigoProducto):
        try:
            resultado_inventario = self.conexion.sQueryGET("EXEC MrApi.dbo.getPrecioExistencia ?", params=(codigoProducto,))
            if not resultado_inventario:
                raise HTTPException(status_code=404, detail=f"El codigo {codigoProducto} no es valido, intenta revisar el corigo de barras y volver a intetnar")

            res = resultado_inventario[0]
            return ProductoPrecioExist.model_validate(res)

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error al obtener inventario para el producto con código {codigoProducto}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al obtener inventario para el producto con código {codigoProducto}")

    def get_imagen(self, codigoProducto):
        try:
            resultado_imagen = self.conexion.sQueryGET("EXEC MrApi.dbo.getFoto ?", params=(codigoProducto,))
            if not resultado_imagen:
                raise HTTPException(status_code=404, detail=f"El codigo {codigoProducto} no es valido, intenta revisar el corigo de barras y volver a intetnar")

            res = resultado_imagen[0]
            return res["Foto"]

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error al obtener imagen para el producto con código {codigoProducto}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error al obtener imagen para el producto con código {codigoProducto}")

    def get_inventario(self):
        try:
            resultado_inventario = self.conexion.sQueryGET("EXEC MrApi.dbo.getInventario")
            if not resultado_inventario:
                raise HTTPException(status_code=404, detail="No se encontró inventario")

            res = resultado_inventario
            return [Inventario.model_validate(inventario) for inventario in res]

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error al obtener inventario: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al obtener inventario")

    def get_nueva_cotizacion(self, correoUsuario):
        try:
            resultado_cotizacion = self.conexion.sQueryGET("EXEC MrApi.dbo.getNuevaCotizacion ?", params=(correoUsuario,))
            if not resultado_cotizacion:
                raise HTTPException(status_code=404, detail="Error al crear cotización")
            elif resultado_cotizacion[0] == 0:
                raise HTTPException(status_code=404, detail="Cliente invalido")

            res = resultado_cotizacion[0]
            return res

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error al obtener cotización: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al obtener cotización")
    
    def get_ofertas_cotizacion(self, correoUsuario, idProducto):
        try:
            resultado_ofertas = self.conexion.sQueryGET("EXEC MrApi.dbo.getCotizarOfertas ?, ?", params=(correoUsuario, idProducto))
            if not resultado_ofertas:
                raise HTTPException(status_code=404, detail=f"No se encontro el producto con id {idProducto}")

            res = resultado_ofertas[0]
            return Oferta.model_validate(res)

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error al obtener ofertas: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al obtener ofertas")
        
    def add_producto_cotizacion(self, correoUsuario, idCotizacion, idProducto, cantidad):
        try:
            resultado = self.conexion.sQueryGET("EXEC MrApi.dbo.insertProductoCotizacion ?, ?, ?, ?", params=(correoUsuario, idCotizacion, idProducto, cantidad))
            if not resultado:
                raise HTTPException(status_code=404, detail=f"Error al ejecutar la inserción del producto en la cotización")
            
            res = resultado[0]
            return Respuesta.model_validate(res)

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error al agregar producto a la cotización: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al agregar producto a la cotización")
    
    def delete_producto_cotizacion(self, correUsuario, idCotizacion ,idProducto):
        try:
            resultado = self.conexion.sQueryGET("EXEC MrApi.dbo.deleteProductoCotizacion ?, ?, ?", params=(correUsuario, idCotizacion, idProducto))
            if not resultado:
                raise HTTPException(status_code=404, detail=f"Error al ejecutar la eliminación del producto en la cotización")
            
            res = resultado[0]
            return Respuesta.model_validate(res)

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error al eliminar producto de la cotización: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al eliminar producto de la cotización")

    def colocar_cotizacion(self, correoUsuario, idCotizacion, obsevaciones: str = None):
        try:
            resultado = self.conexion.sQueryGET("EXEC MrApi.dbo.insertCotizacion ?, ?, ?", params=(correoUsuario, idCotizacion, obsevaciones))
            if not resultado:
                raise HTTPException(status_code=404, detail=f"Error al ejecutar la colocación de la cotización")
            
            res = resultado[0]
            return res
        
        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error al colocar cotización: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al colocar cotización")
    
    def eliminar_cotizacion(self, correoUsuario, idCotizacion):
        try:
            resultado = self.conexion.sQueryGET("EXEC MrApi.dbo.deleteCotizacion ?, ?", params=(correoUsuario, idCotizacion))
            if not resultado:
                raise HTTPException(status_code=404, detail=f"Error al ejecutar la eliminación de la cotización")
            
            res = resultado[0]
            return Respuesta.model_validate(res)
        
        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error al eliminar cotización: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al eliminar cotización")