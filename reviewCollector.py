import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from reviewsDatabase import ReviewsDatabase


class ReviewCollector:

    @staticmethod
    def __emag_find_next_page_button(driver: WebDriver):
        nav = driver.find_element(By.CLASS_NAME, 'js-reviews-paginator')
        nav_buttons = nav.find_elements(By.TAG_NAME, 'li')
        return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((nav_buttons[len(nav_buttons) - 1])))

    @staticmethod
    def collect_from_bonprix(url: str) -> ReviewsDatabase:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        review_cards = soup.find_all('li', class_='text-center')
        df = pd.DataFrame([ReviewCollector.__extract_review(review) for review in review_cards],
                          columns=["review_text", "rating"])
        return ReviewsDatabase(df, url)

    @staticmethod
    def collect_from_emag(url: str) -> ReviewsDatabase:
        driver = webdriver.Chrome(r'C:\webdrivers\chromedriver.exe')
        driver.get(url)
        driver.implicitly_wait(10)

        # Scroll to pagination nav
        ActionChains(driver).move_to_element(driver.find_element(By.CLASS_NAME, 'js-reviews-paginator')).perform()
        # Accept cookies
        cookie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-accept')))
        cookie_button.click()

        # Dismiss login
        login_dismiss_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'js-dismiss-login-notice-btn')))
        login_dismiss_button.click()

        nav_list = driver.find_element(By.CLASS_NAME, 'js-reviews-paginator').find_elements(By.TAG_NAME, 'li')
        num_of_pages = int(nav_list[len(nav_list) - 2].text)

        reviews = dict()

        for x in range(num_of_pages):
            response = BeautifulSoup(driver.page_source, 'html.parser')
            review_divs = response.find_all('div', class_='product-review-item')
            reviews.update(
                {review.find('div', class_='review-body-container').text.strip().replace("\n", ""): ReviewCollector.__get_stars_emag(review) for review in
                 review_divs})

            next_page_button = ReviewCollector.__emag_find_next_page_button(driver)
            next_page_button.click()

        response = BeautifulSoup(driver.page_source, 'html.parser')
        review_divs = response.find_all('div', class_='product-review-item')
        reviews.update(
            {review.find('div', class_='review-body-container').text.strip().replace("\n", ""): ReviewCollector.__get_stars_emag(review) for review in
             review_divs})

        df = pd.DataFrame(reviews.items(), columns=["review_text", "rating"])
        return ReviewsDatabase(df, url)

    @staticmethod
    def __get_stars_emag(review) -> int:
        stars = review.find('div', class_='star-rating')
        tag = stars.attrs['class'][2]
        return int(tag[len(tag)-1])


    @staticmethod
    def __extract_review(review) -> (str, int):
        review_text = review.find('p', class_='comment-content').text.strip().replace("\n", "")
        stars = review.find('p', class_='product-comment-stars').span
        rating = len(list(filter(lambda star: star.attrs['class'][1] == 'text-danger', stars)))
        return review_text, rating
