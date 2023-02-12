import pandas as pd

df = pd.read_csv('data/homework.csv').drop('price_category', axis=1)

atribut_and_type = {}
types = {
    'int64': 'int',
    'float64': 'float'
}
for k, v in df.dtypes.iteritems():
    atribut_and_type[k] = types.get(str(v), "str")

    print(f'{k}: {types.get(str(v), "str")}')
#print(atribut_and_type)




# Таймер обратного отсчета

import time, subprocess

wait = 10
while wait > 0:
    print(wait, end='')
    time.sleep(1)
    wait = wait - 1

# Воспроизведение звукового файла по завершении обратного отсчета
subprocess.Popen(['start', 'C:\\example\alarm.wav'], shell = True)