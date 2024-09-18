from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Directorio de JSON
JSON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../Downloads/Hackaton2/json_files")


def set_value_in_json(data, path, value):
    """
    Navegar y actualizar el JSON siguiendo la ruta dada.
    Si la ruta contiene índices de lista, se convierten correctamente en enteros.
    """
    keys = path.replace('[', '.').replace(']', '').split('.')  # Dividir la ruta en claves e índices
    current = data

    # Navegar hasta el penúltimo nivel del JSON
    for i, key in enumerate(keys[:-1]):
        if isinstance(current, list):
            try:
                # Convertir la clave en índice solo si estamos en una lista
                key = int(key)
            except ValueError:
                return f"Error: se esperaba un índice entero, pero se recibió '{key}'"
        # Acceder al siguiente nivel
        try:
            current = current[key]
        except (KeyError, IndexError, TypeError) as e:
            return f"Error al navegar en el JSON: {e}"

    # Obtener la clave final
    final_key = keys[-1]
    if isinstance(current, list):
        try:
            final_key = int(final_key)  # Convertir el último índice en entero si es una lista
        except ValueError:
            return f"Error: se esperaba un índice entero, pero se recibió '{final_key}'"

    # Actualizar el valor en el nivel correcto
    try:
        current[final_key] = value
    except (KeyError, IndexError, TypeError) as e:
        return f"Error al intentar asignar el valor en el JSON: {e}"

    return None  # No hubo errores


@app.route('/')
def index():
    # Comprobar si el directorio existe
    if not os.path.exists(JSON_DIR):
        return "El directorio no existe", 404

    # Listar archivos JSON
    json_files = [f for f in os.listdir(JSON_DIR) if f.endswith('.json')]
    
    # Si no hay archivos JSON
    if not json_files:
        return "No hay archivos JSON disponibles", 404
    
    return render_template('index.html', json_files=json_files)


@app.route('/view/<filename>', methods=['GET'])
def view_json(filename):
    # Cargar el archivo JSON
    file_path = os.path.join(JSON_DIR, filename)
    with open(file_path, 'r') as f:
        data = json.load(f)
    return render_template('details.html', filename=filename, data=data)


@app.route('/save/<filename>', methods=['POST'])
def save_json(filename):
    # Cargar el archivo JSON actual
    file_path = os.path.join(JSON_DIR, filename)
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Obtener la ruta y el nuevo valor
    path = request.form['path']  # Ejemplo: "bultos[0].campo"
    new_value = request.form['value']  # El nuevo valor

    # Actualizar el JSON
    error = set_value_in_json(data, path, new_value)
    if error:
        return error, 400

    # Sobrescribir el archivo JSON
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    # Redirigir a la página de detalles
    anchor = path.replace('.', '_').replace('[', '_').replace(']', '_')
    return redirect(url_for('view_json', filename=filename) + f"#field-{anchor}")


if __name__ == '__main__':
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)
    app.run(debug=True)
