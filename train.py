import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
import joblib
import os

# Load CSV
df = pd.read_csv("data/real_india_city_routes.csv")

# Features and target
X = df[["From", "To", "Distance (KM)"]]
y = df["Time (Hours)"]

# Preprocessing
preprocessor = ColumnTransformer(transformers=[
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["From", "To"])
], remainder='passthrough')

# Model pipeline
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

# Train
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model.fit(X_train, y_train)

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/route_time_predictor.pkl")
print("✅ Model trained and saved to /models/route_time_predictor.pkl")
