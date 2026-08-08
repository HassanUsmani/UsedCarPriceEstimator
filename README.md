# UsedCarPriceEstimator

## Description

A machine learning model that predicts the estimated selling price of a used car.

## Features

- Predict used car prices
- Supports different brands and models
- Uses machine learning for price prediction
- FastAPI backend
- Vue.js frontend

## Technologies Used

- Python
- Pandas
- NumPy
- scikit-learn
- FastAPI
- Vue.js

## Project Structure

```text
UsedCarPriceEstimator/
├── backend/
│   └── main.py              # FastAPI backend
├── Data/
│   └── carDekhoDataset.csv  # Dataset
├── frontend/                # Vue.js frontend
├── model/
│   └── model.pkl            # Trained ML model
├── notebook/
│   └── main.ipynb           # Data analysis and model training
├── requirements.txt         # Python dependencies
├── .gitignore
└── README.md
```

## Installation 

### 1. Clone the repository 
```bash
git clone https://github.com/HassanUsmani/UsedCarPriceEstimator.git
cd UsedCarPriceEstimator
```

### 2. Backend 
Navigate to the backend
```bash
cd backend
```
Create a virtual environment 
```bash
python -m venv .venv
```
Activate the virtual environment
Windows:
```bash
.venv\Scripts\activate.bat
```
Install the backend dependencies
```bash
pip install -r ..\requirements.txt
```
Start the backend server 
```bash
uvicorn main:app --reload
```

### 3. Frontend
Navigate to the frontend
```bash
cd ../frontend
```
Install te frontend dependencies 
```bash
npm install 
```
Start the frontend server
```bash
npm run serve
```

## Machine Learning Model

The `notebook/main.ipynb` contains all the details of: 

- Data Preprocessing
- Exploratory Data Analysis
- Feature Engineering
- Model Training
- Model Evaluation

The trained model is saved in `model/model.pkl` which is loaded by FastAPI to make predictions
