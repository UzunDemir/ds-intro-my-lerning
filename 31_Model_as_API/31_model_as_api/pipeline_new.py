# создание пайплайна, который находит лучшую модель и сериализует ее
from datetime import datetime # модуль для работы со временем

import dill # модуль для сериализации
import pandas as pd
import time
from sklearn.ensemble import RandomForestClassifier # модель случайного леса
from sklearn.model_selection import cross_val_score # среднее значение по сверткам перекрестной проверки
from sklearn.preprocessing import OneHotEncoder # класс - кодировщик категориальных фич
from sklearn.preprocessing import StandardScaler # класс для стандартизации числовых фич, если большой разброс в данных
from sklearn.preprocessing import FunctionTransformer # переводит функции в шаги пайплайна
from sklearn.impute import SimpleImputer # класс для заполнения пропусков,
# используя разные стратегии: среднее, медиана, мода и т. д.
from sklearn.compose import ColumnTransformer, make_column_selector # класс для объединения обработки категориальных и
# числовых фич в один шаг пайплайна

from sklearn.pipeline import Pipeline # импортируем класс из библиотеки для создания пайплайна
from sklearn.linear_model import LogisticRegression # логистическая регрессия
from sklearn.svm import SVC # Метод опорных векторов


def filter_data(df): # функция удаления ненужных столбцов
    columns_to_drop = [
        'id',
        'url',
        'region',
        'region_url',
        'price',
        'manufacturer',
        'image_url',
        'description',
        'posting_date',
        'lat',
        'long'
    ]

    return df.drop(columns_to_drop, axis=1)


def remove_outliers(df): # функция удаления выбросов

    def calculate_outliers(data): # функция нахождения квантилей (границ, выше которых считаем выбросами)
        q25 = data.quantile(0.25)
        q75 = data.quantile(0.75)
        iqr = q75 - q25
        boundaries = (q25 - 1.5 * iqr, q75 + 1.5 * iqr)

        return boundaries

    df = df.copy() # создаем копию датафрейма

    boundaries = calculate_outliers(df['year']) # вызываем функцию для расчета квантилей

    df.loc[df['year'] < boundaries[0], 'year'] = round(boundaries[0]) # удаляем выбросы
    df.loc[df['year'] > boundaries[1], 'year'] = round(boundaries[1])

    return df


def create_features(df): # создаем новые фичи

    df = df.copy()

    def short_model(x): # короткое название модели
        import pandas
        if not pandas.isna(x): # если не пустое значение
            return x.lower().split(' ')[0] # берем первое слово, удаляем пробел и переводим в нижний регистр
        else:
            return x

    # Добавляем фичу "short_model" – это первое слово из колонки model
    df.loc[:, 'short_model'] = df['model'].apply(short_model)

    # Добавляем фичу "age_category" (категория возраста)
    df.loc[:, 'age_category'] = df['year'].apply(lambda x: 'new' if x > 2013 else ('old' if x < 2006 else 'average'))

    return df


def main():
    df = pd.read_csv('data/homework.csv') # читаем датафрейм

    X = df.drop('price_category', axis=1) # предикторы
    y = df['price_category'] # целевая переменная

    numerical_features = make_column_selector(dtype_include=['int64', 'float64']) # создаем список числовых фич
    categorical_features = make_column_selector(dtype_include=object) #  создаем список текстовых фич

    numerical_transformer = Pipeline(steps=[ # шаг пайплайна:
        ('imputer', SimpleImputer(strategy='median')), # заполняем числовые медианой
        ('scaler', StandardScaler()) # стандартизируем числовые данные
    ])

    categorical_transformer = Pipeline(steps=[ # шаг пайплайна:
        ('imputer', SimpleImputer(strategy='most_frequent')), # заполняем категориальные часто встречающимся
        ('encoder', OneHotEncoder(handle_unknown='ignore')) # оцифровываем с игнорированием ошибок кодирования
    ])

    # column_transformer связывает названия колонок с преобразователем
    # принимает на вход список кортежей: название, преобразователь, список столбцов для преобразования
    column_transformer = ColumnTransformer(transformers=[ # объединяем обработку числовых
        # и категориальных фич в один шаг
        ('numerical', numerical_transformer, numerical_features),
        ('categorical', categorical_transformer, categorical_features)
    ])

    # все шаги подготовки данных для обучения (пайплайны выше) объединим в один пайплайн - препроцессор
    preprocessor = Pipeline(steps=[
        ('filter', FunctionTransformer(filter_data)),
        ('outlier_remover', FunctionTransformer(remove_outliers)),
        ('feature_creator', FunctionTransformer(create_features)),
        ('column_transformer', column_transformer)
    ])

    models = [
        LogisticRegression(solver='liblinear'),
        RandomForestClassifier(),
        SVC()
    ]
    # перебираем все модели, обучаем, и выбираем лучший
    best_score = .0
    best_pipe = None
    for model in models:
        # используя пайплайн, который состоит из препроцессора подготовкм данных и самого обучения
        pipe = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', model)
        ])
        start = time.time()  # включим таймер для подсчета времени обучения
        # проводим кросс-валидацию на 4 фолда
        score = cross_val_score(pipe, X, y, cv=4, scoring='accuracy')
        elapsed_time = time.time() - start  # зафиксируем время обучения модели
        # выводим имя модели, среднее значение accuracy, среднеквадратичное (стандартное) отклонение
        # и время обучения модели
        print(f'model: {type(model).__name__}, acc_mean: {score.mean():.4f}, acc_std: {score.std():.4f}',
              f", with a fitting time: {elapsed_time:.3f}")
        if score.mean() > best_score: # выбираем лучшую модель
            best_score = score.mean()
            best_pipe = pipe
    # выводим лучшую модель
    print(f'best model: {type(best_pipe.named_steps["classifier"]).__name__}, accuracy: {best_score:.4f}')

    best_pipe.fit(X, y) # обучаем лучшую модель на всем датафрейме
    # записываем в pkl с метаданными
    with open('cars_pipe.pkl', 'wb') as file:
        dill.dump({
            'model': best_pipe,
            'metadata': {
                'name': 'Car price prediction model',
                'author': 'Peter Emelianov & Demir Uzun',
                'version': 1.01,
                'changes': '1.01 - add time-counter for fitting and comments',
                'date': datetime.now(),
                'type': type(best_pipe.named_steps["classifier"]).__name__,
                'accuracy': best_score
            }
        }, file)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
