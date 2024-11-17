import csv
import pg8000
DB_CONFIG_ORIGEN = {
    "database": "gestion_clientes",
    "user": "usuario",
    "password": "admin",
    "host": "esvi",
    "port": 5432
}

DB_CONFIG_DESTINO = {
    "database": "respaldo_financiero",
    "user": "usuario_respaldo",
    "password": "usuario",
    "host": "esvi",
    "port": 5432
}
CSV_FILE = 'reporte_financiero.csv'
def extraer_registros():
    try:
        connection = pg8000.connect(**DB_CONFIG_ORIGEN)
        cursor = connection.cursor()
        query = """
        SELECT fecha, descripcion, monto, tipo_movimiento
        FROM registros_financieros
        WHERE fecha >= CURRENT_DATE - INTERVAL '30 days';
        """
        cursor.execute(query)
        registros = cursor.fetchall()

        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['fecha', 'descripcion', 'monto', 'tipo_movimiento'])
            writer.writerows(registros)

        print(f"Archivo '{CSV_FILE}' generado exitosamente con {len(registros)} registros.")

    except Exception as e:
        print(f"Error durante la extracción: {e}")
    finally:
        if connection:
            connection.close()
def insertar_registros():
    connection = None  
    try:
        connection = pg8000.connect(**DB_CONFIG_DESTINO)
        cursor = connection.cursor()

        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                    INSERT INTO respaldo_financiero (fecha, descripcion, monto, tipo_movimiento, origen)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    row['fecha'],
                    row['descripcion'],
                    row['monto'],
                    row['tipo_movimiento'],
                    "Sistema Contable"
                ))

        connection.commit()
        print("Los datos se han importado correctamente en la base de datos destino.")

    except Exception as e:
        print(f"Error durante la inserción: {e}")
    finally:
        if connection:
            connection.close()
extraer_registros()
insertar_registros()
