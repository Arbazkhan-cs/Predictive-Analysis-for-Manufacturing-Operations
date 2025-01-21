# Manufacturing Predictive Analysis API

A FastAPI-based machine learning service that predicts when manufacturing machines will go down based on Random Forest classification. The API has endpoints for data upload, model training, and makes predictions about the probability of machine failure.

### Table of Contents
- [Features](#features)
- [Why Random Forest?](#why-random-forest)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [API Endpoints](#api-endpoints)
- [Testing with Postman](#testing-with-postman)
- [Quick Testing Guide](#quick-testing-guide)
- [Docker Deployment](#docker-deployment)
- [Hugging Face Deployment](#hugging-face-deployment)
- [Data Format](#data-format)
- [Error Handling](#error-handling)
- [Contributing](#contributing)

### Features
Predicts machine downtime given operational parameters
Automatic synthetic data generation for testing
RESTful API interface
Docker containerization
Error handling implemented completely
Incorporated data validation in models
Metrics to measure performance of the model
 
### Why Random Forest?
Robust against noisy data of manufacturing processes
Handles nonlinear relations
Produces insights regarding feature importance
Fast speed for making predictions in the production environment
Incorporated confidence scores for predictions
Effective handling of missing values

## Tech Stack
Python 3.9
FastAPI
scikit-learn
pandas
Docker
uvicorn

## Quick Start
 

1.  Clone the repository:
git clone https://github.com/yourusername/manufacturing-prediction-api
cd manufacturing-prediction-api
```
2. **Build and run with Docker:**
```bash
docker build -t manufacturing-api .
docker run -p 7860:7860 manufacturing-api
```
3. **Access the API:**
API: http://localhost:7860
Documentation: http://localhost:7860/docs
## Detailed Setup

### Local Setup
1. virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Run the application
```bash
uvicorn app:app --host 0.0.0.0 --port 7860 --reload
```
## API Endpoints

### 1. Upload Data (Optional)
```
POST /upload
- CSV file that contains manufacturing data
Columns Needed: Machine_ID, Temperature, Run_Time
```

### 2. Train Model
```
POST /train
Trains model using uploaded or synthetic data.
Returns accuracy metrics
```

### 3. Make Predictions
```
POST /predict
- Accepts a JSON with the parameters for machine
- Returns the predicted downtime along with a confidence score
```

## Testing with Postman

### Full Testing Flow

1. Upload Data (Optional):
- Method: POST
- URL: `http://localhost:7860/upload`
- Body: form-data
  - Key: file (type: file)
  - Value: your CSV file

2. Train Model:
- Method: POST
- URL: `http://localhost:7860/train`
- No body required

3. **Make Predictions:**
- Method: POST
- URL: `http://localhost:7860/predict`
- Headers: `Content-Type: application/json`
- Body:
```json
{
    "Machine_ID": 1,
    "Temperature": 85,
    "Run_Time": 130
}
```

## Quick Testing Guide

For quick testing, you only need two steps (no data upload required):

1. **Train the model:**
```bash
curl -X POST http://localhost:7860/train
```

2. **Make a prediction:**
```bash
curl -X POST http://localhost:7860/predict \
     -H "Content-Type: application/json" \
-d '{"Machine_ID": 1, "Temperature": 85, "Run_Time": 130}'
```

## Example Responses

### Train Response
```json
{
    "message": "Model trained successfully",
    "metrics": {
        "accuracy": 0.945,
        "f1_score": 0.932
    }
}
```

### Predict Response
```json
{
    "Downtime": "Yes",
    "Confidence": 0.892
}
```

## Data Format

### Input Data Format (for upload)
```csv
Machine_ID,Temperature,Run_Time,Downtime_Flag
1,85,120,1
2,70,90,0
3,95,150,1
```

### Prediction Input Format
```json
{
    "Machine_ID": 1,
    "Temperature": 85,
    "Run_Time": 130
}
```

## Error Handling

Common error responses:

1. Model not trained:
```json
{
    "detail": "Model not trained. Please train the model first."
}
```

2. Invalid file format:
```json
{
    "detail": "Only CSV files are allowed"
}
```

3. Missing columns:
```json
{
    "detail": "CSV must contain columns: Machine_ID, Temperature, Run_Time"
}
```

## Docker Deployment

1. Build the image:
```bash
docker build -t manufacturing-api.

RUN docker run -p 7860:7860 manufacturing-api

## Hugging Face Deployment

1. Create a new Space on Hugging Face
2. Set up Git:
```bash
git init
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
git add.
git commit -m "Initial commit"
git push space main
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License
