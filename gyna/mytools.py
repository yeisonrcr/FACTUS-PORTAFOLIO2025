import sqlite3

def copiar_datos():
    # Establece conexiones a las bases de datos
    conn_origen = sqlite3.connect('copiarDatos.sqlite3')
    conn_destino = sqlite3.connect('db.sqlite3')

    # Crea cursores
    cursor_origen = conn_origen.cursor()
    cursor_destino = conn_destino.cursor()

    # Recupera los datos de la tabla de origen
    cursor_origen.execute('SELECT vehicle_no, vehicle_name,vehicle_model, vehicle_brand, vehicle_cliente, vehicle_mobile, distribuidorax, costAbonado,costTotal,problem_description,date,status,estado,dinomoDis FROM vehicle_request')
    
    datos = cursor_origen.fetchall()

    # Crea la misma tabla en la base de datos de destino (si no existe)
    # ...

    # Inserta los datos en la nueva tabla
    for fila in datos:
        cursor_destino.execute('INSERT INTO vehicle_request (vehicle_no, vehicle_name,vehicle_model, vehicle_brand, vehicle_cliente, vehicle_mobile, distribuidorax, costAbonado,costTotal, problem_description,date,status,estado,dinomoDis) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', fila)

    # Guarda los cambios
    conn_destino.commit()

    # Cierra las conexiones
    conn_origen.close()
    conn_destino.close()

# Llama a la función para copiar los datos
copiar_datos()
