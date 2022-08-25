import itertools
from typing import List

import numpy as np
import huspacy

from reviewsDatabase import ReviewsDatabase
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from summa import keywords
import pytextrank


class KeywordExtractor:
    @staticmethod
    def extract_keywords_hubert(rb: ReviewsDatabase, ngram: int, top_n=10, diversified=False, selected_ratings=(1, 2, 3, 4, 5)) -> List[str]:
        reviews_text = rb.get_filtered_reviews(selected_ratings)
        print(reviews_text)

        # Extract candidate words/phrases
        count = CountVectorizer(ngram_range=(ngram, ngram), stop_words=get_stop_words('hu')).fit([reviews_text])
        candidates = count.get_feature_names_out()

        model = SentenceTransformer("SZTAKI-HLT/hubert-base-cc")
        doc_embedding = model.encode([reviews_text])
        candidate_embeddings = model.encode(candidates)

        distances = cosine_similarity(doc_embedding, candidate_embeddings)
        result_keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]

        if diversified:
            result_keywords = KeywordExtractor.max_sum_sim(doc_embedding, candidate_embeddings, candidates, top_n, nr_candidates=20)

        return result_keywords

    @staticmethod
    def max_sum_sim(doc_embedding, candidate_embeddings, candidates, top_n, nr_candidates) -> List[str]:
        # Calculate distances and extract keywords
        distances = cosine_similarity(doc_embedding, candidate_embeddings)
        distances_candidates = cosine_similarity(candidate_embeddings,
                                                 candidate_embeddings)

        # Get top_n words as candidates based on cosine similarity
        words_idx = list(distances.argsort()[0][-nr_candidates:])
        words_vals = [candidates[index] for index in words_idx]
        distances_candidates = distances_candidates[np.ix_(words_idx, words_idx)]

        # Calculate the combination of words that are the least similar to each other
        min_sim = np.inf
        candidate = None
        for combination in itertools.combinations(range(len(words_idx)), top_n):
            sim = sum([distances_candidates[i][j] for i in combination for j in combination if i != j])
            if sim < min_sim:
                candidate = combination
                min_sim = sim

        return [words_vals[idx] for idx in candidate]

    @staticmethod
    def extract_keywords_summa_textrank(rb: ReviewsDatabase, top_n=5) -> List[str]:
        reviews_text = rb.get_all_reviews()
        text_words = reviews_text.split()
        text_without_sw = [word for word in text_words if word.lower() not in get_stop_words('hu')]
        filtered_text = " ".join(text_without_sw)
        return keywords.keywords(filtered_text, words=top_n, language='hungarian').replace(" ", "\n").split("\n")

    @staticmethod
    def extract_keywords_textrank_spacy(rb: ReviewsDatabase):
        # example text
        text = rb.get_all_reviews()
        # load a spaCy model, depending on language, scale, etc.
        # nlp = spacy.load("hu_core_news_lg")

        nlp = huspacy.load()

        # add PyTextRank to the spaCy pipeline
        nlp.add_pipe("textrank")
        doc = nlp(text)

        # examine the top-ranked phrases in the document
        for phrase in doc._.phrases:
            print(phrase.text)
            print(phrase.rank, phrase.count)
            print(phrase.chunks)
