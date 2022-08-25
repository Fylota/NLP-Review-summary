from typing import Tuple

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

    def get_all_reviews(self) -> str:
        return "\n".join(self.df["review_text"])

    def get_filtered_reviews(self, selected_rates: Tuple) -> str:
        return "\n".join(self.df[self.df['rating'].isin(selected_rates)]["review_text"])

    @staticmethod
    def from_csv(path: str) -> "ReviewsDatabase":
        df = pd.read_csv(path)
        name = path.split("/")[-1]
        return ReviewsDatabase(df, name)
