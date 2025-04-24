import numpy as np
import joblib
import os
import sys
import pandas as pd

# Get arguments from command line
if len(sys.argv) != 8:
    print("Error: 7 input values required (N, P, K, temperature, humidity, ph, rainfall).", file=sys.stderr)
    sys.exit(1)

try:
    inputs = list(map(float, sys.argv[1:]))  # Convert all inputs to float
except ValueError:
    print("Error: All inputs must be numbers.", file=sys.stderr)
    sys.exit(1)

# Load the model
model_path = os.path.join(os.path.dirname(__file__), "crop_recommendation_model.joblib")
model = joblib.load(model_path)

# Create DataFrame with feature names
feature_names = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
input_df = pd.DataFrame([inputs], columns=feature_names)

# Predict probabilities
probabilities = model.predict_proba(input_df)
crop_labels = model.classes_

# Filter crops with >= 75% confidence
threshold = 0.75
filtered_crops = [
    (crop_labels[idx], probabilities[0][idx])
    for idx in np.argsort(probabilities[0])[::-1]
    if probabilities[0][idx] >= threshold
]

# Output results (simple string to return to Express)
if filtered_crops:
    for crop, confidence in filtered_crops:
        print(f"{crop} ({confidence * 100:.2f}%)")
else:
    print("No crops found with confidence above 75%")