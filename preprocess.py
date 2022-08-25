from typing import List
import nltk
import Levenshtein
import pandas as pd

class Preprocessor:

    vowel_dict = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú', 'ü': 'ű', 'ö': 'ő'}

    @staticmethod
    def remove_punctuation(sentence: str) -> List[str]:
        return nltk.RegexpTokenizer(r"\w+").tokenize(sentence)

    @staticmethod
    def calc_word_dist(word: str, df: pd.DataFrame) -> str:
        word_list = [word]
        for key, value in Preprocessor.vowel_dict.items():
            for i in range(word.count(key)):
                word_list.append(word.replace(key, value, i+1))
        for word_ in word_list:
            df[word_] = df["Word"].apply(lambda x: Levenshtein.distance(x, word_)) + df.index / 10000
        best_guess = df[word_list].min().idxmin()
        return df[df[best_guess] == df[best_guess].min()]["Word"].values[0]

    @staticmethod
    def correct_words(words: List[str], correct_words: List[str]) -> List[str]:
        df = pd.DataFrame(correct_words)
        df.columns = ["Word"]
        return [Preprocessor.calc_word_dist(word, df) for word in words]

    @staticmethod
    def correct_sentence(sentence: str, correct_words: List[str]) -> List[str]:
        return Preprocessor.correct_words(Preprocessor.remove_punctuation(sentence), correct_words)
