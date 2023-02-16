import os
import pandas as pd
import datetime as dt
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


args = {
    'owner': 'airflow',                      # Информация о владельце DAG
    'start_date': dt.datetime(2022, 6, 10),  # Время начала выполнения пайплайна
    'retries': 1,                            # Количество повторений в случае неудач
    'retry_delay': dt.timedelta(minutes=1),  # Пауза между повторами
    'depends_on_past': False,                # Зависимость от успешного окончания предыдущего запуска
}


def download_titanic_dataset():
    url = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'
    df = pd.read_csv(url)
    df.to_csv(os.path.join(os.path.expanduser('~'), 'titanic.csv'), encoding='utf-8')


def pivot_dataset():
    titanic_df = pd.read_csv(os.path.join(os.path.expanduser('~'), 'titanic.csv'))
    df = titanic_df.pivot_table(index=['Sex'],
                                columns=['Pclass'],
                                values='Name',
                                aggfunc='count').reset_index()
    df.to_csv(os.path.join(os.path.expanduser('~'), 'titanic_pivot.csv'))


with DAG(
        dag_id='titanic_pivot',           # Имя DAG
        schedule_interval="00 15 * * *",  # Периодичность запуска
        default_args=args,                # Базовые аргументы
) as dag:

    # BashOperator, выполняющий указанную bash-команду
    first_task = BashOperator(
        task_id='first_task',
        bash_command='echo "Here we start!"',
        dag=dag,
    )
    # Загрузка датасета
    create_titanic_dataset = PythonOperator(
        task_id='download_titanic_dataset',
        python_callable=download_titanic_dataset,
        dag=dag,
    )
    # Чтение, преобразование и запись датасета
    pivot_titanic_dataset = PythonOperator(
        task_id='pivot_dataset',
        python_callable=pivot_dataset,
        dag=dag,
    )
    # Порядок выполнения тасок
    first_task >> create_titanic_dataset >> pivot_titanic_dataset
