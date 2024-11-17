import csv
import pg8000 

DB_CONFIG = {
    "database": "gestion_clientes",  
    "user": "usuario",              
    "password": "admin",        
    "host": "esvi",            
    "port": 5432                     
}
OUTPUT_FILE = "nuevos_clientes.csv"
try:
    connection = pg8000.connect(**DB_CONFIG)
    cursor = connection.cursor()
    query = """
    SELECT id, nombre, telefono, email
    FROM clientes
    WHERE fecha_creacion >= CURRENT_DATE;
    """
    cursor.execute(query)
    clientes = cursor.fetchall()

    with open(OUTPUT_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nombre', 'Teléfono', 'Email'])  
        writer.writerows(clientes)

    print(f"Archivo '{OUTPUT_FILE}' generado exitosamente con {len(clientes)} clientes.")
    
except Exception as e:
    print(f"Error: {e}")
finally:
   
    if connection:
        connection.close()
