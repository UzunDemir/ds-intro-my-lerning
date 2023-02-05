
###############################################################
import time
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
from sklearn.preprocessing import FunctionTransformer
from sklearn.svm import SVC

# Step 1 #####################################################################################
def filter_data(df):

    df_copy = df.copy()
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
    
    return df_copy.drop(columns_to_drop, axis=1)


# Step 2 ######################################################################################
def outliers_filler(df):
    df_copy = df.copy()

    def calculate_outliers(data):
        q25 = data.quantile(0.25)
        q75 = data.quantile(0.75)
        iqr = q75 - q25
        boundaries = (q25 - 1.5 * iqr, q75 + 1.5 * iqr)

        return boundaries

    boundaries = calculate_outliers(df_copy['year'])
    df_copy.loc[df['year'] < boundaries[0], 'year'] = round(boundaries[0])
    df_copy.loc[df['year'] > boundaries[1], 'year'] = round(boundaries[1])
    return df_copy

# Step 3 #####################################################################################
def short_model(x):
    if not pd.isna(x):
        return x.lower().split(' ')[0]
    else:
        return x

def short_model_age_category(df_copy):
    #df_copy = df_copy.copy()
    # Добавляем фичу "short_model" – это первое слово из колонки model
    df_copy.loc[:, 'short_model'] = df_copy['model'].apply(short_model)
    # Добавляем фичу "age_category" (категория возраста)
    df_copy.loc[:, 'age_category'] = df_copy['year'].apply(lambda x: 'new' if x > 2013 else ('old' if x < 2006 else 'average'))
    return df_copy

# Step 4 #####################################################################################
def numerical_categorical_transformer(df_copy):
    #df_copy = df_copy.copy()
    numerical = df_copy.select_dtypes(include=['int64', 'float64']).columns
    categorical = df_copy.select_dtypes(include=['object']).columns
    # В категориальных фичах заменяем пропуски модой
    for feat in categorical:
        df_copy[feat].fillna(df_copy[feat].mode()[0], inplace=True)

    # В численных фичах заменяем пропуски медианой
    for feat in numerical:
        df_copy[feat].fillna(df_copy[feat].median(), inplace=True)
    return df_copy

# Step 5 #####################################################################################
def encoding_One_Hot(df_copy):
    #df_copy = df_copy.copy()
    columns_to_encode = [
        'fuel',
        'title_status',
        'transmission',
        'state',
        'short_model',
        'age_category'
    ]

    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    encoder.fit(df_copy[columns_to_encode])

    df_copy.loc[:, encoder.get_feature_names()] = encoder.transform(df_copy[columns_to_encode])
    return df_copy

# Step 6 ####################################################################################
def odometer_scaling(df_copy):
    #df_copy = df_copy.copy()
    # Масштабируем числовые фичи

    scaler = StandardScaler()
    df_copy['odometer_std'] = scaler.fit_transform(df_copy[['odometer']])
    return df_copy

# Step 7 ####################################################################################
def columns_dropping(df_copy):
    #df_copy = df_copy.copy()
    columns_to_drop = [
        'year',
        'model',
        'fuel',
        'odometer',
        'title_status',
        'transmission',
        'state',
        'short_model',
        'age_category'
    ]
    df_copy = df_copy.drop(columns_to_drop, axis=1)
    return df_copy
# Step 8 ####################################################################################
def x_y_preparation_for_fit(df_copy):
    #df_copy = df_copy.copy()
    X = df_copy.drop(['price_category'], axis=1)
    y = df_copy['price_category']
    return X, y

def main():
    print('Loan Prediction Pipeline')
    # Считываем данные из файла в датафрейм
    df = pd.read_csv('data/30.6 homework.csv')
    
    step_1 = FunctionTransformer(filter_data)
    step_2 = FunctionTransformer(outliers_filler)
    step_3 = FunctionTransformer(short_model_age_category)
    step_4 = FunctionTransformer(numerical_categorical_transformer)
    step_5 = FunctionTransformer(encoding_One_Hot)
    step_6 = FunctionTransformer(odometer_scaling)
    step_7 = FunctionTransformer(columns_dropping)
    step_8 = FunctionTransformer(x_y_preparation_for_fit)

    df_final = step_1.transform(df)
    df_final = step_2.transform(df_final)
    df_final = step_3.transform(df_final)
    df_final = step_4.transform(df_final)
    df_final = step_5.transform(df_final)
    df_final = step_6.transform(df_final)
    df_final = step_7.transform(df_final)
    X, y = step_8.transform(df_final)
    
    

    models = [
        LogisticRegression(solver='liblinear'),
        RandomForestClassifier(),
        SVC()
    ]

    for m in models:
        start = time.time()
        score = cross_val_score(m, X, y, cv=4, scoring='accuracy')
        elapsed_time = time.time() - start
        print(f'model: {type(m).__name__}, acc_mean: {score.mean():.4f}, acc_std: {score.std():.4f}'
              f", with a fitting time: {elapsed_time:.3f}")




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


