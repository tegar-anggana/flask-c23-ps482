# cara run : flask --app main run
# "main" karena nama filenya main.py

import os
import io
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "new push done")
    return f"Hello {name}!"

# JUNK FOOD
junkfood_model = load_model('junkfood_model_mobilenet_acc90.h5')
@app.route("/api/junkfood", methods=['POST'])
def junkfood():
    if 'image' not in request.files:
        response = {'message': 'No image file found'}
        return jsonify(response), 400
    
    file = request.files['image']
    
    # Save the image to a desired location
    # image.save(image.filename)

    # Load & Pre process image (bahan klasifikasi)
    image_size = 224
    img = image.load_img(io.BytesIO(file.stream.read()), target_size=(image_size, image_size))
    img = image.img_to_array(img)
    img = img / 255.0

    # Perform the prediction
    # class_labels = ['French fries', 'Hotdog', 'Donut', 'Sandwich', 'Taco', 'Fried chicken', 'Pizza', 'Burger', 'Baked Potato']
    # class_labels = ['Sandwich', 'Fried chicken', 'Hotdog', 'French fries', 'Pizza', 'Baked Potato', 'Burger', 'Donut', 'Taco']
    class_labels = ['Baked Potato', 'Burger', 'Donut', 'French fries', 'Fried chicken', 'Hotdog', 'Pizza', 'Sandwich', 'Taco']
    prediction = junkfood_model.predict(np.expand_dims(img, axis=0))
    predicted_class_index = np.argmax(prediction)
    predicted_class = class_labels[predicted_class_index]

    # Delete the image file
    # os.remove(image.filename)

    response = {'hasil': predicted_class}
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