# Student Performance Predictor

Full-stack app: FastAPI backend + React frontend + scikit-learn model. Optional MongoDB Atlas storage.

## Quick Start (Windows PowerShell)

1. Backend: create venv and install

```powershell
cd c:\Users\cvaru\OneDrive\Desktop\hack\backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Train model (this writes `backend/model.pkl`)

```powershell
python train_model.py
```

3. Start backend

```powershell
$env:MONGODB_URI = "<your mongodb uri>" # optional
uvicorn main:app --reload --port 8000
```

4. Frontend (you can use Parcel, Vite or CRA; this repo includes simple files to run with Parcel)
- Install Parcel (globally) or use your preferred bundler

```powershell
cd ..\frontend
npm install -g parcel-bundler
npm install
parcel src/index.html --port 3000
```

Open `http://localhost:3000` to use the UI.

## API
- `POST /predict` -> JSON -> `{prediction, confidence}`
- `POST /save` -> stores record in MongoDB (requires `MONGODB_URI`)
- `GET /history` -> returns saved records

## File structure
```
student-performance-predictor/
├── backend/
│   ├── main.py
│   ├── model.pkl (generated)
│   ├── train_model.py
│   ├── db.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.js
│       ├── index.html
│       ├── components/Form.js
│       └── services/api.js
├── dataset/
│   └── students.csv
└── README.md
```

## Notes
- The backend expects `model.pkl` (a scikit-learn pipeline). Run `train_model.py` to produce it.
- Set `MONGODB_URI` to enable saving and history endpoints.
- If you want, I can:
  - Add a full `create-react-app` or Vite setup
  - Add tests and CI
  - Wire a Docker Compose for quick local setup

