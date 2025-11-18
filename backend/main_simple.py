from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pickle
import os
import numpy as np
from datetime import datetime
from typing import Optional

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
            raise FileNotFoundError(f'Model not found at {MODEL_PATH}')
        with open(MODEL_PATH, 'rb') as f:
            _model = pickle.load(f)
    return _model

@app.get('/health')
async def health():
    return {'status': 'ok'}

@app.post('/predict', response_model=PredictionOut)
async def predict(inp: StudentInput):
    try:
        model = load_model()
        features = np.array([[inp.attendance, inp.study_hours, inp.internal_marks, inp.assignments_submitted, inp.activities_participated]])
        prob = float(model.predict_proba(features)[0][1])
        pred_label = 'Pass' if prob >= 0.5 else 'Fail'
        return {'prediction': pred_label, 'confidence': round(prob, 4)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
