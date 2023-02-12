# API в рамках практической работы по модулю 31

# импортируем нужные библиотеки
import joblib
import json
import pandas as pd

import dill # модуль для сериализации
from fastapi import FastAPI # модуль для создания API
from pydantic import BaseModel # Pydantic - это библиотека , которая обеспечивает проверку
# данных и управление настройками с использованием аннотаций типов(type annotations)

# импорт библиотек и классов для реализации вызова по расписанию
from apscheduler.schedulers.blocking import BlockingScheduler
import tzlocal # доступ к локальному часовому поясу
from datetime import datetime



# этот блок я планирую для организации заполнения Form(BaseModel)
def atribut_and_type():
    df = pd.read_csv('data/homework.csv').drop('price_category', axis=1)

    atribut_and_type = {}
    types = {
        'int64': 'int',
        'float64': 'float'
    }
    for k, v in df.dtypes.iteritems():
        atribut_and_type[k] = types.get(str(v), "str")
    return atribut_and_type

atribut_and_type = atribut_and_type()
# --------------------------- пока не реализовано --------------------------------

class Form(BaseModel): # создаем и заполняем атрибуты класса
    id: int
    url: str
    region: str
    region_url: str
    price: int
    year: float
    manufacturer: str
    model: str
    fuel: str
    odometer: float
    title_status: str
    transmission: str
    image_url: str
    description: str
    state: str
    lat: float
    long: float
    posting_date: str

class Prediction(BaseModel):
    id: int
    pred: str
    price: int




app = FastAPI()

with open('cars_pipe_new.pkl', 'rb') as file:
   model = dill.load(file)



df = pd.read_csv('data/homework.csv')
sched = BlockingScheduler(timezone=tzlocal.get_localzone())

@app.get('/status') #decorator
def status():
    return 'I am Ok!'


@app.get('/version') #decorator
def version():
    return model['metadata']

@app.post('/predict', response_model=Prediction)
def predict(form: Form):
    df = pd.DataFrame.from_dict([form.dict()])
    y = model['model'].predict(df)

    return {
        'id': form.id,
        'pred': y[0],
        'price': form.price
    }

@sched.scheduled_job('cron', second='*/5')
def on_time():
    data = df.sample(n=2)
    data = data.drop('price_category', axis=1)  # предикторы
    data['pred'] = model['model'].predict(data)
    print(f'{datetime.now()}: ok')
    print(data[['id', 'pred', 'price']])
    #print(data)

if __name__ == '__main__':
    sched.start()
