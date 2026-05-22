from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

MODEL_PATH = os.path.join('model', 'car_price_model.pkl')

if os.path.exists(MODEL_PATH):
    model_data = joblib.load(MODEL_PATH)
    model_pipeline = model_data['pipeline']
    model_metrics = model_data['metrics']
    model_name = model_data['model_name']
else:
    model_pipeline = None
    model_metrics = {"R2": 0.0, "MAE": 0.0, "RMSE": 0.0}
    model_name = "No Model Loaded (Run train_model.py first)"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict_page')
def predict_page():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model_pipeline:
        return jsonify({'error': 'Machine learning model file missing. Train model first.'}), 500
    
    try:
        data = request.json
        
        input_data = pd.DataFrame([{
            'brand': str(data.get('brand')).strip(),
            'year': int(data.get('year')),
            'present_price': float(data.get('present_price')),
            'kms_driven': int(data.get('kms_driven')),
            'fuel_type': str(data.get('fuel_type')).strip(),
            'seller_type': str(data.get('seller_type')).strip(),
            'transmission': str(data.get('transmission')).strip(),
            'owner': int(data.get('owner', 0))
        }])
        
        prediction_output = model_pipeline.predict(input_data)[0]
        final_price = max(0.0, round(prediction_output, 2))
        
        return jsonify({
            'success': True,
            'predicted_price': final_price,
            'model_used': model_name,
            'accuracy_metric': f"{round(model_metrics['R2'] * 100, 2)}%"
        })
        
    except Exception as err:
        return jsonify({'success': False, 'error': str(err)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)