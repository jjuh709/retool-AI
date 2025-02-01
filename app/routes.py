from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load model
model = joblib.load('models/land_price_model.pkl')

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Land Price Prediction API is running!"})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    df = pd.DataFrame(data)
    prediction = model.predict(df)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
