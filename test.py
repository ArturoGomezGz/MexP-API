import pyodbc

def connect_and_query():
    try:
        # Conexión a la base de datos PostgreSQL usando pyodbc
        connection = pyodbc.connect(
            "DRIVER={PostgreSQL Unicode};"
            "SERVER=localhost;"
            "PORT=5432;"
            "DATABASE=MexicanosPrimero;"
            "UID=postgres;"
            "PWD=Pword76;"
        )
        cursor = connection.cursor()
        
        # Ejecutar un query
        query = "SELECT * FROM testFunct();"
        cursor.execute(query)
        
        # Obtener resultados
        results = cursor.fetchall()
        for row in results:
            print(row)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    connect_and_query()
