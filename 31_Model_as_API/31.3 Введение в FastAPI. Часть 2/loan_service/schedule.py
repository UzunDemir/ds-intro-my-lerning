
import joblib
from apscheduler.schedulers.blocking import BlockingScheduler
import tzlocal
from datetime import datetime
import pandas as pd

df = pd.read_csv('model/data/loan_test.csv')
model = joblib.load('model/loan_pipe.pkl')

sched = BlockingScheduler(timezone=tzlocal.get_localzone_name())

@sched.scheduled_job('cron', second='*/10')
def on_time():
    data = df.sample(frac=0.05)
    data['preds'] = model['model'].predict(data)
    print(f'{datetime.now()}: ok')
    print(data[['Loan_ID', 'preds']])

if __name__ == '__main__':
    sched.start()