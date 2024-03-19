import pandas as pd
import numpy as np
import os
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

RANDOM_STATE = 12345


class DataPreprocessing:
    def __init__(self, models_folder="models"):
        self.models_path = os.path.join(os.getcwd(), models_folder)
        pass

    def save_model(self, model, file_name='default_model.pkl'):
        """
        Сохранение модели в .pkl файл
        """
        try:
            os.mkdir(self.models_path)
        except:
            pass
        file_path = os.path.join(self.models_path, file_name)
        pickle.dump(model, open(file_path, 'wb'))
        print(f'Model saved successully to {file_name}')

    def load_model(self, file_name):
        """
        Загрузка сохраненной модели из .pkl файла
        """
        file_path = os.path.join(self.models_path, file_name)
        return pickle.load(open(file_path, 'rb'))

    def my_transformer(self, df, features_to_transform, model=None, file_name='transformer_model.pkl'):
        """
        Трансформирование признаков
        Модель трансформатора подается на вход или загружается из .pkl файла
        на вход подается полностью датафрейм с указанием признаков для трансформации
        на выходе трансформированный датафрейм
        """
        if model is None:
            model_path = os.path.join(self.models_path, file_name)
            model = self.load_model(model_path)
        values = model.transform(df[features_to_transform])
        labels = model.get_feature_names_out()
        df[labels] = values
        df = df.drop(columns=features_to_transform)
        return df

    def fill_na(self, row):
        """
        Заполнение nan медианами по марке и модели
        df = df.apply(self.fill_na, axis=1)
        """
        if row.isna().sum() > 0:
            return row.fillna(self.median_values.loc[row['brand'], row['model']])
        return row

    def run_test(self, df):
        df_test = df.copy()

        # Столбец с обозначением наличия nan в столбце torque
        df_test['torque_isna'] = df_test['torque'].apply(lambda x: 0 if pd.notnull(x) else 1)

        # Медианы по маркам и моделям машин
        self.median_values = self.load_model(file_name='median_values_model.data')

        if df_test.isna().sum().sum() > 0:
            # Заполнение столбцов с nan
            df_test = df_test.apply(self.fill_na, axis=1)

            # Стольбцы с nan
            nan_cols = df_test.isna().sum()[df_test.isna().sum() != 0].index

            # Заполнение остатков nan медианами по столбцу
            df_test[nan_cols] = df_test[nan_cols].fillna(df_test[nan_cols].median())

        # квадрат года
        df_test['sq_year'] = df_test['year'] ** 2

        # столбец с числом "лошадей" на литр объема
        df_test['power/engine'] = df_test['max_power'] / df_test['engine']

        # seats в категории
        df_test['seats'] = df_test['seats'].astype('object')

        if 'selling_price' in df_test.columns:
            # Разделение на признаки и целевой признак с удалением части категориальных признаков
            y_test = df_test['selling_price']
            X_test = df_test.drop(columns=['selling_price'])

        else:
            X_test = df_test
            y_test = None

        # Список категориальных признаков для OHE
        cat_features = X_test.dtypes[X_test.dtypes == 'object'].index

        # OHE
        X_test = self.my_transformer(X_test, cat_features, file_name='ohe_model.pkl')

        return X_test, y_test

    def run_train(self, df):
        df_train = df.copy()
        if df_train.isna().sum().sum() > 0:
            # Стольбцы с nan
            nan_cols = df_train.isna().sum()[df_train.isna().sum() != 0].index

            # Медианы по маркам и моделям машин
            self.median_values = df_train.groupby(by=['brand', 'model'])[nan_cols].median()
            self.save_model(self.median_values, file_name='median_values_model.data')

            # Столбец с обозначением наличия nan в столбце torque
            df_train['torque_isna'] = df_train['torque'].apply(lambda x: 0 if pd.notnull(x) else 1)

            # Заполнение столбцов с nan
            df_train = df_train.apply(self.fill_na, axis=1)

            # Стольбцы с nan
            nan_cols = df_train.isna().sum()[df_train.isna().sum() != 0].index

            # Заполнение остатков nan медианами по столбцу
            df_train[nan_cols] = df_train[nan_cols].fillna(df_train[nan_cols].median())

        # квадрат года
        df_train['sq_year'] = df_train['year'] ** 2

        # столбец с числом "лошадей" на литр объема
        df_train['power/engine'] = df_train['max_power'] / df_train['engine']

        # seats в категории
        df_train['seats'] = df_train['seats'].astype('object')

        # Удаление дубликатов, которые отличаются только ценой. Оставим более свежие записи.
        df_train = df_train.sort_values(by='year')
        col = df_train.drop(columns=['selling_price']).columns
        df_train = df_train.drop_duplicates(subset=col, keep='last').reset_index(drop=True)

        # Разделение на признаки и целевой признак с удалением части категориальных признаков
        y_train = df_train['selling_price']
        X_train = df_train.drop(columns=['selling_price'])

        # Список категориальных признаков для OHE
        cat_features = X_train.dtypes[df_train.dtypes == 'object'].index

        # OHE для категориальных признаков
        ohe = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')
        ohe.fit(X_train[cat_features])
        X_train = self.my_transformer(X_train, cat_features, model=ohe)

        # Сохранение трансформатора OHE
        self.save_model(model=ohe, file_name='ohe_model.pkl')

        # Логарифмирование целевого признака
        y_train = np.log(y_train + 1)

        return X_train, y_train

    def model_train(self, X_train, y_train, X_test=None, y_test=None, file_name='LinearRegression_model.pkl'):
        model = LinearRegression()
        model.fit(X_train, y_train)
        self.save_model(model=model, file_name=file_name)
        if X_test is not None and y_test is not None:
            prediction = np.round(np.exp(model.predict(X_test)) - 1)
            score_r2 = r2_score(y_test, prediction)
            print('Метрика R2 = ', round(score_r2, 3))
        print('Train model finished successfully')

    def model_predict(self, X_test, y_test=None, file_name='LinearRegression_model.pkl'):
        model = self.load_model(file_name=file_name)
        prediction = np.round(np.exp(model.predict(X_test)) - 1)
        print(prediction)
        if y_test is not None:
            score_r2 = r2_score(y_test, prediction)
            print('Метрика R2 = ', round(score_r2, 3))
        else:
            score_r2 = None
        return prediction, score_r2
