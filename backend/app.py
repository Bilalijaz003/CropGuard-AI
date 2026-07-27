# =========================
# CropGuard AI - Flask Backend
# Single Model - 6 Classes
# .keras format
# =========================

from flask import Flask, request, jsonify
from flask_cors import CORS

import numpy as np
import tensorflow as tf
from PIL import Image
import io
import os


# Initialize Flask app
app = Flask(__name__)
CORS(app)


# =========================
# LOAD AI MODEL
# Exact path to your model file
# =========================

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "CropGuardAI_Model.keras"
)

crop_model = None

print('='*50)
print('CropGuard AI - Starting Backend')
print('='*50)
print('Looking for model at:')
print(MODEL_PATH)
print('File exists:', os.path.exists(MODEL_PATH))
print('='*50)

if os.path.exists(MODEL_PATH):
    try:
        crop_model = tf.keras.models.load_model(MODEL_PATH)
        print('CropGuardAI_Model.keras loaded successfully')
        print('Model input shape :', crop_model.input_shape)
        print('Model output shape:', crop_model.output_shape)
        print('='*50)
    except Exception as e:
        print('Error loading model:', str(e))
        print('='*50)
else:
    print('ERROR: Model file not found at the path above')
    print('Please check:')
    print('1. CropGuardAI_Model.keras is inside backend/model/ folder')
    print('2. File name is exactly CropGuardAI_Model.keras')
    print('='*50)




# =========================
# CLASS LABELS
# Ordered exactly as your training folders:
#
# Wheat folder loaded first (alphabetical inside):
# Index 0 -> Wheat___Brown_Rust
# Index 1 -> Wheat___Healthy
# Index 2 -> Wheat___Yellow_Rust
#
# Sugarcane folder loaded second (alphabetical inside):
# Index 3 -> Bacterial Blight
# Index 4 -> Healthy
# Index 5 -> Red Rot
# =========================

ALL_CLASSES = [
    'Wheat___Brown_Rust',
    'Wheat___Healthy',
    'Wheat___Yellow_Rust',
    'Bacterial Blight',
    'Healthy',
    'Red Rot'
]




# =========================
# DISPLAY NAMES
# Clean readable names for frontend UI
# =========================

DISPLAY_NAMES = {
    'Wheat___Brown_Rust'  : 'Brown Rust',
    'Wheat___Healthy'     : 'Healthy',
    'Wheat___Yellow_Rust' : 'Yellow Rust',
    'Bacterial Blight'    : 'Bacterial Blight',
    'Healthy'             : 'Healthy',
    'Red Rot'             : 'Red Rot'
}




# =========================
# HEALTH STATUS MAPPING
# =========================

STATUS_MAP = {
    'Wheat___Brown_Rust'  : 'Diseased',
    'Wheat___Healthy'     : 'Healthy',
    'Wheat___Yellow_Rust' : 'Diseased',
    'Bacterial Blight'    : 'Diseased',
    'Healthy'             : 'Healthy',
    'Red Rot'             : 'Diseased'
}




# =========================
# CROP MAPPING
# Which crop each class belongs to
# =========================

CLASS_CROP = {
    'Wheat___Brown_Rust'  : 'wheat',
    'Wheat___Healthy'     : 'wheat',
    'Wheat___Yellow_Rust' : 'wheat',
    'Bacterial Blight'    : 'sugarcane',
    'Healthy'             : 'sugarcane',
    'Red Rot'             : 'sugarcane'
}




# =========================
# FARMING ADVICE
# =========================

ADVICE = {

    'Wheat___Healthy': (
        'Your wheat crop looks healthy and strong. '
        'Continue regular monitoring, maintain proper irrigation, '
        'and apply balanced fertilizer to sustain healthy growth.'
    ),

    'Wheat___Brown_Rust': (
        'Brown rust detected in your wheat crop. '
        'Apply fungicide containing Propiconazole or Tebuconazole immediately. '
        'Remove and destroy infected leaves to slow down spread. '
        'Ensure proper plant spacing for better air circulation. '
        'Avoid excessive watering as moisture speeds up rust development. '
        'Consider using rust-resistant wheat varieties in next planting season.'
    ),

    'Wheat___Yellow_Rust': (
        'Yellow rust detected in your wheat crop. '
        'Apply fungicide spray on infected areas immediately. '
        'Avoid over-irrigation since wet conditions speed up rust spread. '
        'Monitor neighboring fields as yellow rust spreads very quickly. '
        'Use resistant wheat varieties in next planting season.'
    ),

    'Healthy': (
        'Your sugarcane crop is in healthy condition. '
        'Maintain regular irrigation and balanced soil nutrition. '
        'Continue periodic field inspection to catch early disease signs.'
    ),

    'Bacterial Blight': (
        'Bacterial blight detected in your sugarcane crop. '
        'Remove and destroy all infected canes immediately. '
        'Disinfect all farming tools after each use. '
        'Avoid waterlogged field conditions as bacteria thrive in moisture. '
        'Apply copper-based bactericide to control further spread. '
        'Use certified disease-free cane cuttings for replanting.'
    ),

    'Red Rot': (
        'Red rot fungal disease detected in your sugarcane crop. '
        'This is a serious disease that can destroy the entire crop. '
        'Remove and burn all infected canes immediately. '
        'Do not use infected canes as seed material for replanting. '
        'Apply recommended fungicide and improve field drainage. '
        'Choose red rot resistant sugarcane varieties for next planting season.'
    )
}




