from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Directory for JSON files
JSON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../Downloads/Hackaton2/json_files")


def set_value_in_json(data, path, value):
    """
    Navigate and update the JSON following the given path.
    If the path contains list indices, they are properly converted to integers.
    """
    keys = path.replace('[', '.').replace(']', '').split('.')  # Split the path into keys and indices
    current = data

    # Navigate to the second-to-last level of the JSON
    for i, key in enumerate(keys[:-1]):
        if isinstance(current, list):
            try:
                # Convert the key to an index only if we are in a list
                key = int(key)
            except ValueError:
                return f"Error: expected an integer index, but got '{key}'"
        # Access the next level
        try:
            current = current[key]
        except (KeyError, IndexError, TypeError) as e:
            return f"Error navigating the JSON: {e}"

    # Get the final key
    final_key = keys[-1]
    if isinstance(current, list):
        try:
            final_key = int(final_key)  # Convert the final index to integer if it's a list
        except ValueError:
            return f"Error: expected an integer index, but got '{final_key}'"

    # Update the value at the correct level
    try:
        current[final_key] = value
    except (KeyError, IndexError, TypeError) as e:
        return f"Error attempting to assign the value in the JSON: {e}"

    return None  # No errors


@app.route('/')
def index():
    # Check if the directory exists
    if not os.path.exists(JSON_DIR):
        return "The directory does not exist", 404

    # List JSON files
    json_files = [f for f in os.listdir(JSON_DIR) if f.endswith('.json')]

    # If there are no JSON files
    if not json_files:
        return "No JSON files available", 404

    return render_template('index.html', json_files=json_files)


@app.route('/view/<filename>', methods=['GET'])
def view_json(filename):
    # Load the JSON file
    file_path = os.path.join(JSON_DIR, filename)
    with open(file_path, 'r') as f:
        data = json.load(f)
    return render_template('details.html', filename=filename, data=data)


@app.route('/save/<filename>', methods=['POST'])
def save_json(filename):
    # Load the current JSON file
    file_path = os.path.join(JSON_DIR, filename)
    with open(file_path, 'r') as f:
        data = json.load(f)

    # Get the path and the new value
    path = request.form['path']  # Example: "bultos[0].campo"
    new_value = request.form['value']  # The new value

    # Update the JSON
    error = set_value_in_json(data, path, new_value)
    if error:
        return error, 400

    # Overwrite the JSON file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    # Redirect to the details page
    anchor = path.replace('.', '_').replace('[', '_').replace(']', '_')
    return redirect(url_for('view_json', filename=filename) + f"#field-{anchor}")


if __name__ == '__main__':
    if not os.path.exists(JSON_DIR):
        os.makedirs(JSON_DIR)
    app.run(debug=True)
