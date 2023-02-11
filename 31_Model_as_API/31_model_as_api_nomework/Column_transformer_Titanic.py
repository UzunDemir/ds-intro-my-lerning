

import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.datasets import fetch_openml
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV

np.random.seed(0) # задает начальные условия для генератора случайных чисел.
# \Генератор инициализированный одними и теми же начальными условиями,
# выдает абсолютно идентичные случайные последовательности.

# Загрузить данные с https://www.openml.org/d/40945
X, y = fetch_openml("titanic", version=1, as_frame=True, return_X_y=True)

# В качестве альтернативы X и y можно получить непосредственно из атрибута frame:
# X = titanic.frame.drop ('выжил', ось = 1)
# y = titanic.frame ['выжил']
##############################################################################################################

# Используйте ColumnTransformer , выбрав столбец по именам
# Мы будем обучать наш классификатор со следующими характеристиками:
#
# Numeric Features:
#
# age: float;
# fare: float.
# Categorical Features:
#
# embarked : категории, закодированные в виде строк {'C', 'S', 'Q'} ;
# sex : категории, закодированные в виде строк {'female', 'male'} ;
# pclass : порядковые целые числа {1, 2, 3} .
# Мы создаем конвейеры предварительной обработки как для числовых, так и для категориальных данных.
# Обратите внимание, что pclass можно рассматривать как категориальную или числовую функцию.

#############################################################################################################

numeric_features = ['age', 'fare']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

categorical_features = ['embarked', 'sex', 'pclass']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

# Добавить классификатор в конвейер предварительной обработки.
# Теперь у нас есть полный конвейер прогнозирования.
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LogisticRegression())])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=0)

clf.fit(X_train, y_train)
print("model score: %.3f" % clf.score(X_test, y_test))

##########################################################################################################

# HTML-представление Pipeline
# Когда Pipeline распечатывается в записной книжке jupyter, HTML-представление оценщика отображается следующим образом:

##########################################################################################################


from sklearn import set_config

set_config(display='diagram')
clf
Pipeline
Pipeline(steps=[('preprocessor',
                 ColumnTransformer(transformers=[('num',
                                                  Pipeline(steps=[('imputer',
                                                                   SimpleImputer(strategy='median')),
                                                                  ('scaler',
                                                                   StandardScaler())]),
                                                  ['age', 'fare']),
                                                 ('cat',
                                                  OneHotEncoder(handle_unknown='ignore'),
                                                  ['embarked', 'sex',
                                                   'pclass'])])),
                ('classifier', LogisticRegression())])

###########################################################################################################

# Используйте ColumnTransformer , выбирая столбец по типам данных
# При работе с очищенным набором данных предварительная обработка может быть автоматической,
# используя типы данных столбца, чтобы решить, рассматривать ли столбец как числовой или категориальный признак.
# sklearn.compose.make_column_selector дает такую ​​возможность.
# Во-первых, давайте выберем только подмножество столбцов, чтобы упростить наш пример.

###########################################################################################################

subset_feature = ['embarked', 'sex', 'pclass', 'age', 'fare']
X_train, X_test = X_train[subset_feature], X_test[subset_feature]

# Затем мы исследуем информацию о типе данных каждого столбца.

print(X_train.info())

############################################################################################################

# Mы можем заметить, что столбцы embarked и sex были помечены как столбцы category при загрузке данных
# с помощью fetch_openml . Следовательно, мы можем использовать эту информацию для отправки категориальных
# столбцов в categorical_transformer а остальные столбцы - в numerical_transformer .
#
# Note
#
# На практике вам придется самостоятельно обрабатывать тип данных столбца. Если вы хотите,
# чтобы некоторые столбцы считались category , вам придется преобразовать их в категориальные столбцы.
# Если вы используете pandas, вы можете обратиться к их документации относительно категориальных данных .

############################################################################################################

from sklearn.compose import make_column_selector as selector

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, selector(dtype_exclude="category")),
    ('cat', categorical_transformer, selector(dtype_include="category"))
])
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', LogisticRegression())])


clf.fit(X_train, y_train)
print("model score: %.3f" % clf.score(X_test, y_test))

# Результирующая оценка не совсем такая же, как в предыдущем конвейере,
# потому что селектор на основе pclass столбцы pclass как числовые функции, а не как категориальные, как раньше:

print(selector(dtype_exclude="category")(X_train))

print(selector(dtype_include="category")(X_train))

#############################################################################################################

# Использование конвейера прогнозирования при поиске по сетке
# Поиск по сетке также можно выполнять на различных этапах предварительной обработки,
# определенных в объекте ColumnTransformer , вместе с гиперпараметрами классификатора
# как часть Pipeline . Мы будем искать как стратегию подстановки числовой предварительной
# обработки, так и параметр регуляризации логистической регрессии, используя GridSearchCV .

############################################################################################################

param_grid = {
    'preprocessor__num__imputer__strategy': ['mean', 'median'],
    'classifier__C': [0.1, 1.0, 10, 100],
}

grid_search = GridSearchCV(clf, param_grid, cv=10)
print(grid_search)

ColumnTransformer(transformers=[('num',
                                 Pipeline(steps=[('imputer',
                                                  SimpleImputer(strategy='median')),
                                                 ('scaler', StandardScaler())]),
                                 ),
                                ('cat', OneHotEncoder(handle_unknown='ignore'),
                                 )])
SimpleImputer(strategy='median')
StandardScaler()
grid_search.fit(X_train, y_train)

print(f"Best params:")
print(grid_search.best_params_)

print(f"Internal CV score: {grid_search.best_score_:.3f}")

import pandas as pd

cv_results = pd.DataFrame(grid_search.cv_results_)
cv_results = cv_results.sort_values("mean_test_score", ascending=False)
print(cv_results[["mean_test_score", "std_test_score",
            "param_preprocessor__num__imputer__strategy",
            "param_classifier__C"
            ]].head(5))
