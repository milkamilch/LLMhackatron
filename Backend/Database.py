import sqlite3

# Ruta del archivo SQLite (ajusta a tu fichero)
ruta_db = 'BackEnd/DbHack.db'

# Conectar a la base de datos
conexion = sqlite3.connect(ruta_db)

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()

# Ejecutar una consulta SQL (ajusta tu consulta)
consulta = "SELECT * FROM Orders "
cursor.execute(consulta)

# Obtener todos los resultados de la consulta
resultados = cursor.fetchall()

# Mostrar los resultados
for fila in resultados:
    print(fila)

# Cerrar la conexión
conexion.close()