import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier


def main():
    print('Loan Prediction Pipeline')
    # Считываем данные из файла в датафрейм и удалим из него Loan_ID
    df = pd.read_csv('data/loan_train.csv').drop('Loan_ID', axis=1)

    X = df.drop('Loan_Status', axis=1) # Сформируем датафрейм с предикторами
    # Запишем целевую переменную и переведем ее в числовое значение
    Y = df['Loan_Status'].apply(lambda x: 1.0 if x == 'Y' else 0.0)

    # Сохраним численные и категориальные признаки в разные переменные
    numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X.select_dtypes(include=['object']).columns

    # Создадим объект класса пайплайн
    # пайплайн состоит из шагов
    # каждый шаг - объект класса со свои именем
    # этот объект и выполнит необходимые преобразования
    # шаги задаются кортежами, где 1 - имя, 2 - объект класса преобразователя
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')), # заполнение пропусков медианой
        ('scaler', StandardScaler()) # стандартизируем числовае значения
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')), # заполним пропуски модой (самое частое
                                                              # встречающееся значение - most_frequent
        ('encoder', OneHotEncoder(handle_unknown='ignore')) # закодируем текстовые значения в числовые
                                                            # и игнорируем ошибки кодирования

    ])
    #  объединим эти два пайплайна в один шаг
    preprocessor = ColumnTransformer(transformers=[    # ColumnTransformer принимает список кортежей из трех
        ('numerical', numerical_transformer, numerical_features), # компонентов: 1 - название преобразователя
                                                  # 2 - само преобразование (пайплайны)
                                                  # 3 - имена колонок, к которым применяется преобразование
        ('categorical', categorical_transformer, categorical_features)
    ])
# обучение модели - часть пайплайна, поэтому завернем его в класс пайплайна

    # список моделей для обучения
    models = (
        LogisticRegression(solver='liblinear'),
        RandomForestClassifier(),
        MLPClassifier(activation='logistic', hidden_layer_sizes=(256, 128, 64))
    )
    # счетчик
    best_score = .0
    # лучший
    best_pipe = None

    # пройдем по моделям
    for model in models:
        # на каждой итерации будем составлять пайплайн
        pipe = Pipeline(steps=[
            ('preprocessor', preprocessor), # 1 шаг - обработка признаков (сам является пайплайном!)
            ('classifier', model)           # 2 шаг - вызов модели обучения
        ])
        # кросс валидация на 4 фолда
        score = cross_val_score(pipe, X, Y, cv=4, scoring='accuracy')
        # печатаем имя модели и значения accuracy
        print(f'model: {type(model).__name__}, acc_mean: {score.mean():.4f}, acc_std: {score.std():.4f}')

        if score.mean() > best_score:
            best_score = score.mean() # лучшая точность
            best_pipe = pipe # выбор лучшего пайплайна

    print(f'best model: {type(best_pipe.named_steps["classifier"]).__name__}, accuracy: {best_score:.4f}')
    joblib.dump(best_pipe, 'loan_pipe.pkl') # сохраняем лучшую модель в pikle

if __name__ == '__main__':
    main()


