import pandas as pd
from datetime import datetime


class ReviewsDatabase:
    def __init__(self, df: pd.DataFrame, name: str):
        self.df = df
        self.name = name
        self.date = datetime.now()

    def write_to_csv(self, out_path: str):
        self.df.to_csv(out_path, index=False)

    def refresh_csv(self, out_path: str):
        try:
            self.append(pd.read_csv(out_path))
            self.df.drop_duplicates(inplace=True, )
        except FileNotFoundError:
            pass
        finally:
            self.write_to_csv(out_path)

    def append(self, data: pd.DataFrame):
        self.date = datetime.now()
        self.df = pd.concat([self.df, data], ignore_index=True, )
