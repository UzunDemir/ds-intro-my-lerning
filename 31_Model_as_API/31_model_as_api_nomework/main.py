import json

import joblib

import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
model = joblib.load('model/loan_pipe.pkl')


class Form(BaseModel):
    Loan_ID: str
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: int
    Property_Area: str


class Prediction(BaseModel):
    Loan_ID: str
    Result: float


@app.get('/status')
def status():
    return "I'm OK"


@app.get('/version')
def version():
    return model['metadata']


@app.post('/predict', response_model=Prediction)
def predict(form: Form):
    df = pd.DataFrame.from_dict([form.dict()])
    y = model['model'].predict(df)

    return {
        'Loan_ID': form.Loan_ID,
        'Result': y[0]
    }