# =========================
# IMAGE PREPROCESSING
# =========================

def preprocess_image(image_bytes, target_size=(224, 224)):
    """
    Preprocess image to match CropGuardAI_Model training format
    """

    # Open image from raw bytes
    image = Image.open(io.BytesIO(image_bytes))

    # Always convert to RGB
    image = image.convert('RGB')

    # Resize to match model input size
    image = image.resize(target_size)

    # Convert to numpy array
    img_array = np.array(image)

    # Normalize pixel values 0-255 to 0.0-1.0
    img_array = img_array / 255.0

    # Add batch dimension -> shape (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)

    return img_array




# =========================
# PREDICTION FUNCTION
# =========================

def predict_crop(image_bytes, crop_type):
    """
    Run CropGuardAI_Model prediction on uploaded crop image
    """

    # Use demo mode if model failed to load
    if crop_model is None:
        print('Model not loaded - switching to DEMO mode')
        return demo_prediction(crop_type)

    try:

        # Step 1 - Preprocess the image
        img_array = preprocess_image(image_bytes)

        # Step 2 - Run prediction on all 6 classes
        predictions = crop_model.predict(img_array)[0]

        # Step 3 - Print all class probabilities for debugging
        print('\nAll Class Predictions:')
        for i, prob in enumerate(predictions):
            print(f'  [{i}] {ALL_CLASSES[i]}: {prob*100:.2f}%')

        # Step 4 - Get highest confidence class
        class_index = int(np.argmax(predictions))
        confidence  = float(predictions[class_index]) * 100
        raw_label   = ALL_CLASSES[class_index]

        # Step 5 - Get display values
        display_name  = DISPLAY_NAMES.get(raw_label, raw_label)
        health_status = STATUS_MAP.get(raw_label, 'Unknown')
        advice_text   = ADVICE.get(raw_label, 'Consult an agricultural expert.')
        crop_detected = CLASS_CROP.get(raw_label, crop_type)

        print(f'\nFinal Prediction:')
        print(f'  Class     : {raw_label}')
        print(f'  Display   : {display_name}')
        print(f'  Health    : {health_status}')
        print(f'  Confidence: {confidence:.2f}%')
        print(f'  Crop      : {crop_detected}')

        return {
            'status'        : display_name,
            'health'        : health_status,
            'confidence'    : round(confidence, 2),
            'advice'        : advice_text,
            'crop_type'     : crop_type,
            'crop_detected' : crop_detected,
            'raw_label'     : raw_label,
            'model'         : 'CropGuardAI_Model'
        }

    except Exception as e:
        print('Prediction error:', str(e))
        return {'error': 'Prediction failed: ' + str(e)}




# =========================
# DEMO MODE
# =========================

def demo_prediction(crop_type):
    """
    Simulated prediction when model is not available
    """

    import random

    if crop_type == 'wheat':
        valid_classes = [
            'Wheat___Brown_Rust',
            'Wheat___Healthy',
            'Wheat___Yellow_Rust'
        ]
    else:
        valid_classes = [
            'Bacterial Blight',
            'Healthy',
            'Red Rot'
        ]

    raw_label  = random.choice(valid_classes)
    confidence = round(random.uniform(78.0, 96.5), 2)

    return {
        'status'        : DISPLAY_NAMES[raw_label],
        'health'        : STATUS_MAP[raw_label],
        'confidence'    : confidence,
        'advice'        : ADVICE[raw_label],
        'crop_type'     : crop_type,
        'crop_detected' : CLASS_CROP[raw_label],
        'raw_label'     : raw_label,
        'model'         : 'CropGuardAI_Model - DEMO MODE',
        'demo_mode'     : True
    }




# =========================
# API ROUTES
# =========================

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message'       : 'CropGuard AI Backend is Running',
        'model'         : 'CropGuardAI_Model.keras',
        'model_loaded'  : crop_model is not None,
        'total_classes' : len(ALL_CLASSES),
        'classes'       : ALL_CLASSES,
        'status'        : 'active'
    })




@app.route('/predict', methods=['POST'])
def predict():
    """
    Main detection API endpoint
    """

    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    crop_type  = request.form.get('crop_type', 'wheat').lower()

    if crop_type not in ['wheat', 'sugarcane']:
        return jsonify({
            'error': 'Invalid crop type. Use wheat or sugarcane'
        }), 400

    if image_file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    try:
        image_bytes = image_file.read()
        result      = predict_crop(image_bytes, crop_type)
        return jsonify(result)

    except Exception as e:
        print('Route error:', str(e))
        return jsonify({'error': 'Analysis failed: ' + str(e)}), 500




@app.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'model_name'    : 'CropGuardAI_Model.keras',
        'model_loaded'  : crop_model is not None,
        'all_classes'   : ALL_CLASSES,
        'total_classes' : len(ALL_CLASSES),
        'dataset_size'  : '600 images',
        'crops'         : ['wheat', 'sugarcane'],
        'status'        : 'running'
    })




# =========================
# RUN APPLICATION
# =========================

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )