import Levenshtein
import pandas as pd

word = 'jo'
df = pd.read_csv('word_list.csv', header=None, usecols=[2], nrows=15000)
df.columns = ["Word"]
df = df.astype(str)
print(df)

df["Difference"] = df["Word"].apply(lambda x: Levenshtein.distance(x, word))
df["WeightedDifference"] = df["Difference"] + df.index/10000
print(df[df["WeightedDifference"] == df["WeightedDifference"].min()])
