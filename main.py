from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import pickle
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and scaler
model_path = os.path.join(os.path.dirname(__file__), "diabetes_model.pkl")
scaler_path = os.path.join(os.path.dirname(__file__), "scaler.pkl")

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    print("Model and scaler loaded successfully!")
except Exception as e:
    print("Error loading model/scaler:", e)
    model = None
    scaler = None

# Input schema
class PatientData(BaseModel):
    Glucose: float
    BMI: float
    Age: float
    BloodPressure: float

# Prediction endpoint
@app.post("/predict")
def predict_diabetes(data: PatientData):
    if model is None or scaler is None:
        return {"error": "Model or scaler not loaded"}

    try:
        df = pd.DataFrame([data.dict()])
        df_scaled = scaler.transform(df)
        prediction = model.predict(df_scaled)[0]
        return {"prediction": int(prediction)}
    except Exception as e:
        return {"error": str(e)}

