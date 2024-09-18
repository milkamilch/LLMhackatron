from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
from typing import List,Optional
from fastapi import HTTPException

# Inicializar FastAPI
app = FastAPI()

# Definir un modelo para los datos que se devolverán
class Order(BaseModel):
    ID: int
    client_Id: int
    customer_name: Optional[str]
    reference: Optional[str]
    incoterms: Optional[str]
    pickup_name: Optional[str]
    pickup_address: Optional[str]
    pickup_postalcode: Optional[str]
    pickup_city: Optional[str]
    pickup_country: Optional[str]
    pickup_tlf: Optional[str]
    pickup_contact_name: Optional[str]
    pickup_email: Optional[str]
    delivery_name: Optional[str]
    delivery_address: Optional[str]
    delivery_postalcode: Optional[str]
    delivery_city: Optional[str]
    delivery_country: Optional[str]
    delivery_tlf: Optional[str]
    delivery_contact_name: Optional[str]
    delivery_email: Optional[str]
    pck_quantity: Optional[int]
    description: Optional[str]
    dimensions: Optional[str]
    weight: Optional[str]
    remarks: Optional[str]
    raw_email: Optional[str]
    status: Optional[str]
    user: Optional[str]
    sent: Optional[int]
    creation_date: Optional[str]
    modified_date: Optional[str]

# Modelo para el endpoint OrdersList (solo los campos solicitados)
class OrderList(BaseModel):
    ID: int
    customer_name: Optional[str]
    pickup_email: Optional[str]
    pickup_country: Optional[str]
    delivery_country: Optional[str]
    status: Optional[str]
    user: Optional[str]
    sent: Optional[bool]
    creation_date: Optional[str]
# Ruta del archivo SQLite (ajusta a tu fichero)
DATABASE = "Backend/DbHack.db"

# Conectar y recuperar todos los registros de la tabla "orders"
def get_orders_from_db():
    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()
    
    # Ejecutar una consulta para obtener todos los registros de la tabla "orders"
    cursor.execute("""
        SELECT ID, client_Id, customer_name, reference, incoterms, 
               pickup_name, pickup_address, pickup_postalcode,pickup_city, pickup_country, pickup_tlf, 
               pickup_contact_name, pickup_email, delivery_name, delivery_address, delivery_postalcode, 
               delivery_city, delivery_country, delivery_tlf, delivery_contact_name, delivery_email, 
               pck_quantity, description, dimensions, weight, remarks, raw_email,status, user, sent, 
               creation_date, modified_date
        FROM Orders
    """)

    registers = cursor.fetchall()
    
    # Cerrar la conexión
    conexion.close()

    # Convertir los registros a una lista de diccionarios
    orders = [
        {
            "ID": file[0],
            "client_Id": file[1],
            "customer_name": file[2],
            "reference": file[3],
            "incoterms": file[4],
            "pickup_name": file[5],
            "pickup_address": file[6],
            "pickup_postalcode": file[7],
            "pickup_city": file[8],
            "pickup_country": file[9],
            "pickup_tlf": file[10],
            "pickup_contact_name": file[11],
            "pickup_email": file[12],
            "delivery_name": file[13],
            "delivery_address": file[14],
            "delivery_postalcode": file[15],
            "delivery_city": file[16],
            "delivery_country": file[17],
            "delivery_tlf": file[18],
            "delivery_contact_name": file[19],
            "delivery_email": file[20],
            "pck_quantity": file[21],
            "description": file[22],
            "dimensions": file[23],
            "weight": file[24],
            "remarks": file[25],
            "raw_email": file[26],
            "status": file[27],
            "user": file[28],
            "sent": bool(file[29]),
            "creation_date": file[30],
            "modified_date": file[31]
        }
    for file in registers]
    
    return orders


# Función para obtener solo los campos específicos (para el nuevo endpoint OrdersList)
def get_orders_list_from_db():
    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()
    
    # Ejecutar una consulta SQL para obtener solo los campos requeridos
    cursor.execute("""
        SELECT ID, customer_name, pickup_email,pickup_country,delivery_country, status, user, sent, creation_date
        FROM orders
    """)
    
    registros = cursor.fetchall()
    
    # Cerrar la conexión
    conexion.close()

    # Convertir los registros a una lista de diccionarios
    ordenes = [
        {
            "ID": fila[0],
            "customer_name": fila[1],
            "pickup_email": fila[2],
            "pickup_country": fila[3],
            "delivery_country": fila[4],
            "status": fila[5],
            "user": fila[6],
            "sent": bool(fila[7]),
            "creation_date": fila[8]
        }
    for fila in registros]
    
    return ordenes

