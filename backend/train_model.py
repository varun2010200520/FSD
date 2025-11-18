"""
Train a simple classifier on sample dataset and save a pipeline to `model.pkl`.
Run: `python -m venv .venv; .\.venv\Scripts\activate; pip install -r requirements.txt; python train_model.py`
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'students.csv')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

if __name__ == '__main__':
    df = pd.read_csv(DATA_PATH)
    # Expect columns: attendance,study_hours,internal_marks,assignments_submitted,activities_participated,outcome
    features = ['attendance','study_hours','internal_marks','assignments_submitted','activities_participated']
    X = df[features]
    y = df['outcome'].map({'Fail':0,'Pass':1})

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    probs = pipeline.predict_proba(X_test)[:,1]

    print('Accuracy:', accuracy_score(y_test, preds))
    print('\nClassification Report:\n', classification_report(y_test, preds))

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(pipeline, f)

    print(f"Model saved to {MODEL_PATH}")
