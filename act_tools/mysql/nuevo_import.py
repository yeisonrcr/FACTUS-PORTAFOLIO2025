import mysql.connector
from mysql.connector import connect, Error
import json
import uuid #generador de id unicos


# Conecta a la base de datos



# Cargar el JSON
with open('datos.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Conectar a la base de datos
try:
    connection = connect(
    host='localhost',
    user='ecomycr',
    password='zbyj8918',
    database='ecomycr')
    


    cursor = connection.cursor()

    # Iterar sobre provincias
    for provincia_codigo, provincia_info in data['provincias'].items():
        print(f"Procesando Provincia: {provincia_info['nombre']} (ID: {provincia_codigo})")
        try:
            # Iniciar una nueva transacción para la provincia
            connection.start_transaction()

            # Insertar provincia
            cursor.execute(
                "INSERT IGNORE INTO tiendas_provincia (id, nombre) VALUES (%s, %s)", 
                (provincia_codigo, provincia_info['nombre'])
            )

            cantones_contados = len(provincia_info['cantones'])
            print(f"  Cantones a insertar: {cantones_contados}")

            # Iterar sobre cantones de cada provincia
            for canton_codigo, canton_info in provincia_info['cantones'].items():
                canton_id = str(uuid.uuid4())  # Crear un ID único para el cantón
                print(f"  Insertando Cantón: {canton_info['nombre']} (ID: {canton_id})")
                # Insertar cantón
                cursor.execute(
                    "INSERT IGNORE INTO tiendas_canton (id, nombre, provincia_id) VALUES (%s, %s, %s)", 
                    (canton_id, canton_info['nombre'], provincia_codigo)
                )

                distritos_contados = len(canton_info['distritos'])
                #print(f"    Distritos a insertar para el cantón {canton_info['nombre']}: {distritos_contados}")

                # Iterar sobre distritos de cada cantón
                for distrito_codigo, distrito_nombre in canton_info['distritos'].items():
                    distrito_id = str(uuid.uuid4())  # Crear un ID único para el distrito
                    #print(f"    Insertando Distrito: {distrito_nombre} (ID: {distrito_id})")
                    # Insertar distrito
                    cursor.execute(
                        "INSERT IGNORE INTO tiendas_distrito (id, nombre, canton_id) VALUES (%s, %s, %s)", 
                        (distrito_id, distrito_nombre, canton_id)
                    )

                # Confirmar la transacción para el cantón
                connection.commit()
                #print(f"Cantón {canton_info['nombre']} importado correctamente.\n")

            # Confirmar la transacción para la provincia
            connection.commit()
            #print(f"Provincia {provincia_info['nombre']} importada correctamente.\n")

        except Error as err:
            # Revertir la transacción para esta provincia
            connection.rollback()
            print(f"Error al importar la provincia {provincia_info['nombre']} (ID: {provincia_codigo}): {err}\n")

    # Cerrar conexión después de procesar todas las provincias
    if connection.is_connected():
        cursor.close()
        connection.close()

    #print("Importación completada exitosamente!")

except Error as e:
    print(f"Error de conexión a la base de datos: {e}")
