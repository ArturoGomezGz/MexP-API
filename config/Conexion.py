import pyodbc

class Conexion:
    def __init__(self, jsonBaseDeDatos: dict):
        try:
            self.conexion = None
            self.dbServer = jsonBaseDeDatos["server"]
            self.dbDatabase = jsonBaseDeDatos["database"]
            self.dbUsuario = jsonBaseDeDatos["usuario"]
            self.dbContrasena = jsonBaseDeDatos["contrasena"]
            self.dbPort = jsonBaseDeDatos["port"]

            self.conexion = pyodbc.connect(
                f"DRIVER={{PostgreSQL Unicode}};"
                f"SERVER={self.dbServer};"
                f"DATABASE={self.dbDatabase};"
                f"UID={self.dbUsuario};"
                f"PWD={self.dbContrasena}"
            )

        except Exception as e:
            if self.conexion:
                self.conexion.close()
            raise ConnectionError(f"Error inicializando la conexión: {e}")

    
    def cerrarConexion(self):
        """Cierra la conexión y el cursor."""
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada exitosamente.")

    def query_results_to_json(self, resultados, columnas):
        try:
            # Convierte cada fila en un diccionario usando las columnas proporcionadas
            rows = [{col: str(value) for col, value in zip(columnas, row)} for row in resultados]
            return rows  # Ya está en formato JSON-compatible
        except Exception as e:
            # Opcional: Manejo de errores para depuración
            raise ValueError(f"Error al convertir resultados a JSON: {e}")

    def sQuery(self, query, params = None):
        with self.conexion.cursor() as cursor:
            cursor.execute(query, params)
            self.conexion.commit()

    def sQueryGET(self, query, params=None):
        with self.conexion.cursor() as cursor:
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            
            resultados = cursor.fetchall()
            columnas = [column[0] for column in cursor.description]
            
            return self.query_results_to_json(resultados, columnas)


    def select(self, tabla):
        return self.sQueryGET(f"SELECT * FROM ?;", params=(tabla))
    
    def selectTop(self, n, tabla):
        return self.sQueryGET(f"SELECT TOP ? * FROM ?;", params=(n, tabla))
    