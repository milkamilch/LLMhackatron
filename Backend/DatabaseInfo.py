import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('DbHack.db')
cursor = conn.cursor()

# Nombre de la tabla que quieres inspeccionar
nombre_tabla = 'Orders'

# Consulta para obtener información de la tabla
cursor.execute(f"PRAGMA table_info({nombre_tabla})")

# Obtener los nombres de las columnas
columnas = [descripcion[1] for descripcion in cursor.fetchall()]

# Imprimir los nombres de las columnas
print(columnas)

# Cerrar la conexión
conn.close()