from django.shortcuts import render
from django.conf import settings
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os, io

# Load the trained model
model_path = os.path.join(settings.MODELS_DIR, 'model.h5')
model = load_model(model_path)

# Function to preprocess image before feeding into the model
def preprocess_image(image):
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0  # Normalize the image
    return image_array

# Function to predict image quality
def predict_image_quality(image):
    processed_image = preprocess_image(image)
    prediction = model.predict(np.expand_dims(processed_image, axis=0))
    return prediction

def hello(request):
    prediction = None
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        image = Image.open(io.BytesIO(image_file.read()))
        prediction = predict_image_quality(image)
        pred_idx = np.argmax(prediction)
        labels_dict = {0: 'Fresh', 1: 'Defect', 2: 'Mature', 3: 'Immature'}
        prediction = labels_dict[pred_idx]
    return render(request, 'index.html', {'prediction': prediction})
