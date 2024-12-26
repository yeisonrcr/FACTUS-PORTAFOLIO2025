import mysql.connector
import sqlite3

#realizar migraciones de información de una base de datos a otra por tablas

# Conexión a la base de datos MySQL
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='ecomycr',
    password='zbyj8918',
    database='ecomycr'
)
mysql_cursor = mysql_conn.cursor()

# Conexión a la base de datos SQLite (db.sqlite3, creada por Django)
sqlite_conn = sqlite3.connect('db.sqlite3')
sqlite_cursor = sqlite_conn.cursor()

def migrate_table_data(table_name):
    # Obtener los datos de la tabla de MySQL
    mysql_cursor.execute(f"SELECT * FROM {table_name}")
    rows = mysql_cursor.fetchall()

    # Obtener la estructura de la tabla en MySQL (columnas)
    mysql_cursor.execute(f"DESCRIBE {table_name}")
    columns = mysql_cursor.fetchall()

    # Filtrar las columnas para evitar 'id' si es autoincremental
    column_names = [column[0] for column in columns]

    if 'id' in column_names:
        # Excluir la columna 'id' en los datos que vamos a insertar
        index_of_id = column_names.index('id')
        rows = [tuple(row[:index_of_id] + row[index_of_id+1:]) for row in rows]

    # Crear la lista de placeholders
    placeholders = ", ".join(["?" for _ in range(len(columns) - 1)])  # Excluyendo 'id'
    
    # Preparar el SQL para insertar en SQLite (sin la columna 'id')
    insert_sql = f"INSERT INTO {table_name} ({', '.join([column[0] for column in columns if column[0] != 'id'])}) VALUES ({placeholders})"
    
    # Insertar los datos en SQLite (sin 'id' si es autoincremental)
    sqlite_cursor.executemany(insert_sql, rows)
    sqlite_conn.commit()

# Ejemplo de uso
migrate_table_data('blog_blog')  # Cambia 'your_table_name' por el nombre real de tu tabla