# Función para obtener una orden por ID
def get_order_by_id_from_db(order_id: int):
    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL para obtener la orden con el ID específico
    cursor.execute("""
        SELECT ID, client_Id, customer_name, reference, incoterms, 
               pickup_name, pickup_address, pickup_postalcode,pickup_city, pickup_country, pickup_tlf, 
               pickup_contact_name, pickup_email, delivery_name, delivery_address, delivery_postalcode, 
               delivery_city, delivery_country, delivery_tlf, delivery_contact_name, delivery_email, 
               pck_quantity, description, dimensions, weight, remarks, raw_email, status, user, sent, 
               creation_date, modified_date
        FROM orders
        WHERE ID = ?
    """, (order_id,))

    registro = cursor.fetchone()
    conexion.close()

    # Si no se encuentra el registro, retornar None
    if registro is None:
        return None

    # Convertir el registro a un diccionario
    orden = {
        "ID": registro[0],
        "client_Id": registro[1],
        "customer_name": registro[2],
        "reference": registro[3],
        "incoterms": registro[4],
        "pickup_name": registro[5],
        "pickup_address": registro[6],
        "pickup_postalcode": registro[7],
        "pickup_city": registro[8],
        "pickup_country": registro[9],
        "pickup_tlf": registro[10],
        "pickup_contact_name": registro[11],
        "pickup_email": registro[12],
        "delivery_name": registro[13],
        "delivery_address": registro[14],
        "delivery_postalcode": registro[15],
        "delivery_city": registro[16],
        "delivery_country": registro[17],
        "delivery_tlf": registro[18],
        "delivery_contact_name": registro[19],
        "delivery_email": registro[20],
        "pck_quantity": registro[21],
        "description": registro[22],
        "dimensions": registro[23],
        "weight": registro[24],
        "remarks": registro[25],
        "raw_email": registro[26],
        "status": registro[27],
        "user": registro[28],
        "sent": bool(registro[29]),
        "creation_date": registro[30],
        "modified_date": registro[31]
    }

    return orden

# Función para actualizar una orden por ID con los campos opcionales
def update_order_in_db(order_id: int, order_data: dict):
    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()

    # Construir dinámicamente la consulta SQL para actualizar solo los campos proporcionados
    fields = []
    values = []

    for key, value in order_data.items():
        if value is not None:  # Solo actualizamos los campos que no son None
            fields.append(f'"{key}" = ?')
            values.append(value)
    
    # Si no hay campos para actualizar, salir de la función
    if not fields:
        return None
    
    # Agregar el ID al final de la lista de valores para la condición WHERE
    values.append(order_id)

    # Crear la consulta SQL dinámicamente
    sql_query = f'UPDATE orders SET {", ".join(fields)} WHERE ID = ?'

    # Ejecutar la consulta SQL
    cursor.execute(sql_query, values)

    # Confirmar la transacción
    conexion.commit()
    rows_affected = cursor.rowcount
    conexion.close()

    # Si no se actualizó ninguna fila, retornar None
    if rows_affected == 0:
        return None

    return rows_affected


# Definir el método GetOrder() para devolver todos los registros
@app.get("/orders/", response_model=List[Order])
def GetOrder():
    orders = get_orders_from_db()
    return orders

# Endpoint para obtener solo los campos seleccionados (OrdersList)
@app.get("/orderslist/", response_model=List[OrderList])
def OrdersList():
    ordersList = get_orders_list_from_db()
    return ordersList


# Endpoint para obtener una orden por ID
@app.get("/order/{order_id}", response_model=Order)
def get_order_by_id(order_id: int):
    order = get_order_by_id_from_db(order_id)
    # Si no se encuentra la orden, devolver un error
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order



# Endpoint para actualizar una orden por ID usando la clase Order
@app.put("/orders/{order_id}")
def update_order(order_id: int, order: Order):
    #print(order)
    # Convertir el modelo Pydantic a un diccionario para pasar a la base de datos
    updated_rows = update_order_in_db(order_id, order.dict(exclude_unset=True))
    
    # Si no se actualizó ninguna fila, lanzar una excepción 404
    if updated_rows is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return {"message": "Order updated successfully"}