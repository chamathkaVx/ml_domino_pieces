from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import pandas as pd
from sklearn.preprocessing import StandardScaler
from pathlib import Path

class StandardScalerPiece(BasePiece):

    def read_data_from_file(self, path):
        """
        Read data from a file.
        """
        if path.endswith(".csv"):
            return pd.read_csv(path)
        elif path.endswith(".json"):
            return pd.read_json(path)
        else:
            raise ValueError("File type not supported.")

    def piece_function(self, input_data: InputModel):


        df_train = self.read_data_from_file(path=input_data.train_data_path)
        df_test = self.read_data_from_file(path=input_data.test_data_path)

        if "target" not in df_train.columns or "target" not in df_test.columns:
            raise ValueError("Target column not found in data with name 'target'.")

        scaler = StandardScaler()
        scaler.fit(df_train.drop('target', axis=1))
        X_train = scaler.transform(df_train.drop('target', axis=1))
        X_test = scaler.transform(df_test.drop('target', axis=1))

        df_train_scaled = pd.DataFrame(X_train, columns=df_train.drop('target', axis=1).columns)
        df_train_scaled['target'] = df_train['target']
        df_test_scaled = pd.DataFrame(X_test, columns=df_test.drop('target', axis=1).columns)
        df_test_scaled['target'] = df_test['target']

        train_data_path = str(Path(self.results_path) / "scaled_train_data.csv")
        test_data_path = str(Path(self.results_path) / "scaled_test_data.csv")

        df_train_scaled.to_csv(train_data_path, index=False)
        df_test_scaled.to_csv(test_data_path, index=False)

        return OutputModel(train_data_path=train_data_path, test_data_path=test_data_path)


