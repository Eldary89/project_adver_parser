import logging

from datetime import datetime
from time import sleep
from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from ..models import Advertisement

PAUSE_DURATION_SECONDS = 5

logger = logging.getLogger(__name__)


class SeleniumChromeDrive:
    def __enter__(self):
        return self._driver

    def __init__(self):
        self._options = Options()
        self._options.add_argument('--headless')
        self._options.add_argument('--no-sandbox')
        self._options.add_argument('--disable-dev-shm-usage')
        self._service = Service(executable_path=ChromeDriverManager().install())
        self._driver = webdriver.Chrome(service=self._service, options=self._options)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.close()


class AvitoScraper:

    def __init__(self) -> None:
        self._data = dict()

    def _scrape_data_by_url(self, url: str = "") -> Dict:
        with SeleniumChromeDrive() as driver:
            driver.get(url)
            sleep(PAUSE_DURATION_SECONDS)

            elements = driver.find_elements(By.XPATH, "//div[@data-marker='item']")
            logging.info(f"{len(elements)} elements parsed")
            for element in elements:
                self._data[element.get_attribute('data-item-id')] = {
                    'link': element.find_element(By.XPATH, ".//a[@itemprop='url']").get_attribute('href'),
                    'description': element.find_element(By.XPATH, ".//meta[@itemprop='description']").get_attribute(
                        'content'),
                    'title': element.find_element(By.XPATH, ".//a[@itemprop='url']").get_attribute('title'),
                    'price': element.find_element(By.XPATH, ".//meta[@itemprop='price']").get_attribute('content'),
                    'price_currency': element.find_element(
                        By.XPATH, ".//meta[@itemprop='priceCurrency']"
                    ).get_attribute('content'),
                    'category': element.get_attribute('itemtype').split('/')[-1].lower()
                }

        return self._data

    def write_data_to_models(self, url: str) -> List['Advertisement']:
        data = self._scrape_data_by_url(url)
        today = datetime.now().date()
        existing_advertisements = set(Advertisement.objects.filter(created__gt=today).values_list('remote_id'))
        keys_to_add = set(data.keys()) - existing_advertisements
        created_advertisements = [
            Advertisement.objects.create(
                remote_id=key,
                link=data[key]['link'],
                description=data[key]['description'],
                title=data[key]['title'],
                price=data[key]['price'],
                currency=data[key]['price_currency'],
                category=data[key]['category'],
            )
            for key in keys_to_add
        ]
        logging.info(f"{len(created_advertisements)} ads created")
        return created_advertisements



