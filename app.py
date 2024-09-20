from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Ruta principal para mostrar la lista de órdenes
@app.route('/')
def index():
    try:
        # Solicitud GET para obtener la lista de órdenes
        response = requests.get('http://127.0.0.1:8000/orderslist/')
        response.raise_for_status()  # Verifica si hay errores
        orders = response.json()  # Parseamos el JSON
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener la lista de órdenes: {e}')
        orders = []  # Si hay un error, devolvemos una lista vacía

    # Renderizamos la plantilla index.html con la lista de órdenes
    return render_template('index.html', json_files=orders)

# Ruta para mostrar los detalles de una orden específica
@app.route('/order/<int:order_id>')
def order_details(order_id):
    try:
        # Solicitud GET para obtener los detalles de la orden
        response = requests.get(f'http://127.0.0.1:8000/order/{order_id}')
        response.raise_for_status()  # Verifica si hay errores
        order_data = response.json()  # Parseamos el JSON con los detalles de la orden
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener los detalles de la orden {order_id}: {e}')
        order_data = {}  # Si hay un error, devolvemos un diccionario vacío

    # Renderizamos la plantilla details.html con los detalles de la orden
    return render_template('details.html', data=order_data)

# Ruta PUT para guardar la orden
@app.route('/save_order/<int:order_id>', methods=['PUT'])
def save_order(order_id):
    # Recibimos los datos del formulario en formato JSON
    try:
        order_data = request.json  # Obtenemos el JSON del cuerpo de la solicitud
        print(f'Recibido el siguiente JSON para guardar: {order_data}')
        
        # Hacemos la solicitud PUT a la API para actualizar la orden
        response = requests.put(f'http://127.0.0.1:8000/orders/{order_id}', json=order_data)
        response.raise_for_status()  # Verifica si hay errores
        updated_order = response.json()  # Parseamos el JSON de la respuesta

        return jsonify({'status': 'success', 'message': 'Order updated successfully', 'data': updated_order}), 200

    except requests.exceptions.RequestException as e:
        print(f'Error al actualizar la orden {order_id}: {e}')
        return jsonify({'status': 'error', 'message': 'Failed to update order'}), 400

# Esto se ejecuta si corres el archivo directamente
if __name__ == '__main__':
    app.run(debug=True)
