from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
from sklearn.model_selection import train_test_split
import pandas as pd
from pathlib import Path


class TrainTestSplitPiece(BasePiece):

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
        """
        Split the data into training and test sets.
        """
        df = self.read_data_from_file(path=input_data.data_path)

        if "target" not in df.columns:
            raise ValueError("Target column not found in data with name 'target'.")

        X_train, X_test, y_train, y_test = train_test_split(df.drop('target', axis=1), df['target'], test_size=input_data.test_data_size, random_state=input_data.random_state)

        df_train = pd.concat([X_train, y_train], axis=1)
        df_test = pd.concat([X_test, y_test], axis=1)


        train_data_path = str(Path(self.results_path) / "train_data.csv")
        test_data_path = str(Path(self.results_path) / "test_data.csv")

        df_train.to_csv(train_data_path, index=False)
        df_test.to_csv(test_data_path, index=False)

        return OutputModel(train_data_path=train_data_path, test_data_path=test_data_path)

