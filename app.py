from flask import Flask, render_template, request
import pickle
import numpy as np
from logic.disease_rules import infer_disease
import os

app = Flask(__name__)
model = pickle.load(open('model/liver_model.pkl', 'rb'))
scaler = pickle.load(open('model/scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = [float(x) for x in request.form.values()]
    features = {
        'Age': data[0],
        'Gender': data[1],
        'Total_Bilirubin': data[2],
        'Direct_Bilirubin': data[3],
        'Alkaline_Phosphotase': data[4],
        'Alamine_Aminotransferase': data[5],
        'Aspartate_Aminotransferase': data[6],
        'Total_Protiens': data[7],
        'Albumin': data[8],
        'Albumin_and_Globulin_Ratio': data[9]
    }
    input_scaled = scaler.transform([list(features.values())])
    pred = model.predict(input_scaled)[0]
    disease_info = infer_disease(features)
    result = 'Liver Disease Detected' if pred == 1 else 'No Liver Disease Detected'
    return render_template('result.html', result=result, disease=disease_info['primary'], reason=disease_info['explanation'])

if __name__ == '__main__':
    app.run(debug=True)
