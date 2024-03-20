import pandas as pd
import os

from src.functions import DataPreprocessing


train_path = os.path.join(os.getcwd(), "dataset", "prepared_train.csv")
test_path = os.path.join(os.getcwd(), "dataset", "prepared_test.csv")

df_train = pd.read_csv(train_path)
df_test = pd.read_csv(test_path)

preprocessing = DataPreprocessing(models_folder="models")
X_train, y_train = preprocessing.run_train(df_train)
X_test, y_test = preprocessing.run_test(df_test)

preprocessing.model_train(X_train, y_train, X_test, y_test)

if __name__ == "__main__":
    print("Done")
