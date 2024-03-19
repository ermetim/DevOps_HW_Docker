from functions import DataPreprocessing
import pandas as pd
import os

test_path = os.path.join(os.getcwd(), "dataset", "prepared_test.csv")

df_test = pd.read_csv(test_path)

preprocessing = DataPreprocessing(models_folder="models")
X_test, y_test = preprocessing.run_test(df_test.head())

preprocessing.model_predict(X_test)

if __name__ == "__main__":
    print("Done")
