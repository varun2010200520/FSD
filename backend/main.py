from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle
import os
import numpy as np
from datetime import datetime
from typing import Optional

from db import save_prediction, get_history, collection

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

app = FastAPI(title='Student Performance Predictor')

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test route to verify server is running
@app.get('/health')
async def health():
    return {'status': 'ok'}

class StudentInput(BaseModel):
    attendance: float = Field(..., ge=0, le=100)
    study_hours: float = Field(..., ge=0, le=24)
    internal_marks: float = Field(..., ge=0, le=100)
    assignments_submitted: int = Field(..., ge=0)
    activities_participated: int = Field(..., ge=0)

class PredictionOut(BaseModel):
    prediction: str
    confidence: float

_model = None

def load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError('Model not found. Run `train_model.py` to generate `model.pkl`.')
        with open(MODEL_PATH, 'rb') as f:
            _model = pickle.load(f)
    return _model

@app.post('/predict', response_model=PredictionOut)
async def predict(inp: StudentInput):
    try:
        print(f"Loading model from {MODEL_PATH}")
        model = load_model()
        print("Model loaded successfully")
        features = np.array([[inp.attendance, inp.study_hours, inp.internal_marks, inp.assignments_submitted, inp.activities_participated]])
        prob = float(model.predict_proba(features)[0][1])
        pred_label = 'Pass' if prob >= 0.5 else 'Fail'
        return {'prediction': pred_label, 'confidence': round(prob, 4)}
    except Exception as e:
        print(f"Error in predict: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/save')
async def save(inp: StudentInput, save: Optional[bool] = True):
    try:
        model = load_model()
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    features = np.array([[inp.attendance, inp.study_hours, inp.internal_marks, inp.assignments_submitted, inp.activities_participated]])
    prob = float(model.predict_proba(features)[0][1])
    pred_label = 'Pass' if prob >= 0.5 else 'Fail'

    doc = {
        'attendance': inp.attendance,
        'study_hours': inp.study_hours,
        'internal_marks': inp.internal_marks,
        'assignments_submitted': inp.assignments_submitted,
        'activities_participated': inp.activities_participated,
        'prediction': pred_label,
        'confidence': round(prob, 4),
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }

    if save:
        if collection is None:
            raise HTTPException(status_code=500, detail='MongoDB is not configured. Set MONGODB_URI environment variable.')
        inserted_id = await save_prediction(doc)
        return {'inserted_id': str(inserted_id), 'doc': doc}
    else:
        return {'doc': doc}

@app.get('/history')
async def history(limit: int = 100):
    if collection is None:
        raise HTTPException(status_code=500, detail='MongoDB is not configured. Set MONGODB_URI environment variable.')
    rows = await get_history(limit)
    return rows
