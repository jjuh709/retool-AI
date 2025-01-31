import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import joblib

# Load data
data = pd.read_csv('data/land_price_data.csv')

# Check if 'price' column exists
if 'price' not in data.columns:
    raise KeyError("'price' column is missing in the data")

# Check if there's enough data
if len(data) < 2:
    raise ValueError("Not enough data to perform train-test split. Ensure you have more than one sample.")

# Features and target
X = data.drop('price', axis=1)  # Features
y = data['price']  # Target

# Convert categorical columns to numeric
categorical_cols = ['land_use', 'soil_quality', 'flood_risk_x', 'flood_risk_y']
X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)  # One-hot encoding

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Save model
joblib.dump(model, 'models/land_price_model.pkl')
