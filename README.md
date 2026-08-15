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
│   ├── main.py
│   └── routers/
├── frontend/
│   └── src/
│       ├── components/
│       ├── views/
│       ├── App.vue
│       └── main.js
├── Data/
│   ├── Dataset.csv
│   └── preprocessedDataset.csv
├── model/
│   └── model.pkl
├── notebook/
│   └── main.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites 
- python 3.14.4
- Node.js and npm
- Vue.js
- Git

## Installation & Setup 

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
Install the frontend dependencies 
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

The trained model is saved in `model/model.pkl` which is loaded by FastAPI to make predictions.

## API EndPoint 

|   Method   |   Endpont   |   Description   |
| --- | --- | --- |
|  `GET`  |  `/engine/{brandname}/{modelname}`  |  To get the list of engines from the dataset according to the model  | 
|  `GET`  |  `/mileage/{engine}`  |  To get the mileage range according to the engine  |
|  `GET`  |  `/model_start_year/{brandname}/{modelname}`  |  To get the year in which that model was introduced in India  |
|  `GET`  |  `/fuel/{brandname}/{modelname}/{engine}`  | To get the list of fuel types for the selected car  |
|  `GET`  |  `/trans/{brandname}/{modelname}/{engine}`  | To get the list of transmission types available for that car  |
|  `POST` |  `/predict`  |  Predict the estimated selling price of your car  |


