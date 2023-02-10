import joblib
import json
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



@app.get('/status') #decorator
def status():
    return 'I am Ok!'

@app.get('/welcome') #decorator
def status():
    return 'You are welcome!'

@app.get('/version') #decorator
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



# def main():
#     model = joblib.load('model/loan_pipe.pkl')
#     print(model['metadata'])
#     with open('model/data/31.1 form_LP001024.json') as fin:
#         form = json.load(fin)
#         df = pd.DataFrame.from_dict([form])
#         y = model['model'].predict(df)
#         print(f'{form["Loan_ID"]}: {y[0]}')
#         #print(form)




