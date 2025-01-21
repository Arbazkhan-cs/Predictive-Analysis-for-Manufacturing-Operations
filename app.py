 app.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import joblib
import io
import json
import os

# Create data directory if it doesn't exist
DATA_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_DIR, exist_ok=True)

app = FastAPI(title="Manufacturing Predictive Analysis API")

# Define file paths
SAMPLE_DATA_PATH = os.path.join(DATA_DIR, "sample_manufacturing_data.csv")
UPLOADED_DATA_PATH = os.path.join(DATA_DIR, "uploaded_data.csv")
MODEL_PATH = os.path.join(DATA_DIR, "model.joblib")
SCALER_PATH = os.path.join(DATA_DIR, "scaler.joblib")

# Global variables to store model and scaler
model = None
scaler = None
required_columns = ['Machine_ID', 'Temperature', 'Run_Time']

class PredictionInput(BaseModel):
    Temperature: float
    Run_Time: float
    Machine_ID: int

# Generate synthetic data for testing
def generate_sample_data(n_samples=1000):
    np.random.seed(42)
    data = {
        'Machine_ID': np.random.randint(1, 11, n_samples),
        'Temperature': np.random.normal(75, 15, n_samples),
        'Run_Time': np.random.normal(100, 25, n_samples),
    }
    
    # Create downtime based on conditions
    df = pd.DataFrame(data)
    df['Downtime_Flag'] = (
        (df['Temperature'] > 90) | 
        (df['Run_Time'] > 140) | 
        ((df['Temperature'] > 80) & (df['Run_Time'] > 120))
    ).astype(int)
    
    return df

# Save sample data
try:
    sample_data = generate_sample_data()
    sample_data.to_csv(SAMPLE_DATA_PATH, index=False)
except Exception as e:
    print(f"Warning: Could not save sample data: {str(e)}")

@app.post("/upload")
async def upload_data(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Validate required columns
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400, 
                detail=f"CSV must contain columns: {', '.join(required_columns)}"
            )
        
        # Store the data temporarily
        df.to_csv(UPLOADED_DATA_PATH, index=False)
        return {"message": "Data uploaded successfully", "shape": df.shape}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/train")
async def train_model():
    try:
        # Try to load uploaded data, fall back to sample data if none exists
        try:
            df = pd.read_csv(UPLOADED_DATA_PATH)
        except FileNotFoundError:
            df = pd.read_csv(SAMPLE_DATA_PATH)
        
        # Prepare features and target
        X = df[['Machine_ID', 'Temperature', 'Run_Time']]
        y = df['Downtime_Flag']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale the features
        global scaler
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train the model
        global model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Make predictions on test set
        y_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        # Save the model and scaler
        joblib.dump(model, MODEL_PATH)
        joblib.dump(scaler, SCALER_PATH)
        
        return {
            "message": "Model trained successfully",
            "metrics": {
                "accuracy": round(accuracy, 3),
                "f1_score": round(f1, 3)
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
async def predict(input_data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=400, detail="Model not trained. Please train the model first.")
    
    try:
        # Prepare input data
        input_df = pd.DataFrame([{
            'Machine_ID': input_data.Machine_ID,
            'Temperature': input_data.Temperature,
            'Run_Time': input_data.Run_Time
        }])
        
        # Scale the input
        input_scaled = scaler.transform(input_df)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        confidence = model.predict_proba(input_scaled)[0].max()
        
        return {
            "Downtime": "Yes" if prediction == 1 else "No",
            "Confidence": round(float(confidence), 3)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
