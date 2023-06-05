import os

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "new push done")
    return f"Hello {name}!"

@app.route("/api/junkfood", methods=['POST'])
def junkfood():
    if 'image' not in request.files:
        response = {'message': 'No image file found'}
        return jsonify(response), 400
    
    image = request.files['image']

    if image.filename == '':
        response = {'message': 'Invalid image file'}
        return jsonify(response), 400
    
    # Save the image to a desired location
    image.save(image.filename)

    # Load & use model here (todo)

    # Delete the image file
    os.remove(image.filename)

    response = {'message': 'Image received and deleted successfully'}
    return jsonify(response)

@app.route('/api/exercises', methods=['POST'])
def process():
    if not request.is_json:
        response = {'message': 'Invalid JSON data'}
        return jsonify(response), 400

    data = request.get_json()

    # Load & use model here (todo)
    
    # Return the JSON data back
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# cara run : flask --app main run
# "main" karena nama filenya main.py