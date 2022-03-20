import bs4
import pandas as pd
import requests
from bs4 import BeautifulSoup

from reviewsDatabase import ReviewsDatabase


class ReviewCollector:
    @staticmethod
    def collect_from_bonprix(url: str) -> ReviewsDatabase:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        review_cards = soup.find_all('li', class_='text-center')
        df = pd.DataFrame([ReviewCollector.__extract_review(review) for review in review_cards],
                          columns=["review_text", "rating"])
        return ReviewsDatabase(df, "Bonprix")

    @staticmethod
    def __extract_review(review) -> (str, int):
        review_text = review.find('p', class_='comment-content').text.strip().replace("\n", "")
        stars = review.find('p', class_='product-comment-stars').span
        rating = len(list(filter(lambda star: star.attrs['class'][1] == 'text-danger', stars)))
        return review_text, rating
