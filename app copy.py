from flask import Flask, render_template
import requests

app = Flask(__name__)

# Ruta principal para mostrar la lista de órdenes
@app.route('/')
def index():
    try:
        # Hacemos una solicitud GET a la API que está corriendo en el puerto 8000
        response = requests.get('http://127.0.0.1:8000/orderslist/')
        response.raise_for_status()  # Verifica si hay errores
        orders = response.json()  # Parseamos el JSON
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener la lista de órdenes: {e}')
        orders = []  # Si hay un error, devolvemos una lista vacía

    # Renderizamos la plantilla index.html con la lista de órdenes
    return render_template('index.html', json_files=orders)

# Nueva ruta para mostrar los detalles de una orden específica
@app.route('/order/<int:order_id>')
def order_details(order_id):
    try:
        # Hacemos una solicitud GET a la API para obtener los detalles de la orden específica
        response = requests.get(f'http://127.0.0.1:8000/order/{order_id}')
        response.raise_for_status()  # Verifica si hay errores
        order_data = response.json()  # Parseamos el JSON con los detalles de la orden
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener los detalles de la orden {order_id}: {e}')
        order_data = {}  # Si hay un error, devolvemos un diccionario vacío

    # Renderizamos la plantilla details.html con los detalles de la orden
    return render_template('details.html', data=order_data)

# Esto se ejecuta si corres el archivo directamente
if __name__ == '__main__':
    app.run(debug=True)
