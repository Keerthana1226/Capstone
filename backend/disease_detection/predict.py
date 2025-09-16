import sys
import os
from PIL import Image
import numpy as np

# Suppress informational messages from TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from tensorflow.keras.layers import RandomFlip, RandomRotation, RandomZoom

# --- Class Names Dictionary ---
CLASS_NAMES = {
    'maize': [
        'Corn___Common_Rust',
        'Corn___Gray_Leaf_Spot',
        'Corn___Healthy',
        'Corn___Northern_Leaf_Blight',
        'Corn___Northern_Leaf_Spot',
        'Corn___Phaeosphaeria_Leaf_Spot'
    ],
    'rice': [
        'bacterial_leaf_blight', 'brown_spot', 'healthy', 'leaf_blast',
        'leaf_scald', 'narrow_brown_spot', 'neck_blast', 'rice_hispa',
        'sheath_blight', 'tungro'
    ],
    'wheat': ['Aphid', 'Black_Rust', 'Blast', 'Brown_Rust', 'Common_root_rot', 'Fusarium Head Blight', 
              'Healthy', 'Leaf_Blight', 'Mildew', 'Mite','Septoria', 'Smut', 'Stem_fly', 'Tanspot', 'Yellow_Rust']
}

# --- Model Paths ---
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path_dict = {
    'maize': os.path.join(script_dir, 'models', 'maize_disease_model.keras'),
    'rice': os.path.join(script_dir, 'models', 'rice_disease_model.keras'),
    'wheat': os.path.join(script_dir, 'models', 'wheat_disease_model.pth')
}

# --- Get POSITIONAL arguments from Node.js ---
try:
    image_path = sys.argv[1]
    crop_type = sys.argv[2]
except IndexError:
    print("Error: Script expects two arguments: image_path and crop_type.")
    sys.exit(1)

model_path = model_path_dict.get(crop_type)

if not model_path:
    print(f"Error: No model found for crop type '{crop_type}'")
    sys.exit(1)

prediction = "Could not determine the disease."

try:
    if model_path.endswith('.keras') or model_path.endswith('.h5'):
        # ✅ Fix: Register preprocessing layers
        custom_objects = {
            "RandomFlip": RandomFlip,
            "RandomRotation": RandomRotation,
            "RandomZoom": RandomZoom,
        }

        model = tf.keras.models.load_model(model_path, custom_objects=custom_objects)

        img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)

        predictions = model.predict(img_array, verbose=0)
        score = tf.nn.softmax(predictions[0])
        class_name = CLASS_NAMES[crop_type][np.argmax(score)]
        confidence = 100 * np.max(score)
        prediction = f"{class_name} (Confidence: {confidence:.2f}%)"

    elif model_path.endswith('.pth'):
        import torch
        import torchvision.transforms as transforms
        model = torch.load(model_path, map_location=torch.device('cpu'))
        model.eval()
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        img = Image.open(image_path).convert('RGB')
        img_tensor = preprocess(img).unsqueeze(0)
        with torch.no_grad():
            outputs = model(img_tensor)
            _, predicted_idx = torch.max(outputs, 1)
            class_name = CLASS_NAMES[crop_type][predicted_idx.item()]
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence = probabilities[0][predicted_idx.item()].item() * 100
            prediction = f"{class_name} (Confidence: {confidence:.2f}%)"

except Exception as e:
    prediction = f"Error processing model: {str(e)}"

# --- Print the final result ---
print(prediction)
sys.stdout.flush()